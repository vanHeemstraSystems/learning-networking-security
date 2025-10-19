# Nmap - Network Exploration and Security Auditing

## 📖 Overview

**Nmap** (Network Mapper) is a free and open-source network scanner used for network discovery and security auditing. It’s one of the most popular and essential tools in a security professional’s toolkit.

### What Nmap Does

- Discovers hosts and services on a network
- Identifies operating systems and software versions
- Detects security vulnerabilities
- Maps network topology
- Monitors host or service uptime

### Key Features

- **Port Scanning**: Identifies open ports on target systems
- **Service Detection**: Determines what services are running on open ports
- **OS Fingerprinting**: Identifies the operating system of target hosts
- **Script Engine (NSE)**: Extensible with custom scripts for vulnerability detection
- **Performance**: Fast and efficient with multi-threaded scanning
- **Output Options**: Multiple output formats (XML, JSON, plain text)

## 🔧 Installation

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install nmap -y
```

### Linux (RHEL/CentOS/Fedora)

```bash
sudo yum install nmap -y
# or
sudo dnf install nmap -y
```

### macOS

```bash
# Using Homebrew
brew install nmap

# Or download from official website
# Visit: https://nmap.org/download.html
```

### Windows

1. Download the installer from: https://nmap.org/download.html
1. Run the `.exe` installer
1. Follow the installation wizard
1. Optionally install Zenmap (GUI version)

### Verify Installation

```bash
nmap --version
```

## 💻 Basic Usage

### Syntax

```bash
nmap [Scan Type(s)] [Options] {target specification}
```

### Simple Scans

#### Scan a Single Host

```bash
nmap 192.168.1.1
```

#### Scan Multiple Hosts

```bash
nmap 192.168.1.1 192.168.1.2 192.168.1.3
```

#### Scan an IP Range

```bash
nmap 192.168.1.1-20
```

#### Scan a Subnet (CIDR)

```bash
nmap 192.168.1.0/24
```

#### Scan from a List of Targets

```bash
nmap -iL targets.txt
```

## 🎯 Common Scan Types

### TCP Connect Scan (Default)

```bash
nmap -sT 192.168.1.1
```

- Completes TCP three-way handshake
- Most reliable but easily detected

### SYN Scan (Stealth Scan)

```bash
sudo nmap -sS 192.168.1.1
```

- Doesn’t complete TCP handshake
- Faster and stealthier
- Requires root/administrator privileges

### UDP Scan

```bash
sudo nmap -sU 192.168.1.1
```

- Scans UDP ports
- Slower than TCP scans
- Important for DNS, DHCP, SNMP services

### Comprehensive Scan

```bash
sudo nmap -sS -sU -T4 -A -v 192.168.1.1
```

- Combines TCP and UDP scanning
- OS detection, version detection, script scanning
- Aggressive timing template

## 🔍 Service and Version Detection

### Detect Service Versions

```bash
nmap -sV 192.168.1.1
```

### Aggressive Service Detection

```bash
nmap -sV --version-intensity 9 192.168.1.1
```

### OS Detection

```bash
sudo nmap -O 192.168.1.1
```

### Comprehensive Detection

```bash
sudo nmap -A 192.168.1.1
```

- Enables OS detection, version detection, script scanning, and traceroute

## ⚡ Timing and Performance

### Timing Templates (T0-T5)

```bash
nmap -T0 192.168.1.1  # Paranoid (IDS evasion)
nmap -T1 192.168.1.1  # Sneaky (IDS evasion)
nmap -T2 192.168.1.1  # Polite (slows down to use less bandwidth)
nmap -T3 192.168.1.1  # Normal (default)
nmap -T4 192.168.1.1  # Aggressive (fast networks)
nmap -T5 192.168.1.1  # Insane (very fast networks)
```

### Control Parallelism

```bash
nmap --min-parallelism 10 --max-parallelism 100 192.168.1.1
```

## 📝 Output Options

### Save Results in Multiple Formats

```bash
nmap -oN output.txt 192.168.1.1      # Normal output
nmap -oX output.xml 192.168.1.1      # XML output
nmap -oG output.gnmap 192.168.1.1    # Grepable output
nmap -oA output 192.168.1.1          # All formats
```

## 🔐 NSE Scripts (Nmap Scripting Engine)

### List Available Scripts

```bash
ls /usr/share/nmap/scripts/
```

### Run Default Scripts

```bash
nmap -sC 192.168.1.1
```

### Run Specific Script

```bash
nmap --script=http-enum 192.168.1.1
```

### Run Multiple Scripts

```bash
nmap --script=http-enum,http-headers,http-methods 192.168.1.1
```

### Vulnerability Scanning

```bash
nmap --script=vuln 192.168.1.1
```

### Common Script Categories

```bash
nmap --script=auth 192.168.1.1       # Authentication scripts
nmap --script=broadcast 192.168.1.1  # Network broadcast discovery
nmap --script=discovery 192.168.1.1  # Host and service discovery
nmap --script=dos 192.168.1.1        # DoS detection
nmap --script=exploit 192.168.1.1    # Exploitation scripts
nmap --script=safe 192.168.1.1       # Safe scripts (non-intrusive)
```

## 🎓 Practical Examples

### Web Server Enumeration

```bash
nmap -p 80,443 --script=http-enum,http-headers,http-methods,http-title 192.168.1.1
```

### Database Server Scan

```bash
nmap -p 1433,3306,5432 --script=mysql-info,ms-sql-info,pgsql-brute 192.168.1.1
```

### SMB/Windows Enumeration

```bash
nmap -p 445 --script=smb-os-discovery,smb-protocols,smb-security-mode 192.168.1.1
```

### SSH Security Audit

```bash
nmap -p 22 --script=ssh-auth-methods,ssh-hostkey,ssh2-enum-algos 192.168.1.1
```

### Find All Live Hosts (Ping Sweep)

```bash
nmap -sn 192.168.1.0/24
```

### Quick Scan (Top 100 Ports)

```bash
nmap -F 192.168.1.1
```

### Scan Specific Ports

```bash
nmap -p 80,443,8080 192.168.1.1
nmap -p 1-65535 192.168.1.1  # All ports
```

## 🛡️ Firewall and IDS Evasion

### Fragment Packets

```bash
nmap -f 192.168.1.1
```

### Use Decoy Addresses

```bash
nmap -D RND:10 192.168.1.1
```

### Spoof Source Address

```bash
sudo nmap -S 192.168.1.100 192.168.1.1
```

### Randomize Host Order

```bash
nmap --randomize-hosts 192.168.1.0/24
```

## 📚 Learning Resources

### Official Documentation

- [Nmap Official Documentation](https://nmap.org/docs.html)
- [Nmap Reference Guide](https://nmap.org/book/man.html)
- [NSE Script Documentation](https://nmap.org/nsedoc/)

### Books

- “Nmap Network Scanning” by Gordon “Fyodor” Lyon (creator of Nmap)
- “Nmap 6: Network Exploration and Security Auditing Cookbook”

### Online Resources

- [Nmap Tutorial](https://nmap.org/book/toc.html)
- [HackerSploit Nmap Tutorials](https://www.youtube.com/hacksploit)
- [TryHackMe Nmap Room](https://tryhackme.com/room/furthernmap)

## 💡 Best Practices

### 1. Always Get Permission

```bash
# Only scan networks you own or have written permission to test
```

### 2. Start with Non-Intrusive Scans

```bash
# Begin with ping scans and basic port scans
nmap -sn 192.168.1.0/24
```

### 3. Document Your Scans

```bash
# Always save output for later analysis
nmap -oA scan_results_$(date +%Y%m%d) 192.168.1.1
```

### 4. Use Appropriate Timing

```bash
# Don't use T5 (insane) on production networks
# T3 or T4 is usually appropriate
nmap -T4 192.168.1.1
```

### 5. Combine Multiple Techniques

```bash
# Use multiple scan types for comprehensive results
sudo nmap -sS -sU -A -p- --script=vuln -oA full_scan 192.168.1.1
```

## ⚠️ Common Errors and Solutions

### Error: “You requested a scan type which requires root privileges”

**Solution**: Use `sudo` for SYN scans, OS detection, and some NSE scripts

```bash
sudo nmap -sS 192.168.1.1
```

### Error: “Failed to resolve target”

**Solution**: Check DNS resolution or use IP address directly

```bash
nmap -n 192.168.1.1  # Skip DNS resolution
```

### Slow Scans

**Solution**: Adjust timing template and reduce port range

```bash
nmap -T4 -F 192.168.1.1  # Fast scan, top 100 ports
```

## 🔒 Security and Ethics

### Legal Considerations

- **Authorization Required**: Always obtain written permission before scanning
- **Legal Consequences**: Unauthorized scanning may violate Computer Fraud and Abuse Act (CFAA) or similar laws
- **Network Impact**: Aggressive scans can disrupt services

### Responsible Use

- ✅ Scan your own networks and systems
- ✅ Use for authorized penetration testing
- ✅ Educational purposes in lab environments
- ❌ Never scan networks without permission
- ❌ Don’t use results maliciously
- ❌ Avoid scanning critical infrastructure

## 🎯 Practice Labs

### Safe Practice Environments

- [Metasploitable](https://www.metasploit.com/) - Vulnerable VM for practice
- [HackTheBox](https://www.hackthebox.com/) - Online penetration testing labs
- [TryHackMe](https://tryhackme.com/) - Guided cybersecurity training
- [VulnHub](https://www.vulnhub.com/) - Vulnerable VMs for practice

### Create Your Own Lab

```bash
# Set up virtual machines with VMware/VirtualBox
# Scan your own isolated network
```

## 📊 Sample Output Analysis

### Understanding Nmap Output

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.9p1 Debian 10+deb10u2
80/tcp   open  http    Apache httpd 2.4.38 ((Debian))
443/tcp  open  ssl/http Apache httpd 2.4.38 ((Debian))
3306/tcp closed mysql
```

