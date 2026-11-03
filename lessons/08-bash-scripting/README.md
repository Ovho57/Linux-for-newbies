# Lesson 08 — Bash scripting

**Goal:** Turn repeated commands into readable, repeatable scripts.

## Your first script

Create `hello.sh`:

```bash
#!/usr/bin/env bash
set -u

name="${1:-Linux learner}"
printf 'Hello, %s!\n' "$name"
```

Run it:

```bash
bash hello.sh
bash hello.sh Sam
```

The shebang tells the system which interpreter to use when executing the script directly. `$1` is the first argument. `${1:-default}` supplies a fallback if it is unset or empty.

## Variables and quoting

```bash
course="Linux"
printf 'Welcome to %s\n' "$course"
```

Quote variable expansions unless you have a specific reason not to. Quoting prevents many accidental word-splitting and glob-expansion problems.

## Conditions and loops

```bash
if [[ -f "notes.txt" ]]; then
  echo "The file exists"
else
  echo "No notes file yet"
fi

for item in one two three; do
  printf '%s\n' "$item"
done
```

## Functions

```bash
greet() {
  printf 'Hi, %s\n' "$1"
}
greet "reader"
```

## Errors and debugging
- `bash -n script.sh` checks syntax without running the script.
- `bash -x script.sh` traces execution; avoid this if the script may print secrets.
- Check exit statuses and handle missing files or invalid input.
- `set -e` can help in some scripts but has edge cases; understand its behavior rather than treating it as complete error handling.

## Mini project
Write a script that:
1. Accepts a directory path.
2. Checks that it exists and is a directory.
3. Counts regular files in it.
4. Prints a clear result.
5. Handles a missing argument.

Reference: [GNU Bash manual](https://www.gnu.org/software/bash/manual/).
