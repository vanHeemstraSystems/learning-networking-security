# Security Testing Lab - Quick Start Guide

## 📋 Overview

This Docker-based security lab provides a **completely isolated** environment for practicing network security testing. All targets and tools run in containers on an internal network, keeping your actual network safe.

## 🚀 Quick Start

### Prerequisites

- Docker installed (version 20.10+)
- Docker Compose installed
- At least 8GB RAM available
- 20GB free disk space

### Setup in 3 Steps

```bash
# 1. Make the lab manager executable
chmod +x lab-manager.sh

# 2. Start the lab
./lab-manager.sh start

# 3. Wait for initialization (about 30 seconds)
# Then access the Kali attacker container
./lab-manager.sh kali
```

## 🎯 Available Targets

### Web Applications (Browser Access from Host)

|Application|URL                  |Credentials     |Description              |
|-----------|---------------------|----------------|-------------------------|
|DVWA       |http://localhost:8001|admin / password|SQL injection, XSS, etc. |
|WebGoat    |http://localhost:8002|Register first  |OWASP training platform  |
|bWAPP      |http://localhost:8003|bee / bug       |100+ vulnerabilities     |
|Juice Shop |http://localhost:8004|Register first  |Modern web app challenges|

### Network Services (Access from Kali Container)

|Service   |IP Address |Port |Credentials                |Description          |
|----------|-----------|-----|---------------------------|---------------------|
|SSH       |172.20.0.40|2222 |admin / password123        |Weak password SSH    |
|FTP       |172.20.0.50|21   |ftpuser / ftppass          |Anonymous FTP enabled|
|Telnet    |172.20.0.60|23   |testuser / testpass        |Unencrypted telnet   |
|MySQL     |172.20.0.70|3306 |root / root                |Database server      |
|PostgreSQL|172.20.0.75|5432 |postgres / postgres        |Database server      |
|Redis     |172.20.0.80|6379 |requirepass / weakredispass|In-memory database   |
|MongoDB   |172.20.0.85|27017|admin / mongopass          |NoSQL database       |

### Tools Container

|Container    |IP Address |Description                   |
|-------------|-----------|------------------------------|
|Kali Attacker|172.20.0.5 |Pre-loaded with security tools|
|Wireshark    |172.20.0.90|Web-based traffic analyzer    |

## 📖 Common Commands

### Lab Management

```bash
# Start the lab
./lab-manager.sh start

# Check status
./lab-manager.sh status

# Access Kali attacker
./lab-manager.sh kali

# Show all targets
./lab-manager.sh targets

# Stop the lab
./lab-manager.sh stop

# Completely destroy lab (removes all data)
./lab-manager.sh destroy
```

### Inside Kali Container

```bash
# Network discovery
nmap -sn 172.20.0.0/24

# Port scan DVWA
nmap -sV -p- 172.20.0.10

# Web vulnerability scan
nikto -h http://172.20.0.10

# SQL injection test
sqlmap -u "http://172.20.0.10/vulnerabilities/sqli/?id=1" \
  --cookie="security=low; PHPSESSID=xyz"

# SSH brute force (educational purposes)
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://172.20.0.40

# Metasploit
msfconsole
```

## 🎓 Learning Paths

### Beginner: Network Reconnaissance

```bash
# 1. Access Kali
./lab-manager.sh kali

# 2. Discover live hosts
nmap -sn 172.20.0.0/24

# 3. Scan specific target
nmap -sV 172.20.0.10

# 4. Save results
nmap -sV -oA dvwa_scan 172.20.0.10

# Results will be in /shared/ which is accessible from host
```

### Intermediate: Web Application Testing

```bash
# 1. Open DVWA in browser
# http://localhost:8001

# 2. From Kali, run web scanner
nikto -h http://172.20.0.10

# 3. Test SQL injection manually
curl "http://172.20.0.10/vulnerabilities/sqli/?id=1' OR '1'='1"

# 4. Automated SQL injection
sqlmap -u "http://172.20.0.10/vulnerabilities/sqli/?id=1" \
  --cookie="security=low; PHPSESSID=abc123" \
  --dbs
```

### Advanced: Full Penetration Test

```bash
# 1. Reconnaissance
nmap -sS -sV -O -A 172.20.0.0/24 -oA full_scan

# 2. Service enumeration
nmap --script=default,vuln 172.20.0.40

# 3. Exploitation (example with SSH)
# Create password list
echo -e "admin\npassword\npassword123\n123456" > passwords.txt

# Brute force
hydra -l admin -P passwords.txt ssh://172.20.0.40 -t 4

# 4. Post-exploitation
ssh admin@172.20.0.40
# Explore the system

# 5. Documentation
# Save all findings in /shared/ directory
```

## 🔧 Troubleshooting

### Issue: Containers won’t start

```bash
# Check if ports are already in use
sudo netstat -tuln | grep -E '8001|8002|8003|8004'

# Stop conflicting services
sudo systemctl stop apache2  # if applicable

# Restart Docker
sudo systemctl restart docker

# Try again
./lab-manager.sh start
```

### Issue: Can’t connect to targets from Kali

