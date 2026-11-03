# Lesson 06 — Package management

**Goal:** Install, update, and remove software using your distribution's package manager.

A package manager downloads software from configured repositories, checks package metadata, tracks installed files, and resolves dependencies. Use the manager instead of downloading random executables whenever possible.

## Debian and Ubuntu: APT

```bash
sudo apt update
apt list --installed
apt search package-name
sudo apt install package-name
sudo apt remove package-name
```

Important distinction:
- `apt update` refreshes the local package index.
- `apt upgrade` installs available upgrades.
- `apt install` installs packages.

Review what the package manager plans to do before confirming.

## Fedora: DNF

```bash
sudo dnf check-update
sudo dnf search package-name
sudo dnf install package-name
sudo dnf remove package-name
```

## Arch: Pacman

```bash
sudo pacman -Syu
sudo pacman -Ss package-name
sudo pacman -S package-name
sudo pacman -R package-name
```

Commands vary by distribution. Do not mix package-manager instructions from unrelated distros.

## Repositories and trust
Repositories are software sources. Prefer official distribution repositories and trusted vendor sources. Avoid adding repositories or signing keys without checking who controls them and why they are needed.

## Exercises
1. Identify your distro and package manager.
2. Search for a harmless utility.
3. Inspect its package information.
4. Explain update vs upgrade.

References: [Ubuntu APT](https://ubuntu.com/server/docs/package-management), [Fedora DNF](https://docs.fedoraproject.org/), [Arch package management](https://wiki.archlinux.org/title/Pacman).
