---
name: talk-video-file
description: >-
  Create a `video-file.html` meta-redirect bookmark inside a talk folder that
  points to the talk's recording on Google Drive. The large `.mov` recordings
  live in committee-only Drive and stay out of the public GitHub repo; this HTML
  stub is the committed in-repo pointer to them. Use whenever the user hands over
  a Google Drive link for a talk recording and wants it bookmarked, says the
  video is "stored separately"/"in Drive"/"not in the repo", asks to link or
  reference a recording from its talk folder, or mentions `video-file.html` —
  even across several talks at once.
---

# Bookmarking a talk recording with video-file.html

Talk recordings are multi-gigabyte `.mov` files kept in a Google Drive that only JB Agentic committee members can open. They are deliberately excluded when the repo is published to GitHub. So each talk folder carries a tiny committed `video-file.html` that redirects whoever opens it to the real video in Drive — a durable bookmark that survives in the public repo without shipping the file itself.

## Input

- A talk folder `deliverables/talks/JBAgentic-<YYYYMMDD>-meetup-<N>-<Speaker>-<TopicSlug>/` (the same folder holding the SRTs and `slides.pdf`).
- A Google Drive share link for that talk's recording, e.g. `https://drive.google.com/file/d/<FILE_ID>/view?usp=drive_link`. If the user names the talk but not the link (or vice versa), ask — don't guess which recording maps to which folder.
- When several talks are given at once, treat each as one (folder, link) pair and write one file per folder.

## Output

- `video-file.html` written **inside the talk folder** (sibling to the SRTs), containing a meta-refresh redirect plus a visible clickable fallback link:

  ```html
  <meta http-equiv="refresh" content="0; url=<DRIVE_LINK>">
  <a href="<DRIVE_LINK>">Open the video on Google Drive (committee access only)</a>
  ```

- Invariants:
  - The **same Drive URL** appears in both the `<meta>` `content` and the `<a href>` — they must never diverge.
  - The URL is **byte-identical** to what the user gave (don't rewrite `/view?usp=drive_link`, don't convert to a `uc?export` form) — it's a human bookmark, not a hotlink.
  - One file per talk folder, always named exactly `video-file.html`.

## Workflow

1. **Pair each link to its folder.** Match the user's talk reference to a folder under `deliverables/talks/`. If the mapping is ambiguous, confirm before writing.
2. **Write `video-file.html`** into the folder using the two-line shape above, substituting the Drive link verbatim in both places.
3. **Verify.** Confirm the file exists at `<folder>/video-file.html` and that the `<meta>` and `<a>` URLs match each other and the input. Repeat for every (folder, link) pair before reporting done.

## Conventions

- **Keep it minimal.** The single `<meta http-equiv="refresh">` line is what redirects; the `<a>` line exists only as a fallback for browsers that block meta-refresh or that show source (e.g. GitHub's file view). No `<html>/<head>/<body>` scaffolding, no styling — browsers tolerate the bare tags.
- **The recording stays out of the repo.** This skill never copies, uploads, or commits the `.mov`. When the repo is first put under git for publishing, a `.gitignore` rule like `*.mov` keeps the recordings local while these bookmarks ship. Mention it if the user is heading toward a push, but it's not part of writing the file.
- **Don't fabricate links.** A `video-file.html` with a wrong or invented Drive ID is worse than none. Only write what the user supplied.

## Related
- **How-to** — sibling talk skills `talk-youtube-metadata`, `talk-caption-polish`, `talk-caption-translate-zh` operate on the same talk folder.
- **Up** — [AGENTS.md](../../AGENTS.md)
