# Linux for Newbies — From Your First Command to Expert

Linux powers servers, cloud platforms, supercomputers, development machines, and many devices you use every day. This guide is for people who want to understand it properly—not just memorize commands.

You don't need previous Linux or programming experience. Start where you are, learn at your own pace, and practise.

## First: where have you reached in Linux?

Choose the statement that sounds most like you:

| Your experience | Start here |
|---|---|
| I've never used Linux and don't know what a terminal is. | [Lesson 00 — Linux basics](lessons/00-linux-basics/README.md) |
| I know what Linux is, but need to install or try it. | [Lesson 01 — Getting started](lessons/01-getting-started/README.md) |
| I can open a terminal, but commands are confusing. | [Lesson 02 — Terminal essentials](lessons/02-terminal/README.md) |
| I can move around folders and use basic commands. | [Lesson 03 — Files and directories](lessons/03-files-and-directories/README.md) |
| I know basic commands and want to manage a Linux system. | [Roadmap: intermediate topics](ROADMAP.md#intermediate) |
| I already administer Linux and want deeper internals and automation. | [Roadmap: advanced and expert](ROADMAP.md#advanced-and-expert) |

**Not sure?** Begin with Lesson 00. You can always skip ahead later.

## Lessons

1. [Linux basics](lessons/00-linux-basics/README.md)
2. [Getting started and setup](lessons/01-getting-started/README.md)
3. [Terminal essentials](lessons/02-terminal/README.md)
4. [Files and directories](lessons/03-files-and-directories/README.md)
5. [Reading and editing files](lessons/04-reading-and-editing/README.md)
6. [Users and permissions](lessons/05-users-and-permissions/README.md)
7. [Package management](lessons/06-package-management/README.md)
8. [Processes and jobs](lessons/07-processes-and-jobs/README.md)
9. [Bash scripting](lessons/08-bash-scripting/README.md)
10. [Networking](lessons/09-networking/README.md)
11. [Storage and filesystems](lessons/10-storage/README.md)
12. [Services and systemd](lessons/11-services-systemd/README.md)
13. [Logs and troubleshooting](lessons/12-logs-troubleshooting/README.md)
14. [Linux security](lessons/13-linux-security/README.md)
15. [Administration and automation](lessons/14-admin-automation/README.md)
16. [Kernel and system internals](lessons/15-kernel-internals/README.md)
17. [Expert practice projects](lessons/16-expert-projects/README.md)

## How to study

- Read one lesson, then run the examples yourself.
- Make small changes and predict the result before pressing Enter.
- Complete the exercises without immediately checking solutions.
- Keep a notebook of commands and concepts.
- Use a virtual machine or disposable environment for system-level experiments.
- If something breaks, learn to read the error message instead of blindly copying another command.

## Safety note

Commands can delete files, alter permissions, stop services, or damage a system. Don't run commands you don't understand, especially when they use `sudo`, `rm`, disk tools, or recursive options. Back up important files and practise system changes in a virtual machine. Security exercises should only target systems you own or have explicit permission to test.

## Useful learning links

- [Linux Journey](https://linuxjourney.com/) — friendly interactive beginner lessons.
- [The Linux Documentation Project](https://tldp.org/) — guides and documentation.
- [Ubuntu Help](https://help.ubuntu.com/) — Ubuntu user and system documentation.
- [Debian Documentation](https://www.debian.org/doc/) — manuals and official guides.
- [Arch Wiki](https://wiki.archlinux.org/) — detailed technical reference.
- [GNU Bash manual](https://www.gnu.org/software/bash/manual/) — Bash reference.
- [Linux man-pages](https://www.kernel.org/doc/man-pages/) — Linux command and system interface documentation.
- [OverTheWire Bandit](https://overthewire.org/wargames/bandit/) — terminal puzzle game in a controlled environment.
- [WSL documentation](https://learn.microsoft.com/en-us/windows/wsl/) — Linux environment on Windows.
- [VirtualBox](https://www.virtualbox.org/) — virtual machines for safe practice.

## What you'll learn

You'll build confidence with the shell, filesystem, permissions, software installation, processes, scripting, networking, storage, services, logs, security fundamentals, troubleshooting, administration, and system internals.

Becoming an expert takes hands-on experience. This repository is a roadmap and practice resource, not a shortcut.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) if you want to improve a lesson or add examples.

**Start learning:** [Lesson 00 — Linux basics](lessons/00-linux-basics/README.md)
