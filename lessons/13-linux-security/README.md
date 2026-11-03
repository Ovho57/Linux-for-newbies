# Lesson 13 — Linux security fundamentals

**Goal:** Build defensive habits for machines you own or are authorized to administer.

## Core principles
- **Least privilege:** users and services should have only the access they need.
- **Updates:** install security updates from trusted sources.
- **Authentication:** protect accounts with strong, unique credentials and appropriate MFA where available.
- **Defense in depth:** combine account controls, updates, firewall rules, backups, and monitoring.
- **Backups:** test restoration; a backup that cannot be restored is not useful.
- **Reduce attack surface:** remove or disable unneeded software and services.

## Useful defensive checks

```bash
whoami
id
sudo -l
ss -tuln
systemctl --type=service --state=running
```

These help you understand your account privileges, listening sockets, and running services. Use them for your own system.

## SSH basics
SSH provides encrypted remote login. For server administration:
- Keep SSH software updated.
- Prefer key-based authentication when appropriately configured.
- Protect private keys and never share them.
- Restrict access to accounts that need it.
- Keep a recovery path before changing remote SSH settings.

Do not lock yourself out of a remote machine. Test configuration changes and maintain an authorized console or recovery option.

## Firewall
A firewall controls network traffic. Tools and defaults vary (for example, UFW on Ubuntu). Understand the policy and ensure you do not block legitimate administration access.

## Security practice boundaries
Only test systems you own or have explicit permission to assess. This course focuses on hardening, monitoring, and understanding defensive controls—not breaking into other people's systems.

## Exercises
1. Identify unnecessary services on a test VM.
2. Review account permissions.
3. Explain least privilege.
4. Make a backup and test restoring a file.

References: [Ubuntu security](https://ubuntu.com/security), [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks).
