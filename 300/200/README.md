# Wireshark - Network Protocol Analyzer

## 📖 Overview

**Wireshark** is the world’s most popular network protocol analyzer. It’s a free and open-source packet analyzer used for network troubleshooting, analysis, software and protocol development, and education.

### What Wireshark Does

- Captures live network traffic in real-time
- Analyzes network protocols at a deep level
- Displays packet data in human-readable format
- Filters and searches through captured traffic
- Reconstructs network conversations and sessions
- Identifies network security issues and anomalies

### Key Features

- **Deep Inspection**: Analyzes hundreds of protocols
- **Live Capture**: Real-time packet capture and analysis
- **Offline Analysis**: Examine previously captured data
- **Rich Display Filters**: Powerful filtering capabilities
- **Protocol Decryption**: Decrypt SSL/TLS with proper keys
- **Export Options**: Save data in various formats
- **Multi-platform**: Works on Windows, Linux, macOS, and more

## 🔧 Installation

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install wireshark -y

# Add user to wireshark group for packet capture without sudo
sudo usermod -aG wireshark $USER
# Log out and log back in for changes to take effect

# Or reconfigure to allow non-root capture
sudo dpkg-reconfigure wireshark-common
```

### Linux (RHEL/CentOS/Fedora)

```bash
sudo yum install wireshark wireshark-qt -y
# or
sudo dnf install wireshark wireshark-qt -y

# Add user to wireshark group
sudo usermod -aG wireshark $USER
```

### macOS

```bash
# Using Homebrew
brew install --cask wireshark

# Or download from official website
# Visit: https://www.wireshark.org/download.html
```

### Windows

1. Download installer from: https://www.wireshark.org/download.html
1. Run the `.exe` installer
1. Install WinPcap/Npcap when prompted (required for packet capture)
1. Follow installation wizard
1. Launch Wireshark from Start Menu

### Verify Installation

```bash
wireshark --version
tshark --version  # Command-line version
```

## 💻 Basic Usage

### Starting Wireshark

#### GUI Version

```bash
wireshark
# or with sudo for full capture capabilities
sudo wireshark
```

#### Command-Line Version (TShark)

```bash
tshark -i eth0
```

### Interface Overview

#### Main Components

1. **Capture Interfaces**: Select network interface to monitor
1. **Packet List Pane**: Shows captured packets
1. **Packet Details Pane**: Shows selected packet’s protocol details
1. **Packet Bytes Pane**: Shows raw packet data in hexadecimal
1. **Display Filter Bar**: Filter captured packets
1. **Status Bar**: Shows capture statistics

## 📡 Capturing Traffic

### Start a Basic Capture

1. Open Wireshark
1. Select network interface (e.g., eth0, wlan0)
1. Click blue shark fin icon or double-click interface
1. Traffic appears in real-time
1. Click red square to stop capture

### Command-Line Capture

```bash
# Capture on specific interface
tshark -i eth0

# Capture and save to file
tshark -i eth0 -w capture.pcap

# Capture limited packets
tshark -i eth0 -c 100

# Capture with display filter
tshark -i eth0 -f "port 80"
```

### Capture Filters (Applied During Capture)

```bash
# Capture only HTTP traffic
host 192.168.1.1 and port 80

# Capture traffic to/from specific host
host 192.168.1.1

# Capture specific network
net 192.168.1.0/24

# Capture by protocol
tcp
udp
icmp

# Capture by port
port 443
port 80 or port 443

