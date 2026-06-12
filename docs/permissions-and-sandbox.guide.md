# Agent Permissions & Sandbox — Security Model

How this workspace keeps an AI coding agent useful but contained. The enforcement lives in
[`.claude/settings.json`](../.claude/settings.json); this guide explains how to *operate* it and
why it's safe.

## Two operating modes

Both modes run on the **same OS-sandbox baseline** (`sandbox.enabled: true`) — the agent's files
are confined to the project folder and its web access goes through an allowlist. They differ by
**one setting**, `permissions.defaultMode`:

| | 🌙 **Away — autonomous** | 👤 **Around — supervised** |
|---|---|---|
| `defaultMode` | `dontAsk` | `default` |
| You are… | not at the laptop | at the laptop |
| Un-allowed action | **auto-denied, no prompt** | **asks you**; your *yes* extends the allowlist |
| Best for | unattended / overnight runs | day-to-day work, granting new access |

**Switch by changing one word** in `.claude/settings.json`: `"defaultMode": "dontAsk"` ⇄
`"default"`. (There is no `"ask"` mode — supervised mode is literally `"default"`.) Changes take
effect next session.

> Around mode is how the allowlist *grows*: when the agent needs a command or web domain it
> doesn't have, it asks; approving adds it, so future Away runs are more capable. In Away those
> same requests are silently denied — so **pre-seed what an unattended run needs** before you leave.

## What the agent can and cannot do (true in BOTH modes)

The sandbox guarantees these regardless of mode — the mode only changes what happens for things
*not yet allowed*.

| | ✅ Can | ❌ Cannot |
|---|---|---|
| **Files** | read/write inside the **project folder** | write outside it (kernel-blocked); read credential dirs — `~/.ssh`, `~/.aws`, … (`denyRead`) |
| **Shell** | run Bash confined to the project | run deny-listed commands; let a subprocess escape the project folder |
| **Web** | reach **allow-listed** domains | reach any other domain — exfiltration path closed |

## `deny` vs `ask` — the command policy

Three buckets, by how much trust a command needs:

- **`allow`** — safe, runs in both modes: in-project `Edit`/`Write`, sandboxed `Bash`, `WebSearch`.
- **`ask`** — *supervised-only*: **denied in Away, prompts you in Around**. For commands that are
  **legitimate sometimes, reversible, and judgeable at the prompt**: `sudo`, `git push`,
  `git reset --hard`, `git clean`, `dd`.
- **`deny`** — hard wall in every mode. For commands that are **never legitimate here,
  catastrophic/irreversible, or un-reviewable at approval time**: `rm -rf /` & `~`, `mkfs`,
  force-push, and `curl|sh` / `wget|sh` (you can't see what the remote serves before it runs, so a
  prompt would give you no real choice).

The rule of thumb: if you could *sensibly* approve it at a prompt, it's `ask`; if approving it
would be a reflex you'd regret, it's `deny`.

**Protected paths come for free.** Claude Code never auto-approves writes to `.git`, `.claude`,
`.mcp.json`, `.envrc`, `.npmrc`, shell rc files, etc. — **denied in Away, prompted in Around**, and
no `allow` rule can override it. So the agent can't silently widen its own policy or add a malicious
MCP server.

## Why this is safe

- **The OS enforces the box, not the model.** The file and network limits hold even if hostile
  instructions reach the agent via web content (prompt injection) — it *physically* cannot leave
  the project folder or reach a non-allow-listed host.
- **The egress allowlist is the anti-exfiltration control.** Reading a secret is useless to an
  attacker if it can't be sent anywhere; the allowlist (plus `denyRead`) is what stops the leak.
- **Rules are a softer inner layer.** The deny/ask lists are a mistake-guard — evadable on their
  own. The sandbox is the hard boundary. Defense in depth.
- **Caveat:** TLS isn't inspected, so a *broad* allow-listed domain can still be abused via domain
  fronting. **Keep `allowedDomains` tight**, especially for Away runs.