```bash
# Verify network connectivity
docker exec kali-attacker ping -c 3 172.20.0.10

# Check container is running
docker ps | grep dvwa

# Restart specific container
docker restart dvwa

# Check network
docker network inspect security-lab
```

### Issue: Tools missing in Kali

```bash
# Install additional tools
./lab-manager.sh tools

# Or manually
docker exec kali-attacker apt update
docker exec kali-attacker apt install -y nmap nikto sqlmap
```

### Issue: Out of disk space

```bash
# Clean up Docker
docker system prune -a

# Remove old volumes
docker volume prune

# Start fresh
./lab-manager.sh destroy
./lab-manager.sh start
```

## 💡 Best Practices

### 1. **Never expose to internet**

```bash
# The lab uses internal networks only
# Ports 8001-8004 are for HOST access only
# Never forward these ports externally
```

### 2. **Regular backups**

```bash
# Backup your work
./lab-manager.sh backup

# Backups saved to backups/ directory
```

### 3. **Document your findings**

```bash
# Use the shared/ directory
docker exec kali-attacker bash -c "
  echo 'Finding: SQL injection in DVWA' >> /shared/findings.txt
  echo 'URL: http://172.20.0.10/vulnerabilities/sqli/?id=1' >> /shared/findings.txt
"

# Access from host
cat shared/findings.txt
```

### 4. **Stop when not in use**

```bash
# Save resources
./lab-manager.sh stop

# Restart when needed
./lab-manager.sh start
```

### 5. **Keep it updated**

```bash
# Update images periodically
docker compose pull
./lab-manager.sh restart
```

## 🎯 Practice Challenges

### Challenge 1: Find All Services

**Goal**: Discover all running services in the network

```bash
# Tools: nmap
# Target: 172.20.0.0/24
# Expected: ~10 hosts with various services
```

### Challenge 2: Break into SSH

**Goal**: Gain SSH access to 172.20.0.40

```bash
# Tools: hydra, wordlists
# Hint: Password is weak and common
```

### Challenge 3: SQL Injection

**Goal**: Extract database contents from DVWA

```bash
# Tools: sqlmap or manual
# URL: http://172.20.0.10/vulnerabilities/sqli/
# Hint: Set security to "low" first
```

### Challenge 4: Cross-Site Scripting

**Goal**: Execute JavaScript in Juice Shop

```bash
# Tools: Burp Suite, manual testing
# Target: http://localhost:8004
# Look for: Search, review, profile fields
```

### Challenge 5: Network Mapping

**Goal**: Create a complete network diagram

```bash
# Tools: nmap, documentation
# Deliverable: Document all hosts, services, versions
```

## 🔒 Security Considerations

### ✅ Safe Practices

- Lab is isolated on internal Docker network
- No internet access from vulnerable targets
- Easy to destroy and recreate
- Perfect for learning and experimentation

### ⚠️ Important Warnings

- **NEVER** use these techniques on systems you don’t own
- **NEVER** expose lab ports to the internet
- **ALWAYS** stop lab when not in use
- **NEVER** store sensitive data in containers
- These are vulnerable systems - treat as compromised

### 🎓 Ethical Use

This lab is for:

- ✅ Learning security testing techniques
- ✅ Practicing for certifications (CEH, OSCP, etc.)
- ✅ Understanding vulnerabilities
- ✅ Testing your own tools

NOT for:

- ❌ Attacking real systems
- ❌ Illegal activities
- ❌ Unauthorized testing
- ❌ Circumventing security controls

## 📚 Additional Resources

### Learn More

- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe](https://tryhackme.com/)
- [PentesterLab](https://pentesterlab.com/)

### Certifications

- Certified Ethical Hacker (CEH)
- Offensive Security Certified Professional (OSCP)
- CompTIA Security+
- GIAC Penetration Tester (GPEN)

### Communities

- [Reddit r/netsec](https://reddit.com/r/netsec)
- [Reddit r/AskNetsec](https://reddit.com/r/asknetsec)
- [Bug Bounty Forum](https://bugbountyforum.com/)

## 🆘 Getting Help

### Check Logs

```bash
# View logs for specific container
./lab-manager.sh logs dvwa

# View all logs
docker compose logs
```

### Reset Everything

```bash
# Nuclear option - completely reset
./lab-manager.sh destroy
./lab-manager.sh start
```

### Common Commands Reference

```bash
# Quick scan
./lab-manager.sh scan

# See all targets
./lab-manager.sh targets

# Run example tests
./lab-manager.sh examples

# Access monitoring
# Open http://localhost:3000 for Wireshark
```

## 📝 Lab Structure

```
Learning-Networking-Security/
├── docker-compose.yml       # Main lab configuration
├── lab-manager.sh          # Management script
├── LAB-SETUP.md           # This file
├── shared/                # Shared between host and containers
├── captures/              # Network captures
├── scripts/               # Custom scripts
└── backups/              # Lab backups
```

-----

**Remember**: This is a learning environment. Practice responsibly, document your findings, and never use these skills without authorization!

**Happy (Ethical) Hacking! 🔒**
