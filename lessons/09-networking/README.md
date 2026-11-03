# Lesson 09 — Linux networking

**Goal:** Learn basic network concepts and diagnose connectivity on systems you own or are authorized to administer.

## Key concepts
- IP address: address assigned to a network interface.
- Subnet: range of addresses sharing a network prefix.
- Default gateway: router used for destinations outside the local network.
- DNS: translates names such as example.com into addresses.
- TCP: reliable, connection-oriented transport.
- UDP: datagram transport with different trade-offs.

## Inspect your machine

```bash
ip addr
ip route
```

These show interface addresses and routing information. The output depends on your network.

## DNS and connectivity

```bash
getent hosts example.com
ping -c 4 example.com
```

Ping may be blocked by a network or host, so failure does not prove a website is down. DNS lookup and network reachability are separate problems.

## Listening ports

```bash
ss -tuln
```

This displays listening TCP/UDP sockets. Interpret it locally for system troubleshooting. Do not scan or probe networks you don't own or have permission to assess.

## A simple troubleshooting order
1. Is the interface up?
2. Does it have an address?
3. Is a default route present?
4. Can the system reach the gateway?
5. Does DNS resolve?
6. Is the destination service available?
7. Is a firewall or proxy involved?

## Exercises
- Find your interface address and default route.
- Resolve a domain name.
- Explain why ping can fail even when a website works.
- Write down a troubleshooting sequence for “internet not working.”

References: `man ip`, `man ss`, [Ubuntu networking](https://ubuntu.com/server/docs/network-configuration).
