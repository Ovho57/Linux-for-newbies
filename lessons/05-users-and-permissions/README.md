# Lesson 05 — Users and permissions

**Goal:** Understand ownership and access control.

Linux supports multiple users. Permissions help prevent one user or process from changing another user's files or the operating system.

## Inspect ownership

```bash
whoami
id
ls -l
```

A listing such as `-rw-r--r--` describes file type and permissions, followed by owner and group.

## Read permission bits

There are three groups:
- owner (user)
- group
- others

Each group can have:
- `r` read
- `w` write
- `x` execute (for directories, execute means traverse/search)

Example: `rw-r-----` means owner can read/write, group can read, others have no access.

## Numeric permissions

`r=4`, `w=2`, `x=1`; add values per group.

- 7 = rwx
- 6 = rw-
- 5 = r-x
- 4 = r--

Example: `chmod 640 report.txt` sets owner read/write, group read, others none.

```bash
chmod 600 private.txt
chmod u+x script.sh
```

Use `chmod` carefully. Avoid broad permissions such as `chmod -R 777`; they usually create security problems.

## Ownership and sudo

`chown` changes ownership and usually requires administrator privileges. `sudo` runs a command with elevated permissions when authorized.

```bash
sudo command
```

Only use sudo when needed and when you understand the command. Never paste unknown commands into a sudo prompt.

## Exercises
1. Create a file and inspect it with `ls -l`.
2. Set it to `600`, then inspect again.
3. Explain why `777` is usually a poor default.
4. Describe the difference between a user and a group.

Further reading: [Ubuntu permissions guide](https://help.ubuntu.com/community/FilePermissions), `man chmod`, `man chown`.
