---
name: orchestrate-seats
description: "Model-seat delegation policy (opus, neon, fable, sol, ds-flash), prompting rules, write ownership, and readability gate. Load before multi-track subagent delegation when staffing specific model seats."
---

# Orchestrate Seats

Own the sequence and acceptance of delegated work. You are on the hook for what
children produce: a successful report does not make an implementation
understandable or ready to merge.

## Models

Staff every seat with a named droid from `~/.factory/droids/` below. Avoid
staffing model-sensitive seats with generic `worker` or `explorer`: they route
by settings complexity tier rather than an explicitly chosen model.

### Opus (`opus`)

- Default for high-judgment coding and writing
- Extremely intelligent and versatile
- Great for system design, clean code implementation, UI/UX, and prose/copy
- Tendency to underdiscover or guess from memory unless prodded and scoped; keep briefs grounded with verified facts
- Overprescribing can hurt its creativity and taste, so clear goals and constraints beat micromanagement

### Neon (`neon`)

- Clean code, UI/UX, and prose/copy (Gemini 4 Neon)
- Strong at crisp implementation and user-facing writing
- NOT for exhaustive data gathering or deep codebase due diligence; pair with `sol` or `ds-flash` for mining first

### Sol (`sol`, read-only)

- Fast, cheap, read-only miner and investigator (`tools: read-only`, `mcpServers: []`)
- Strong miner: loads skills on its own, digs through past sessions with `dsx`, and reproduces or traces defects cleanly
- Keeps observed, reproduced, and unmeasured apart
- Not a designer: reaches the right core but tends to add mechanism. Give it the mining brief and let `opus`, `neon`, or `fable` design from its report

### Fable (`fable`)

- Strong system design, approach design, coherent implementation, UI/UX, and structural review
- Stays grounded and excellent at long-term coherence
- Can be slower and occasionally less proactive; give it crisp scope and a checkable done

### DS-Flash (`ds-flash`)

- Very lean, fast, cheap bounded implementation and evidence gathering
- Good adversarial attacker and parallel fan-out worker
- Higher variance / lower pass@1 than frontier seats; compensate with tight briefs and overcoverage or verification

## Prompting

- Provide verified, ground-truth context/facts, useful commands, etc., that you don't want it to rediscover.
- Provide prime-directive, action-oriented *goals*, not a prescription on how.
- Provide hard constraints when you deem apt.
- Provide a checkable definition of done.
- Suggest or directly trigger skills freely.

## Rules

1. Never accept obfuscated code as mergeable code, even with green tests or a
   confident author. Require simplification or verified necessity with a
   discoverable explanation; see the readability gate.
2. Never let parallel writers share a changing contract or write ownership.
   Settle prerequisites and approvals before dispatching consumers.
3. Never replace missing Task access with shell-spawned agents. Return a
   dispatch request to the parent.
4. Never accept a child's report unread. Read the decisive diff and run the
   [readability gate](references/readability.md) first.

## Failure map

| Symptom | Action |
|---|---|
| Code looks inexplicable; author reports success | Hold acceptance and run [readability](references/readability.md). |
| Clarification exists only in the agent transcript | Have the owner simplify the code or record the non-obvious constraint beside it. |
| Explanation sounds plausible but lacks evidence | Verify the decisive caller or external contract; do not treat the explanation as proof. |
| Child rediscovered what you already knew, or returned narrative instead of evidence | The brief was missing facts or a checkable done ([prompting](#prompting)); fix it before resuming. |
| Model unavailable, interrupted writer, or unclear ownership | Follow [coordination](references/coordination.md) before reassigning. |
| Fresh edits invalidate QA | Re-run the checks those edits touch; keep the rest of the evidence. |

## References

- [references/coordination.md](references/coordination.md): delegation and
  the fan-out workflows (mine then write; design, build, attack).
- [references/readability.md](references/readability.md): comprehend, clarify,
  simplify or justify, and re-check before accepting an implementation.
