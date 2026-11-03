# Lesson 04 — Reading and editing files

**Goal:** Inspect text files and make changes safely.

## Read files

```bash
cat file.txt
less file.txt
head file.txt
tail file.txt
tail -n 30 file.txt
```

- `cat` prints the whole file.
- `less` lets you scroll through a file.
- `head` shows the beginning.
- `tail` shows the end; `tail -f` follows new lines as they arrive (useful for logs).

## Search text

```bash
grep "error" app.log
grep -n "error" app.log
grep -i "warning" app.log
```

`grep` searches text. `-n` displays line numbers; `-i` ignores case.

## Redirection and pipes

```bash
echo "hello" > hello.txt
echo "another line" >> hello.txt
cat hello.txt | grep hello
```

- `>` redirects output and **overwrites** a file.
- `>>` appends.
- `|` sends one program's output to another program's input.

Be cautious with `>`: an existing file can be truncated immediately.

## Editors
- Nano is approachable: `nano notes.txt`
- Vim is powerful and modal: learn its basic modes before editing important files.

In Nano, Ctrl+O saves, Enter confirms the filename, and Ctrl+X exits.

## Exercises
1. Create a file with three lines.
2. Use `head`, `tail`, and `grep` to inspect it.
3. Append a line, then verify the file.
4. Explain the difference between `>` and `>>`.

Further reading: [GNU grep](https://www.gnu.org/software/grep/manual/), [GNU sed](https://www.gnu.org/software/sed/manual/).
