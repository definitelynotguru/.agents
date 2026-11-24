import json
import tempfile
import unittest
from pathlib import Path

from hooks import state_capture
from hooks.pre_tool_use import protect_paths
from hooks.session_start import instructions as session_instructions
from hooks.subagent_stop import log_errors as subagent_log_errors
from hooks.utils.types import PreCompactInput, SessionEndInput, SubagentStopInput


class ProtectPathsTest(unittest.TestCase):
    def test_blocks_env_and_git_and_allows_env_example(self) -> None:
        kwargs = {
            "protected_basenames": protect_paths.DEFAULT_PROTECTED_BASENAMES,
            "allowed_basenames": protect_paths.DEFAULT_ALLOWED_BASENAMES,
            "protected_segments": protect_paths.DEFAULT_PROTECTED_SEGMENTS,
        }
        self.assertIsNotNone(protect_paths.match_protected_path("/repo/.env", **kwargs))
        self.assertIsNotNone(protect_paths.match_protected_path("/repo/.env.local", **kwargs))
        self.assertIsNotNone(protect_paths.match_protected_path("/repo/.git/config", **kwargs))
        self.assertIsNotNone(protect_paths.match_protected_path("/home/u/.ssh/id_ed25519", **kwargs))
        self.assertIsNone(protect_paths.match_protected_path("/repo/.env.example", **kwargs))
        self.assertIsNone(protect_paths.match_protected_path("/repo/src/app.ts", **kwargs))

    def test_extracts_apply_patch_paths(self) -> None:
        patch = (
            "*** Begin Patch\n"
            "*** Update File: src/app.ts\n"
            "*** Add File: .env.production\n"
            "*** End Patch\n"
        )
        paths = protect_paths.extract_target_paths("ApplyPatch", {"patch": patch})
        self.assertEqual(paths, ["src/app.ts", ".env.production"])


class StateCaptureTest(unittest.TestCase):
    def test_captures_pre_compact_and_session_end(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger_dir = root / "work" / ".agents" / "ledgers"
            ledger_dir.mkdir(parents=True)
            (ledger_dir / "campaign.md").write_text("# ledger\n", encoding="utf-8")
            state_dir = root / "state"

            cfg = {"enabled": True, "state_dir": str(state_dir), "max_files": 50}
            pre = PreCompactInput(
                session_id="sess-123",
                transcript_path="/tmp/sess.jsonl",
                cwd=str(root / "work"),
                permission_mode="auto-high",
                hook_event_name="PreCompact",
                message_id=None,
                trigger="auto",
                custom_instructions=None,
                message_count=42,
                estimated_tokens=150000,
            )
            out_path = state_capture.capture(pre, cfg)
            self.assertIsNotNone(out_path)
            end = SessionEndInput(
                session_id="sess-123",
                transcript_path="/tmp/sess.jsonl",
                cwd=str(root / "work"),
                permission_mode="auto-high",
                hook_event_name="SessionEnd",
                message_id=None,
                reason="prompt_input_exit",
                session_duration_ms=98000,
                message_count=55,
            )
            state_capture.capture(end, cfg)

            saved = json.loads((state_dir / "sess-123.json").read_text(encoding="utf-8"))
            self.assertEqual(saved["last_event"], "SessionEnd")
            self.assertEqual(len(saved["events"]), 2)
            self.assertEqual(saved["events"][0]["event"], "PreCompact")
            self.assertEqual(saved["events"][1]["event"], "SessionEnd")
            self.assertEqual(len(saved["ledgers"]), 1)
            self.assertTrue((state_dir / "latest.json").is_file())
            lines = (state_dir / "history.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)


class LedgerDiscoveryTest(unittest.TestCase):
    def test_discovers_active_ledgers_in_cwd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger_dir = root / ".agents" / "ledgers"
            ledger_dir.mkdir(parents=True)
            (ledger_dir / "alpha.md").write_text("# a\n", encoding="utf-8")
            (ledger_dir / "alpha.notes.md").write_text("# notes\n", encoding="utf-8")
            block = session_instructions._discover_ledgers_block(str(root))
            self.assertIn("alpha.md", block)
            self.assertIn("alpha.notes.md", block)


class SubagentStopErrorLogTest(unittest.TestCase):
    def test_logs_only_when_task_error_is_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "subagent-errors.jsonl"
            cfg = {"enabled": True, "log_path": str(log_path)}
            ok_event = SubagentStopInput(
                session_id="s1",
                transcript_path="/tmp/t",
                cwd="/tmp",
                permission_mode="auto-high",
                hook_event_name="SubagentStop",
                message_id=None,
                task_name="explorer",
                task_result="done",
                task_error=None,
                stop_hook_active=False,
            )
            self.assertIsNone(subagent_log_errors.record_error(ok_event, cfg))
            self.assertFalse(log_path.exists())

            err_event = SubagentStopInput(
                session_id="s1",
                transcript_path="/tmp/t",
                cwd="/tmp",
                permission_mode="auto-high",
                hook_event_name="SubagentStop",
                message_id=None,
                task_name="sol",
                task_result=None,
                task_error="model_authentication_failed",
                stop_hook_active=False,
            )
            written = subagent_log_errors.record_error(err_event, cfg)
            self.assertEqual(written, log_path)
            entry = json.loads(log_path.read_text(encoding="utf-8").strip())
            self.assertEqual(entry["task_name"], "sol")
            self.assertEqual(entry["task_error"], "model_authentication_failed")


if __name__ == "__main__":
    unittest.main()
