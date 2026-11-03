# Lesson 12 — Logs and troubleshooting

**Goal:** Diagnose issues systematically rather than guessing.

## A repeatable approach
1. Describe the symptom precisely.
2. Identify what changed recently.
3. Check whether the problem affects one user, one application, or the whole system.
4. Gather evidence (status, logs, disk, memory, network).
5. Make one change at a time.
6. Verify the result and document what fixed it.

## Logs
Many system logs are available through journald:

```bash
journalctl -b
journalctl -p warning
journalctl --since "1 hour ago"
```

Traditional log files may also exist under `/var/log`. Access can be restricted.

## Resource checks

```bash
free -h
df -h
uptime
top
```

These help answer:
- Is memory under pressure?
- Is a filesystem full?
- Is the machine under heavy load?
- Which processes are consuming resources?

## Don't delete logs blindly
Logs are evidence. Removing them can hide the cause of a problem and may not free meaningful space. Find the source of excessive logging and use the distribution's log rotation tools.

## Practice scenario
A service refuses to start:
- Check `systemctl status`.
- Inspect its journal.
- Confirm configuration and permissions.
- Check whether required files or ports exist.
- Make one correction and verify.

Further reading: `man journalctl`, `man logrotate`.
