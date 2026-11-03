# Lesson 14 — Administration and automation

**Goal:** Make routine administration consistent, documented, and repeatable.

## Admin habits
- Keep an inventory of machines and their purpose.
- Track configuration changes.
- Schedule maintenance and backups.
- Monitor disk, memory, CPU, and service health.
- Document recovery procedures.
- Avoid manual changes that cannot be reproduced.

## Cron
Cron schedules commands on many Linux systems. User and system crontabs have different formats.

```bash
crontab -l
crontab -e
```

A cron schedule can be easy to misread. Verify the schedule and command path, redirect logs intentionally, and consider environment differences (cron often has a minimal PATH).

## Backups
A basic backup plan should specify:
- what data matters,
- where copies are stored,
- how often backups run,
- how long they are retained,
- who can access them,
- how restoration is tested.

Keep at least one backup separate from the machine being backed up.

## Configuration management
Tools such as Ansible help apply configuration consistently across systems. Start by learning inventory, variables, tasks, idempotence, and safe check/dry-run modes.

- [Ansible documentation](https://docs.ansible.com/)
- [systemd timers](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html)

## Mini project
Create a script that reports hostname, date, disk usage, and memory usage. Save the report to a timestamped file in your home directory. Handle errors and avoid collecting sensitive information unnecessarily.
