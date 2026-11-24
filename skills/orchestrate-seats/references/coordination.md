# Coordination

Fan out more droids than your first instinct says. If it's ever too much, I
will let you know.

## Delegation

- Delegate by default, but freely handle small work yourself when you
  understand the task deeply and a handoff would cost more than the work.
- Judge task scoping by uncertainty and coupling, not line count.
- Never split substantive work into small edits to dodge delegation.
- Resume an existing coding owner for corrections rather than editing
  underneath it.
- If an owner gets sloppy, kill it and start a fresh one.
- You are in charge, so be as aggressive and ruthless as necessary. Do not
  hesitate.
- A subagent launched during spec mode cannot write, and a resume keeps the
  flag. Launch writers fresh after a spec approval.
- Delivery is not liveness: judge a child by Task state, PID, and disk, not by
  whether a tick arrived.

## Workflows

Core pattern: fan out, then coalesce. Independent seats work in parallel; you
merge their output before the next stage.

### Mine, then write

**For:** copy or prose built from data or evidence: write-ups, PR bodies,
summaries.

1. **Mine:** `sol` and `ds-flash` mine the data sources and write thorough reports.
2. **Write:** `opus` or `neon` writes from the reports.
3. **Verify:** `sol` fact-checks the draft against ground truth.
4. **Refine:** `opus` or `neon` corrects it from the findings.

### Design, build, attack

**For:** net-new systems, or overhauls of systems and architectures.

**Design**

1. **Ground:** ground yourself in the problem and derive the crux of what we
   want to achieve (crux lens steps 1–2,
   `~/.agents/skills/review-pr/references/lenses/crux.md`).
2. **Round table:** freeform `opus`, `fable`, and `neon` each solve the crux
   from first principles (that lens's steps 3–5: pure solution, then layers
   of reality). `sol` does not sit at the table; it mines the evidence the
   designers work from.
3. **Cross-critique:** send every proposal to every other designer for an
   independent critique.
4. **Mine:** `sol` breaks down the proposals and critiques against the codebase.
5. **Elucidate:** a fresh `opus` and a fresh `fable` each derive an independent,
   clean proposal from all of the above.
6. **Attack:** the round-table designers critique both proposals.
7. **Converge:** derive the final, golden proposal yourself, unless the attack
   found glaring issues in either; then go back to Mine. Fix findings by
   cutting (AGENTS.md, "When findings arrive"); a finding only a new mechanism
   can answer goes back to Mine as a constraint.
8. **Finalize:** a fresh `fable` judges the write-up (completeness, clarity), not
   the architecture; apply its feedback.

**Build**

1. **Build:** fan out builders (`opus`, `neon`, `fable`, `ds-flash`) extensively.
2. **Attack:** fan out attackers (`ds-flash`, `sol`, `senior-code-reviewer`) extensively, incrementally or at the end.
3. **Fix:** reuse builders for minor issues; start fresh ones for extensive
   issues. When a round's fixes would add more mechanism than they remove,
   stop fixing and send that part back through Design with the findings as
   constraints.
4. **Review:** attackers confirm their issues are fixed, then `review-pr`
   subagents (`fable`, `opus`, `sol`) review. Loop with Fix until clean.
5. **Finish:** report what was done, how, and the deliverables, with a
   show-me view when structure warrants it.