# Capture excluding broadcast/multicast
not broadcast and not multicast
```

## 🔍 Display Filters (Applied After Capture)

### Basic Filters

#### Filter by Protocol

```
http
dns
tcp
udp
icmp
ssh
ftp
smtp
```

#### Filter by IP Address

```
ip.addr == 192.168.1.1           # Traffic to/from this IP
ip.src == 192.168.1.1            # Traffic from this IP
ip.dst == 192.168.1.1            # Traffic to this IP
```

#### Filter by Port

```
tcp.port == 80                    # TCP port 80
tcp.dstport == 443               # TCP destination port 443
udp.port == 53                    # UDP port 53
```

#### Filter by MAC Address

```
eth.addr == 00:11:22:33:44:55
```

### Advanced Filters

#### HTTP Analysis

```
http.request                      # HTTP requests only
http.request.method == "POST"     # POST requests
http.request.uri contains "login" # URIs containing "login"
http.response.code == 200         # HTTP 200 responses
http.response.code >= 400         # HTTP errors
http.cookie                       # Packets with cookies
```

#### TCP Analysis

```
tcp.flags.syn == 1                # SYN packets
tcp.flags.reset == 1              # RST packets
tcp.analysis.retransmission       # Retransmissions
tcp.analysis.duplicate_ack        # Duplicate ACKs
tcp.window_size < 1000            # Small TCP windows
```

#### DNS Analysis

```
dns.qry.name contains "google"    # DNS queries for google
dns.flags.response == 1           # DNS responses
dns.qry.type == 1                 # A record queries
```

#### TLS/SSL Analysis

```
tls.handshake.type == 1           # Client Hello
tls.handshake.type == 2           # Server Hello
ssl.record.version == 0x0303      # TLS 1.2
```

### Combining Filters

#### AND Operator

```
ip.addr == 192.168.1.1 and tcp.port == 80
http and ip.src == 192.168.1.100
```

#### OR Operator

```
tcp.port == 80 or tcp.port == 443
http or dns
```

#### NOT Operator

```
not arp                           # Exclude ARP
not icmp and not dns             # Exclude ICMP and DNS
```

#### Complex Filters

```
(http.request or tls.handshake) and ip.addr == 192.168.1.1
tcp.port == 443 and not ip.addr == 192.168.1.1
```

## 🎯 Common Analysis Tasks

### Analyze HTTP Traffic

1. Apply filter: `http`
1. Right-click packet → Follow → HTTP Stream
1. View complete HTTP conversation
1. Export objects: File → Export Objects → HTTP

### Analyze DNS Queries

```
dns
dns.qry.name contains "malware"
dns.flags.response == 0  # Queries only
```

### Find Network Issues

```
tcp.analysis.retransmission       # Network congestion
tcp.analysis.lost_segment         # Packet loss
tcp.analysis.duplicate_ack        # Reliability issues
tcp.analysis.zero_window          # Flow control issues
```

### Detect Port Scans

```
tcp.flags.syn == 1 and tcp.flags.ack == 0
# Look for many SYN packets to different ports from same source
```

### Find Unencrypted Passwords

```
http.request.method == "POST"
ftp.request.command == "PASS"
```

### Identify Malicious Traffic

```
http.request.uri contains "cmd"   # Command injection attempts
http.request.uri contains "../"   # Path traversal
dns.qry.name contains ".ru"       # Suspicious TLDs (example)
```

## 📊 Statistics and Analysis

### Protocol Hierarchy

- **Menu**: Statistics → Protocol Hierarchy
- Shows breakdown of protocols in capture
- Identifies most common protocols

### Conversations

- **Menu**: Statistics → Conversations
- Shows communication between endpoints
- Available for IPv4, TCP, UDP, etc.

### Endpoints

- **Menu**: Statistics → Endpoints
- Lists all IP addresses or MAC addresses
- Shows packet and byte counts

### IO Graphs

- **Menu**: Statistics → I/O Graph
- Visualizes traffic over time
- Useful for identifying traffic patterns

### Flow Graph

- **Menu**: Statistics → Flow Graph
- Visual representation of packet flow
- Helps understand communication sequence

## 🔐 SSL/TLS Decryption

### Decrypt HTTPS Traffic with Server Key

1. Obtain server’s private key (.key file)
1. Edit → Preferences → Protocols → TLS
1. Add key file:
- IP Address: server IP
- Port: 443
- Protocol: http
- Key File: path to .key file

### Using Pre-Master Secret (Browser Method)

```bash
# Set environment variable before starting browser
export SSLKEYLOGFILE=/path/to/sslkeys.log
firefox

