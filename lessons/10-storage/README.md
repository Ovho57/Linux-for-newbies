# Lesson 10 — Storage and filesystems

**Goal:** Understand disks, partitions, filesystems, and mount points.

## Important distinctions
- **Disk/device:** storage hardware or virtual device.
- **Partition:** a region defined on a disk.
- **Filesystem:** structure used to store and retrieve files.
- **Mount point:** directory where a filesystem is made accessible.

Linux represents devices with paths such as `/dev/sda` or `/dev/nvme0n1`; names vary and can change. Never assume a device name refers to the same disk on every machine.

## Inspect storage (read-only commands)

```bash
lsblk
df -h
du -sh ~/Downloads
```

- `lsblk`: block devices and partitions.
- `df -h`: filesystem space usage.
- `du -sh`: space used by a directory.

## Mounting
Mounting connects a filesystem to a directory in the tree. The system may mount filesystems automatically at boot. `/etc/fstab` describes persistent mounts on many Linux systems.

Disk formatting, partition editing, and mount configuration can destroy data or prevent booting. Practise those topics in a VM using disposable virtual disks only; verify the target device and back up data before any real change.

## Exercises
1. Use `lsblk` and explain the output.
2. Compare `df -h` with `du -sh`.
3. Explain filesystem vs partition vs mount point.

References: `man lsblk`, `man df`, `man mount`.
