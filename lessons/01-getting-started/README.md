# Lesson 01 — Getting started safely

**Level:** Beginner  
**Goal:** Choose a practice environment and learn how to get help.

## Choose your setup

### Option A: WSL on Windows
Windows Subsystem for Linux lets you run a Linux environment on Windows without setting up a traditional dual-boot. It is a convenient choice for command-line learning.

Guide: [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install)

### Option B: Virtual machine
A VM runs a guest operating system inside your existing computer. VirtualBox is one option. It is useful for learning system administration because you can take snapshots and restore a machine after experiments.

Guide: [VirtualBox](https://www.virtualbox.org/)

### Option C: A spare computer
You can install Linux on hardware you own, but installation can erase data or change boot settings. Back up important files and carefully check which disk is selected. Beginners should start with WSL or a VM.

## First commands

Open your Linux terminal and try:

```bash
whoami
pwd
uname -a
```

- `whoami` prints the current username.
- `pwd` prints the current working directory.
- `uname -a` shows kernel/system information.

Your output will differ depending on the machine.

## Getting help

Linux commands often have built-in manuals:

```bash
man pwd
pwd --help
```

Not every program supports `--help`, but many do. In a manual page:
- Press `q` to quit.
- Use arrow keys or Page Up/Page Down to move.
- Search with `/` followed by a word, then Enter.

## Understand your prompt

A prompt may look something like:

```text
student@linuxbox:~$
```

- `student`: username
- `linuxbox`: computer name
- `~`: shorthand for your home directory
- `$`: commonly indicates a regular user (root prompts often use `#`)

The exact prompt can be customized.

## Practice
1. Run `whoami`.
2. Run `pwd`.
3. Read the manual for `pwd`.
4. Write down your distribution and shell if you know them.

**Safety:** Do not use administrator privileges just because a tutorial does. First understand why they are needed.