# In Wireshark
# Edit → Preferences → Protocols → TLS
# (Pre)-Master-Secret log filename: /path/to/sslkeys.log
```

## 💾 Saving and Exporting

### Save Capture File

```
File → Save As
# Choose format: pcap, pcapng (recommended)
```

### Export Specific Packets

```
File → Export Specified Packets
# Select displayed packets only
```

### Export Objects

```
File → Export Objects → HTTP/SMB/etc.
# Extract files transferred over network
```

### Export Packet Dissections

```
File → Export Packet Dissections → As Plain Text/CSV/XML
```

## 🎓 Practical Examples

### Example 1: Investigate Slow Network

```
1. Capture traffic for 5 minutes
2. Statistics → I/O Graph
3. Filter: tcp.analysis.retransmission
4. Identify problematic hosts
5. Statistics → Conversations → TCP
6. Sort by bytes to find heavy users
```

### Example 2: Detect Malware Communication

```
1. Capture all traffic
2. Filter: http.request
3. Look for unusual user-agents
4. Filter: dns
5. Look for suspicious domain names
6. Statistics → Protocol Hierarchy
7. Look for unusual protocols
```

### Example 3: Analyze Login Process

```
1. Filter: http.request.method == "POST"
2. Follow HTTP Stream
3. Look for username/password in clear text
4. Verify if HTTPS is used
```

### Example 4: VoIP Quality Analysis

```
1. Filter: rtp
2. Telephony → RTP → RTP Streams
3. Analyze jitter, packet loss
4. Telephony → VoIP Calls
5. Play back audio if needed
```

## 🛠️ Advanced Features

### TShark Command-Line Examples

#### Basic Capture

```bash
tshark -i eth0 -w capture.pcap
```

#### Read and Filter File

```bash
tshark -r capture.pcap -Y "http"
```

#### Extract Specific Fields

```bash
tshark -r capture.pcap -T fields -e ip.src -e ip.dst -e http.host
```

#### Count Packets by Protocol

```bash
tshark -r capture.pcap -q -z io,phs
```

#### Export HTTP Objects

```bash
tshark -r capture.pcap --export-objects http,/output/directory
```

### Name Resolution

```bash
# Enable name resolution
View → Name Resolution → Resolve Network Addresses
View → Name Resolution → Resolve Transport Addresses

# Disable for better performance
Edit → Preferences → Name Resolution
```

### Color Rules

```
View → Coloring Rules
# Customize packet colors based on filters
# Example: Red for TCP errors, Green for HTTP
```

### Custom Columns

```
Edit → Preferences → Appearance → Columns
# Add custom columns showing specific fields
# Example: Add "http.host" column
```

## 📚 Learning Resources

### Official Documentation

- [Wireshark User’s Guide](https://www.wireshark.org/docs/wsug_html_chunked/)
- [Display Filter Reference](https://www.wireshark.org/docs/dfref/)
- [Sample Captures](https://wiki.wireshark.org/SampleCaptures)

### Books

- “Practical Packet Analysis” by Chris Sanders
- “Wireshark Network Security” by Piyush Gupta
- “Wireshark for Security Professionals” by Jessey Bullock

### Online Resources

- [Wireshark Official Wiki](https://wiki.wireshark.org/)
- [Wireshark Q&A Forum](https://ask.wireshark.org/)
- [PacketLife Cheat Sheets](https://packetlife.net/library/cheat-sheets/)

### Video Tutorials

- [Wireshark YouTube Channel](https://www.youtube.com/wireshark)
- [Hak5 Wireshark Tutorials](https://www.youtube.com/hak5)

## 💡 Best Practices

### 1. Legal Considerations

```bash
# Only capture traffic you're authorized to monitor
# Corporate networks: Get permission from IT/management
# Public WiFi: Be aware of privacy laws
```

### 2. Manage Capture Size

```bash
# Use capture filters to reduce file size
# Set file size limits
# Use ring buffers for continuous capture
```

### 3. Performance Optimization

```bash
# Disable name resolution during capture
# Use capture filters, not just display filters
# Close unnecessary columns
# Use TShark for large files
```

### 4. Organize Captures

```bash
# Use descriptive filenames with dates
# capture_website_issue_20251019.pcap
# Document capture conditions
# Keep separate files for different issues
```

### 5. Privacy and Security

```bash
# Sanitize captures before sharing
# Remove sensitive data (passwords, keys)
# Use TraceWrangler or similar tools
# Never share raw captures publicly
```

## ⚠️ Common Issues and Solutions

### Issue: “No interfaces found” or Permission Denied

**Solution**:

```bash
# Linux: Add user to wireshark group
sudo usermod -aG wireshark $USER
# Then log out and back in

