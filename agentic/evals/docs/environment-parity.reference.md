# Environment parity — reference

Why eval executors must **not** install dependencies at run time, and how to pre-provision instead
so an eval run matches production.

Eval executors are spawned subagents: a `pip install` inside one needs a permission prompt the
subagent can't answer (so it's auto-denied) and, if the Bash sandbox is on, network too. Relying on
runtime `pip` makes runs flaky and breaks eval-vs-actual parity — the executor silently does
something different from production. So **don't install at run time**; pre-provision:

1. **Install the dependency once into the same `python3`** the executors use:
   `pip3 install --user --break-system-packages <pkg>`. It is then importable for every interactive
   run and subagent — no network in the loop.
2. **Guard it in the eval's `prepare.py`** with an importability check that fails loudly with the
   install command, so a missing dep stops the run instead of silently degrading it.
   `subtitle-translate-zh/prepare.py` does this for OpenCC (`check_opencc()`).

## Current eval dependencies

- `opencc-python-reimplemented` — [subtitle-translate-zh](../subtitle-translate-zh/), OpenCC `s2twp`
  conversion. Install: `pip3 install --user --break-system-packages opencc-python-reimplemented`.
  Without it, `with_skill` runs silently fall back to a manual Hans→Hant conversion and measure the
  wrong workflow.

The other skills need none — `slides-png-to-text` transcribes slide PNGs with the model (no
library), and the rest are stdlib-only. Prefer keeping it that way: a zero-dependency skill has
parity by construction.
