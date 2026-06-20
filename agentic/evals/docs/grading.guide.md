# Grading evals: grade the principle, not the method

When an eval flags a regression, check the **metric measures the principle** before changing the
thing under test.

The `doc-this--context-discovery` grader once required the agent's *literal first action* to be a
README **read** and counted any non-README glob as a "blind search" — so it failed benign "glob to
locate the README, then read it" and manufactured a phantom regression that burned a whole
copy-tuning cycle. The fix: grade whether a README is read **before any code/content access** (a
content `Grep` or a non-README `Read`); globs only *locate* files and are navigation, not violations.

**General rule:** a good check **passes obviously-correct behavior and fails obviously-wrong
behavior**. If it doesn't, fix the grader first — don't tune the artifact to satisfy a metric that's
testing the wrong thing.

## Related
- [doc-this--context-discovery](../doc-this--context-discovery/) — the eval whose grader prompted this lesson.
