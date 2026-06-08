# backup-tool — brain dump (raw, unsorted)

ok so backup-tool is a little CLI we use to snapshot the postgres volumes nightly.
the whole point is: one command, restorable snapshots, no babysitting.

how the incremental thing works: first run is a full snapshot, after that each run
only stores the blocks that changed since the last snapshot, and a restore walks the
chain back to the last full. that's why deleting an old full breaks every incremental
that depends on it — they're not standalone.

config — it reads these env vars:
- BACKUP_DEST   (s3 bucket url, required)
- BACKUP_KEY    (encryption key, required)
- RETAIN_DAYS   (how long to keep snapshots, default 30)
- PG_DSN        (postgres connection string, required)

to restore: 1) stop the app, 2) run `backup-tool restore --snapshot <id> --dry-run`
and read the plan, 3) run it for real without --dry-run, 4) verify row counts, 5) start
the app again. always dry-run first or you can clobber a live volume.

NOTE for agents working in here: never run `restore` for real without doing the
--dry-run pass first and never delete a full snapshot to "save space". those are hard
rules.

commands: `backup-tool snapshot`, `backup-tool list`, `backup-tool restore`, `backup-tool prune`.
