---
name: redirect-bookmark
description: >-
  Create a tiny committed HTML meta-refresh redirect file that points to an
  external URL — a durable in-repo bookmark to a resource kept outside the repo
  (a large media file, a cloud/Drive link, an access-restricted asset). Use
  whenever the user hands over an external/Drive/cloud URL and wants it
  bookmarked in a folder, says a file is "stored separately"/"in Drive"/"not in
  the repo", asks to link or reference an external resource from a folder, or
  asks for an HTML bookmark or a redirect/bookmark HTML stub — even across
  several at once.
---

# Bookmarking an external resource with a redirect file

Some resources are deliberately kept outside the repo — multi-gigabyte media, files behind access control, links that live in someone else's cloud. So a tiny committed HTML file redirects whoever opens it to the real resource: a durable bookmark that survives in the repo without shipping the resource itself.

## Input

- A target folder to write into, and the external URL to point at. Pair them up; if only one is given, ask — don't guess which resource maps to which folder.
- Filename: default `redirect.html`. A project may define the exact name and folder via its own reference doc.
- When several (folder, URL) pairs are given at once, treat each as one pair and write one file per folder.

## Output

- An HTML file (named and placed per the project's convention; default `redirect.html`) containing a meta-refresh redirect plus a visible clickable fallback link:

  ```html
  <meta http-equiv="refresh" content="0; url=<URL>">
  <a href="<URL>">Open the linked resource</a>
  ```

  A project may specify its own fallback link text (e.g. "committee access only").

- Invariants:
  - The **same URL** appears in both the `<meta>` `content` and the `<a href>` — they must never diverge.
  - The URL is **byte-identical** to what the user gave (don't rewrite `/view?usp=drive_link`, don't convert to a `uc?export` form) — it's a human bookmark, not a hotlink.
  - One file per folder, named exactly per the resolved filename.

## Workflow

1. **Pair each URL to its folder.** Match the user's reference to a target folder. If the mapping is ambiguous, confirm before writing.
2. **Write the file** into the folder using the two-line shape above, substituting the URL verbatim in both places.
3. **Verify.** Confirm the file exists at `<folder>/<filename>` and that the `<meta>` and `<a>` URLs match each other and the input. Repeat for every (folder, URL) pair before reporting done.

## Conventions

- **Keep it minimal.** The single `<meta http-equiv="refresh">` line is what redirects; the `<a>` line exists only as a fallback for browsers that block meta-refresh or that show source (e.g. GitHub's file view). No `<html>/<head>/<body>` scaffolding, no styling — browsers tolerate the bare tags.
- **The linked resource stays out of the repo.** This skill only writes the pointer; it never copies, uploads, or commits the resource itself.
- **Don't fabricate links.** A redirect file with a wrong or invented URL is worse than none. Only write what the user supplied.
