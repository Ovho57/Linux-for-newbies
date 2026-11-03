# Lesson 00 — Linux basics

**Level:** Absolute beginner  
**Goal:** Understand what Linux is and the pieces that make a Linux computer work.

## 1. What is Linux?

Strictly speaking, **Linux is the kernel**: the core program that manages hardware and provides services to other programs. A usable Linux operating system usually combines the Linux kernel with utilities, libraries, a package manager, and applications. This complete combination is often called a **Linux distribution** (or distro).

Popular distributions include:
- Ubuntu — widely used for desktops, servers, and learning.
- Debian — known for stability and a large package collection.
- Fedora — modern Linux technologies and developer-friendly tools.
- Linux Mint — desktop-oriented and approachable for new users.
- Arch Linux — flexible and hands-on; better once you understand fundamentals.

Different distributions may use different installers, package managers, defaults, and release schedules. The core terminal concepts transfer between them.

## 2. Kernel, shell, and applications

A simplified view:

```text
You
 ├─ Desktop / applications
 └─ Shell (terminal commands)
       ↓
     Linux kernel
       ↓
 CPU • memory • disks • network • devices
```

- **Kernel:** manages CPU time, memory, devices, and processes.
- **Shell:** reads commands and starts programs. Bash is a common shell.
- **Terminal:** the application/window where you interact with a shell.
- **Desktop environment:** graphical interface such as GNOME or KDE Plasma.
- **Distribution:** a packaged operating system built around the Linux kernel.

A terminal is not Linux itself. It is one way to control the system.

## 3. Why learn Linux?

Linux is common in web hosting, cloud infrastructure, software development, networking, embedded devices, and automation. Learning it helps you understand how computers operate beyond the graphical interface.

## 4. Open-source basics

Much Linux software is open source: its source code can be inspected, modified, and redistributed under the applicable license. Open source does not automatically mean “no rules”; licenses still matter.

## 5. First vocabulary

| Word | Meaning |
|---|---|
| Distribution | Complete Linux operating system collection |
| Terminal | Text interface for entering commands |
| Shell | Program that interprets commands |
| Root | Administrator account |
| Home directory | Personal workspace for a user |
| Repository | Software collection used by package managers |
| Process | Running program |
| Filesystem | Organization of files and directories |

## Check your understanding
1. Is Linux the kernel or the entire desktop environment?
2. What is the difference between a terminal and a shell?
3. Name two Linux distributions.
4. Why might someone use Linux on a server?

## Mini exercise
Explain the difference between kernel, shell, terminal, and distribution in your own words. If you can explain it without memorizing the table, you're ready for the next lesson.

## Further reading
- [Linux Journey: What is Linux?](https://linuxjourney.com/lesson/what-is-linux)
- [Linux kernel website](https://www.kernel.org/)
- [Ubuntu](https://ubuntu.com/)
