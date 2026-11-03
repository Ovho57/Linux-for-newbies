# Lesson 03 — Files and directories

**Goal:** Navigate and manage files using the shell.

## The filesystem tree

Linux paths begin at the root directory, written `/`. Directories branch from there.

Common locations:
- `/`: filesystem root
- `/home`: users' home directories
- `/etc`: system configuration
- `/var`: changing data such as logs and caches
- `/tmp`: temporary files
- `/usr`: many programs and shared resources
- `/bin` and `/sbin`: command locations (layout can vary on modern systems)

Do not assume these folders are ordinary personal workspaces.

## Absolute and relative paths

- Absolute path: starts with `/`, e.g. `/home/alex/notes.txt`.
- Relative path: interpreted from your current directory, e.g. `notes.txt`.
- `.`: current directory.
- `..`: parent directory.
- `~`: home directory in Bash.

## Navigation

```bash
pwd
ls
ls -la
cd /tmp
cd ..
cd ~
```

`ls -la` includes hidden entries (names beginning with a dot) and detailed information.

## Create, copy, move, remove

Practise only in a directory you own:

```bash
mkdir linux-practice
cd linux-practice
touch first.txt
mkdir notes
cp first.txt notes/copy.txt
mv first.txt renamed.txt
```

- `mkdir`: create a directory.
- `touch`: create an empty file if it does not exist (or update its timestamp).
- `cp`: copy.
- `mv`: move or rename.
- `rmdir`: remove an empty directory.
- `rm`: remove files; it does not normally move them to a trash bin.

**Danger:** `rm` can permanently remove files. Avoid `rm -r`, `rm -f`, and especially combinations involving administrator privileges until you understand them. Always check your current directory and target first.

## Globbing

```bash
ls *.txt
```

The shell expands `*.txt` to matching filenames before running the command. It is not a regular expression.

## Exercises
1. Create a folder called `practice`.
2. Inside it, create `one.txt` and `two.txt`.
3. Copy `one.txt` to `backup.txt`.
4. Rename `two.txt` to `notes.txt`.
5. Use `pwd` and `ls -la` to inspect your work.

## Reference
- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/)
