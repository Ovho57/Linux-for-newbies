# Lesson 11 — Services and systemd

**Goal:** Learn how Linux starts and supervises background services.

A service is a program that runs in the background to provide functionality—such as networking, logging, or a web server. Many modern Linux distributions use systemd as the init system and service manager.

## Inspect systemd

```bash
systemctl
systemctl --type=service
systemctl status ssh
```

The service name may differ by distribution. If a service isn't installed, the command will report that it cannot find it.

## Common actions
- `start`: start a service now.
- `stop`: stop it now.
- `restart`: stop and start.
- `enable`: configure it to start at boot.
- `disable`: remove automatic startup.

These are different: starting a service does not necessarily enable it at boot.

## Logs

```bash
journalctl -u service-name
journalctl -u service-name --since today
```

Check logs before guessing why a service failed.

## Service configuration
Unit files define service behavior and dependencies. System-provided units and administrator overrides may live in different directories. Read the relevant documentation before editing units.

## Practice
In a VM, inspect a familiar service, identify whether it is active and enabled, and read its recent logs. Do not stop critical services on your everyday computer.

References: [systemd documentation](https://www.freedesktop.org/wiki/Software/systemd/), `man systemctl`.
