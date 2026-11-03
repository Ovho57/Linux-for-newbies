# Lesson 07 — Processes and jobs

**Goal:** Understand running programs and how to inspect them.

A process is a running instance of a program. Linux assigns each process a process ID (PID).

## Inspect processes

```bash
ps
ps aux
top
```

- `ps` displays process information.
- `ps aux` is a common detailed listing (syntax is from procps).
- `top` provides a live process view; press `q` to quit.

## Process relationships
Processes can start other processes. The parent process ID (PPID) identifies a process's parent. The system tracks resource usage such as CPU and memory.

## Signals

`kill` sends a signal to a process; it does not always mean “terminate immediately.”

```bash
kill PID
kill -TERM PID
```

Use only PIDs for processes you own or are authorized to manage. SIGTERM asks a process to stop cleanly. SIGKILL (`kill -9`) cannot be caught or handled and should be a last resort because cleanup may not happen.

## Foreground and background
In a shell, `command &` starts a job in the background. `jobs` lists shell jobs; `fg` brings a job forward. These are shell job controls, not system-wide process managers.

## Exercises
1. Run `sleep 60` in the foreground and stop it with Ctrl+C.
2. Start `sleep 60 &` and inspect jobs.
3. Use `ps` to find a process.
4. Explain why force-killing should not be the first choice.

Reference: `man ps`, `man kill`, `man top`.