- **PORT**: Port number and protocol (TCP/UDP)
- **STATE**: Open, closed, filtered
- **SERVICE**: Service name
- **VERSION**: Detailed version information

## 🔍 Advanced Topics to Explore

1. **Custom NSE Scripts**: Write your own scripts in Lua
1. **Nmap API**: Integrate Nmap into Python/other languages
1. **IPv6 Scanning**: Scan IPv6 networks
1. **Network Inventory**: Use for asset management
1. **Continuous Monitoring**: Automate regular scans

## 📝 Quick Reference Cheat Sheet

```bash
# Basic scans
nmap 192.168.1.1                    # Basic scan
nmap -p 80,443 192.168.1.1         # Specific ports
nmap -p- 192.168.1.1               # All ports
nmap 192.168.1.0/24                # Subnet scan

# Scan types
nmap -sS 192.168.1.1               # SYN scan
nmap -sT 192.168.1.1               # TCP connect
nmap -sU 192.168.1.1               # UDP scan
nmap -sn 192.168.1.0/24            # Ping sweep

# Detection
nmap -sV 192.168.1.1               # Service version
nmap -O 192.168.1.1                # OS detection
nmap -A 192.168.1.1                # Aggressive scan

# Scripts
nmap --script=default 192.168.1.1  # Default scripts
nmap --script=vuln 192.168.1.1     # Vulnerability scan

# Output
nmap -oN out.txt 192.168.1.1       # Normal output
nmap -oX out.xml 192.168.1.1       # XML output
nmap -oA out 192.168.1.1           # All formats

# Timing
nmap -T4 192.168.1.1               # Aggressive timing
nmap -T2 192.168.1.1               # Polite timing
```

-----

**Last Updated**: October 2025  
**Tool Version**: Nmap 7.94+  
**License**: Nmap is licensed under GPL v2
