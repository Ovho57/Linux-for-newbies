# Lesson 16 — Expert practice projects

These projects combine multiple lessons. Do them in a VM or on systems you own and are authorized to administer. Document what you did and why.

## Project 1: Personal Linux workstation checklist
- Identify distro, kernel, storage, memory, and network interfaces.
- List installed updates and enabled services.
- Review user accounts and permissions.
- Create a backup plan and test restoring a file.
- Write a short report with recommendations.

## Project 2: Bash system report
Build a script that:
- checks required commands,
- prints hostname and timestamp,
- reports filesystem and memory usage,
- handles failures,
- writes output to a report file,
- never prints secrets.

## Project 3: Local service lab
In a disposable VM:
- install a small local service from the distro repository,
- inspect its unit and logs,
- configure it to start when appropriate,
- verify access locally,
- document how to stop and remove it cleanly.

## Project 4: Troubleshooting notebook
Create five simulated issues (full test disk, stopped test service, incorrect file permission, DNS failure in a controlled environment, missing command). For each:
1. Record the symptom.
2. Gather evidence.
3. State your hypothesis.
4. Apply one fix.
5. Verify and explain the root cause.

## Project 5: Automated configuration
Use Ansible or another configuration-management tool to configure a disposable Linux VM. Make the process repeatable and explain idempotence.

## Project 6: Backup and restore
Back up a folder, verify the backup, remove a test copy, and restore it. Record the exact procedure and confirm checksums or file contents.

## Project write-up template
- Goal
- Environment and distro/version
- Requirements
- Commands and explanations
- Results
- Problems encountered
- How you verified the result
- Cleanup / rollback
- What you learned

## When can you call yourself advanced?
When you can explain system behavior, diagnose unfamiliar problems methodically, recover from mistakes, automate repeated work, and understand the trade-offs behind your decisions. Keep learning: Linux is broad and changes over time.