# Or run with sudo (not recommended for regular use)
sudo wireshark
```

### Issue: Capture is very slow

**Solution**:

- Disable name resolution (View → Name Resolution)
- Use capture filters to reduce traffic
- Close unnecessary protocol dissectors
- Increase capture buffer size

### Issue: Can’t see packet contents

**Solution**:

- Check if traffic is encrypted (HTTPS, SSH)
- Enable protocol dissectors (Analyze → Enabled Protocols)
- Check display filter syntax

### Issue: Missing packets in capture

**Solution**:

- Check promiscuous mode is enabled
- Verify capture filter syntax
- Increase buffer size in Capture Options
- Use better network card

## 🔒 Security and Ethics

### Legal Considerations

- **Authorization Required**: Only capture traffic you’re authorized to monitor
- **Privacy Laws**: Be aware of wiretapping and privacy laws in your jurisdiction
- **Corporate Policies**: Follow your organization’s security policies
- **Legal Consequences**: Unauthorized packet capture may violate laws

### Responsible Use

- ✅ Capture your own network traffic
- ✅ Use for authorized security assessments
- ✅ Educational purposes in lab environments
- ✅ Network troubleshooting with permission
- ❌ Never capture others’ traffic without permission
- ❌ Don’t intercept confidential communications
- ❌ Avoid capturing sensitive data unnecessarily

## 🎯 Practice Scenarios

### Set Up Practice Environment

```bash
# Use sample captures from Wireshark wiki
https://wiki.wireshark.org/SampleCaptures

# Create your own traffic
# Use tools like curl, wget, ping in a test environment
```

### Practice Exercises

#### Exercise 1: HTTP Analysis

1. Download HTTP sample capture
1. Filter HTTP traffic
1. Find GET and POST requests
1. Extract transmitted files
1. Identify user-agents

#### Exercise 2: DNS Investigation

1. Capture DNS traffic for 5 minutes
1. Find most queried domains
1. Identify DNS response times
1. Look for DNS tunneling attempts

#### Exercise 3: Security Analysis

1. Use malware traffic capture samples
1. Identify C&C communications
1. Find data exfiltration attempts
1. Detect port scanning activity

## 📝 Quick Reference Cheat Sheet

### Common Display Filters

```
# Protocols
http
dns
tcp
tls
ssh

# IP Filtering
ip.addr == 192.168.1.1
ip.src == 192.168.1.1
ip.dst == 192.168.1.1

# Port Filtering
tcp.port == 80
tcp.dstport == 443
udp.port == 53

# HTTP
http.request
http.response
http.request.method == "POST"
http.response.code == 200

# TCP Flags
tcp.flags.syn == 1
tcp.flags.ack == 1
tcp.flags.reset == 1

# Analysis
tcp.analysis.retransmission
tcp.analysis.duplicate_ack
tcp.analysis.lost_segment

# Logical Operators
and, or, not, ==, !=, contains
```

### Keyboard Shortcuts

```
Ctrl+E      Start/Stop capture
Ctrl+K      Capture options
Ctrl+W      Close capture
Ctrl+F      Find packet
Ctrl+N      Next packet
Ctrl+G      Go to packet
Ctrl+/      Apply display filter
Ctrl+R      Reset coloring
Ctrl+Shift+R    Reload capture
```

## 🔍 Related Tools

### Complementary Tools

- **TShark**: Command-line version of Wireshark
- **tcpdump**: Lightweight packet capture utility
- **NetworkMiner**: Network forensics tool
- **Fiddler**: Web debugging proxy (HTTP/HTTPS)
- **Burp Suite**: Web application security testing

### Analysis Tools

- **Snort**: Intrusion detection system
- **Suricata**: Network threat detection
- **Zeek (Bro)**: Network security monitoring
- **Security Onion**: Network security monitoring distro

-----

**Last Updated**: October 2025  
**Tool Version**: Wireshark 4.0+  
**License**: Wireshark is licensed under GPL v2