## Known limits / your responsibilities

The sandbox is strong but not total. You own these:

1. **The egress allowlist covers Bash only** — `WebFetch` and **MCP tools** are *not* sandboxed.
   Away denies them (they're not in `allow`); in Around, vetting them is on you.
2. **Anything you allow-list is also a channel an injected agent can use** (e.g. GitHub is a
   write-capable exfil sink). Keep the allowlist as small as the work needs.
3. **The sandbox protects the machine *from* the project, not the project *from* the agent.**
   In-project files — including uncommitted/untracked work — can still be deleted or clobbered.
   **Commit or stash before an Away run.**
4. **Review agent-authored diffs before committing** — especially `CLAUDE.md` / `AGENTS.md` (not
   protected paths, so editable) and build files (`Makefile`, `package.json` scripts, CI YAML),
   which run later outside the sandbox.

## Tuning safely

Editing the posture means editing [`.claude/settings.json`](../.claude/settings.json). **Do it on a
branch, review the diff, and merge** — never hand-loosen on `main` unreviewed. The guiding rule is
**least privilege: add the narrowest thing that unblocks the work, grant it in Around so you see
exactly what's asked, and re-tighten when the task is done.** Changes take effect next session.

### Add a web domain (`sandbox.network.allowedDomains`)

- **Let the agent hit the wall in Around first.** It will prompt for the *exact* host it needs;
  approve, then copy that host into `allowedDomains`. Don't pre-add domains speculatively.
- **Add the most specific host that works** — `api.example.com`, not `example.com`; never a bare
  TLD or a wildcard you don't need.
- **Every domain is an exfiltration channel** an injected agent can also use. Avoid general-purpose
  sinks (paste sites, gists, generic object stores). GitHub is already dual-use — don't widen it.
- **TLS isn't inspected**, so a broad entry enables domain fronting. Keep the list tight, especially
  for Away runs. If a domain was needed for a one-off, remove it afterward.

### Add a secret path to block (`sandbox.filesystem.denyRead`)

- `denyRead` is **allow-by-default**: the sandbox reads the whole disk *except* what you list. So you
  **add to it, you don't remove** — any new credential location you keep (a vault dir, a cloud cred
  cache, a `.env` *outside* the project) belongs here.
- Use `~/` for home-relative paths, absolute for elsewhere. Over-inclusion is safe (it's a denylist);
  re-allow a sub-path with `allowRead` only if something legitimate breaks.
- **It does not cover in-project secrets** — a `.env` inside the project sits in the writable cwd.
  Gate those with a permission rule instead: `deny: ["Read(/.env)", "Read(/**/.env*)"]` (trade-off:
  breaks legit reads of that file, so opt in deliberately).

### Move a command between `allow` / `ask` / `deny`

- Decide by the rule of thumb: safe and frequent → **`allow`**; sensibly approvable at a prompt →
  **`ask`**; a reflex you'd regret, unreviewable, or catastrophic → **`deny`**.
- To let the agent run a new command **unattended**, add a **narrow** `allow` rule
  (`Bash(npm test *)`, not blanket). To allow it **only under supervision**, put it in `ask`.
- When you approve a prompt with "yes, don't ask again", the rule is written to
  `settings.local.json` (local, git-ignored) — fine for personal/machine-specific approvals. To make
  it part of the **shared** posture, move it into the committed `.claude/settings.json` `allow` list.

### After any change

- Restart `claude` (changes apply next session) and **re-verify**: `/permissions`, the `/sandbox`
  Config tab, and the wall tests (in-project write, a denied command, a non-allow-listed `curl`).
- Commit with a clear message. For unattended runs, ship the **smallest** allowlist that works.

## Portability

This posture is **self-contained in `.claude/settings.json`** — no dependency on global
`~/.claude` settings. To give another project the same posture, copy that file over and tune its
`allowedDomains` / `denyRead` to fit (see [Tuning safely](#tuning-safely)).
