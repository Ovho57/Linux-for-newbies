# Lesson 15 — Kernel and system internals

**Goal:** Build a mental model of what happens below the command line.

## Kernel responsibilities
The Linux kernel handles:
- process scheduling,
- virtual memory,
- device drivers,
- filesystems,
- networking,
- system calls,
- security and access-control mechanisms.

Applications normally interact with the kernel through system calls and libraries rather than directly manipulating hardware.

## User space and kernel space
User-space programs run with restricted privileges. Kernel-space code has broad control over the machine. This separation is essential for stability and security.

## Inspect system information

```bash
uname -r
cat /proc/cpuinfo
cat /proc/meminfo
ls /sys
```

`/proc` and `/sys` expose information about processes and kernel/device state. Some files are virtual interfaces, not ordinary files stored on disk.

## System calls
A system call is a controlled entry point into the kernel. Examples include operations related to opening files, creating processes, and networking. Tools like `strace` can help observe system calls for programs you own or are debugging.

## Modules
Kernel modules extend kernel functionality, often for drivers or filesystem support. Loading or removing modules affects system behavior and may require administrator privileges. Learn this in a VM and consult your distribution's documentation.

## Further study
- [Linux kernel documentation](https://docs.kernel.org/)
- [The Linux Programming Interface](https://man7.org/tlpi/)
- `man proc`, `man sysfs`, `man strace`

## Challenge
Explain the path from a terminal command to a kernel action. Include shell parsing, process creation, system calls, and the kernel.
