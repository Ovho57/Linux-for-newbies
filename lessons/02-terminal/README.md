# Lesson 02 — Terminal essentials

**Goal:** Understand how commands are entered and how arguments work.

## Command anatomy

```bash
ls -l /home
```

- `ls`: command/program
- `-l`: option (long listing)
- `/home`: argument (the target path)

Spaces separate words. If a filename contains spaces, quote it:

```bash
ls "My Projects"
```

Single quotes preserve text literally; double quotes allow certain shell expansions.

## Useful commands

```bash
date       # show date/time
cal        # calendar (may not be installed)
hostname   # computer name
clear      # clear terminal display
echo hello
```

A comment begins with `#` in a shell script. In an interactive command, everything after an unquoted `#` is usually treated as a comment.

## Command history and completion
- Press Up/Down to browse recent commands.
- Press Tab to complete a command or path.
- Use Ctrl+C to interrupt a foreground command (not to undo completed changes).

## Exit status

Programs usually return an exit status: `0` conventionally means success; nonzero often indicates an error.

```bash
true
echo $?
false
echo $?
```

`$?` is the exit status of the most recently executed command. Run the echo immediately after the command you want to inspect.

## Common mistakes
- Forgetting quotes around a path containing spaces.
- Typing a command into the wrong environment (PowerShell vs Bash).
- Assuming every Linux distribution has exactly the same commands.
- Copying a command without reading its options.

## Exercises
1. Display today's date.
2. Print the text `I am learning Linux`.
3. Run `false`, then inspect its exit status.
4. Use Tab completion to finish a path.

## Further reading
- [Bash manual](https://www.gnu.org/software/bash/manual/)
- [Linux Journey: Command line](https://linuxjourney.com/)
