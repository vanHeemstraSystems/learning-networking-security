#!/usr/bin/env python3
“””
Network Security Auditor
A comprehensive network security scanning and auditing tool for learning purposes.
Author: Your Name
License: MIT
“””

import socket
import sys
import argparse
import threading
import json
import csv
from datetime import datetime
from queue import Queue
import ipaddress
import time

class NetworkAuditor:
“”“Main class for network security auditing”””

```
# Common ports and their services
COMMON_PORTS = {
    20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 465: "SMTPS", 587: "SMTP", 993: "IMAPS", 995: "POP3S",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
    6379: "Redis", 8080: "HTTP-Proxy", 8443: "HTTPS-Alt", 27017: "MongoDB"
}

# Vulnerable service patterns
VULNERABILITIES = {
    "FTP": {
        "port": 21,
        "checks": ["anonymous login", "unencrypted"],
        "severity": "HIGH",
        "recommendation": "Use SFTP (port 22) or FTPS instead"
    },
    "Telnet": {
        "port": 23,
        "checks": ["unencrypted protocol"],
        "severity": "CRITICAL",
        "recommendation": "Replace with SSH (port 22)"
    },
    "HTTP": {
        "port": 80,
        "checks": ["unencrypted web traffic"],
        "severity": "MEDIUM",
        "recommendation": "Use HTTPS (port 443) with valid SSL/TLS"
    },
    "SMB": {
        "port": 445,
        "checks": ["SMBv1 vulnerable to EternalBlue"],
        "severity": "CRITICAL",
        "recommendation": "Disable SMBv1, enable SMBv3 encryption"
    },
    "RDP": {
        "port": 3389,
        "checks": ["brute force attacks", "BlueKeep vulnerability"],
        "severity": "HIGH",
        "recommendation": "Use VPN, enable NLA, apply security patches"
    }
}

def __init__(self, target, ports=None, threads=20, timeout=1, stealth=False, verbose=False):
    """Initialize the network auditor"""
    self.target = target
    self.threads = threads
    self.timeout = timeout
    self.stealth = stealth
    self.verbose = verbose
    self.open_ports = []
    self.results = {}
    self.lock = threading.Lock()
    self.queue = Queue()
    
    # Parse port range
    if ports:
        self.ports = self._parse_port_range(ports)
    else:
        self.ports = list(self.COMMON_PORTS.keys())
    
    # Parse target IPs
    self.targets = self._parse_targets(target)

def _parse_port_range(self, port_string):
    """Parse port range string (e.g., '1-1000' or '80,443,8080')"""
    ports = []
    try:
        if '-' in port_string:
            start, end = map(int, port_string.split('-'))
            ports = list(range(start, end + 1))
        elif ',' in port_string:
            ports = [int(p.strip()) for p in port_string.split(',')]
        else:
            ports = [int(port_string)]
    except ValueError:
        print(f"[!] Invalid port specification: {port_string}")
        sys.exit(1)
    return ports

def _parse_targets(self, target):
    """Parse target IP or CIDR range"""
    try:
        # Try to parse as CIDR
        network = ipaddress.ip_network(target, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError:
        # Single IP address
        return [target]

def _banner_grab(self, ip, port):
    """Attempt to grab service banner"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect((ip, port))
        
        # Send HTTP request for web services
        if port in [80, 443, 8080, 8443]:
            sock.send(b"GET / HTTP/1.1\r\nHost: " + ip.encode() + b"\r\n\r\n")
        
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner
    except:
        return None

def _check_port(self, ip, port):
    """Check if a port is open on the target"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            return True
        return False
    except socket.error:
        return False

def _scan_worker(self, ip):
    """Worker thread for scanning ports"""
    while not self.queue.empty():
        port = self.queue.get()
        
        if self.stealth:
            time.sleep(0.1)  # Slow down for stealth
        
        if self._check_port(ip, port):
            service = self.COMMON_PORTS.get(port, "Unknown")
            banner = self._banner_grab(ip, port)
            
            with self.lock:
                self.open_ports.append(port)
                self.results[port] = {
                    "service": service,
                    "banner": banner,
                    "timestamp": datetime.now().isoformat()
                }
                
                if self.verbose:
                    print(f"[+] {ip}:{port} OPEN - {service}")
        
        self.queue.task_done()

def _analyze_vulnerabilities(self, ip):
    """Analyze scan results for vulnerabilities"""
    vulnerabilities = []
    
    for port in self.open_ports:
        service = self.results[port]["service"]
        
        # Check for known vulnerable services
        for vuln_service, vuln_info in self.VULNERABILITIES.items():
            if vuln_service.lower() in service.lower() or vuln_info["port"] == port:
                vulnerabilities.append({
                    "port": port,
                    "service": service,
                    "severity": vuln_info["severity"],
                    "issues": vuln_info["checks"],
                    "recommendation": vuln_info["recommendation"]
                })
    
    return vulnerabilities

def scan(self):
    """Perform the network scan"""
    print(f"\n{'='*70}")
    print(f"Network Security Audit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    
    for target_ip in self.targets:
        print(f"\n[*] Starting scan on {target_ip}")
        print(f"[*] Scanning {len(self.ports)} ports with {self.threads} threads")
        print(f"[*] Timeout: {self.timeout}s | Stealth: {self.stealth}")
        print(f"{'='*70}\n")
        
        self.open_ports = []
        self.results = {}
        
        # Fill queue with ports
        for port in self.ports:
            self.queue.put(port)
        
        # Start scanning threads
        start_time = time.time()
        thread_list = []
        
        for _ in range(self.threads):
            thread = threading.Thread(target=self._scan_worker, args=(target_ip,))
            thread.daemon = True
            thread.start()
            thread_list.append(thread)
        
        # Wait for all threads to complete
        for thread in thread_list:
            thread.join()
        
        scan_time = time.time() - start_time
        
        # Display results
        self._display_results(target_ip, scan_time)

def _display_results(self, ip, scan_time):
    """Display scan results"""
    print(f"\n{'='*70}")
    print(f"SCAN RESULTS FOR {ip}")
    print(f"{'='*70}\n")
    
    if not self.open_ports:
        print("[!] No open ports found")
        return
    
    print(f"[+] Found {len(self.open_ports)} open ports\n")
    
    # Display open ports
    print(f"{'PORT':<10} {'STATE':<10} {'SERVICE':<20} {'BANNER':<30}")
    print("-" * 70)
    
    for port in sorted(self.open_ports):
        service = self.results[port]["service"]
        banner = self.results[port]["banner"]
        banner_preview = (banner[:27] + "...") if banner and len(banner) > 30 else (banner or "N/A")
        print(f"{port:<10} {'OPEN':<10} {service:<20} {banner_preview:<30}")
    
    # Vulnerability analysis
    vulnerabilities = self._analyze_vulnerabilities(ip)
    
    if vulnerabilities:
        print(f"\n{'='*70}")
        print("SECURITY ASSESSMENT")
        print(f"{'='*70}\n")
        
        for vuln in vulnerabilities:
            print(f"[!] {vuln['severity']} - Port {vuln['port']} ({vuln['service']})")
            print(f"    Issues: {', '.join(vuln['issues'])}")
            print(f"    Recommendation: {vuln['recommendation']}\n")
    
    # Security recommendations
    print(f"{'='*70}")
    print("GENERAL RECOMMENDATIONS")
    print(f"{'='*70}\n")
    
    recommendations = [
        "1. Close all unnecessary ports and services",
        "2. Use firewalls to restrict access to essential services only",
        "3. Implement strong authentication mechanisms",
        "4. Keep all services updated with latest security patches",
        "5. Use encrypted protocols (SSH instead of Telnet, HTTPS instead of HTTP)",
        "6. Monitor logs for suspicious activity",
        "7. Implement intrusion detection/prevention systems (IDS/IPS)",
        "8. Regular security audits and penetration testing"
    ]
    
    for rec in recommendations:
        print(f"  {rec}")
    
    print(f"\n{'='*70}")
    print(f"Scan completed in {scan_time:.2f} seconds")
    print(f"{'='*70}\n")

def export_results(self, filename, format_type='json'):
    """Export results to file"""
    try:
        if format_type == 'json':
            with open(filename, 'w') as f:
                json.dump({
                    "scan_date": datetime.now().isoformat(),
                    "target": self.target,
                    "open_ports": self.open_ports,
                    "results": self.results,
                    "vulnerabilities": self._analyze_vulnerabilities(self.target)
                }, f, indent=2)
        
        elif format_type == 'csv':
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Port', 'State', 'Service', 'Banner'])
                for port in sorted(self.open_ports):
                    writer.writerow([
                        port,
                        'OPEN',
                        self.results[port]['service'],
                        self.results[port]['banner'] or 'N/A'
                    ])
        
        elif format_type == 'text':
            with open(filename, 'w') as f:
                f.write(f"Network Security Audit Report\n")
                f.write(f"Target: {self.target}\n")
                f.write(f"Date: {datetime.now().isoformat()}\n\n")
                f.write(f"Open Ports: {len(self.open_ports)}\n\n")
                for port in sorted(self.open_ports):
                    f.write(f"Port {port}: {self.results[port]['service']}\n")
        
        print(f"[+] Results exported to {filename}")
    except Exception as e:
        print(f"[!] Error exporting results: {e}")
```

def main():
“”“Main function”””
parser = argparse.ArgumentParser(
description=‘Network Security Auditor - Educational Security Scanning Tool’,
formatter_class=argparse.RawDescriptionHelpFormatter,
epilog=”””
Examples:
python network_auditor.py –target 192.168.1.1
python network_auditor.py -t 192.168.1.0/24 -p 1-1000 -th 50
python network_auditor.py -t 10.0.0.1 -p 80,443,8080 -o results.json

WARNING: Only scan networks you own or have explicit permission to test!
“””
)

```
parser.add_argument('-t', '--target', required=True,
                   help='Target IP address or CIDR range (e.g., 192.168.1.1 or 192.168.1.0/24)')
parser.add_argument('-p', '--ports',
                   help='Port range (e.g., 1-1000) or comma-separated ports (e.g., 80,443,8080)')
parser.add_argument('-th', '--threads', type=int, default=20,
                   help='Number of concurrent threads (default: 20)')
parser.add_argument('-to', '--timeout', type=float, default=1,
                   help='Connection timeout in seconds (default: 1)')
parser.add_argument('-o', '--output',
                   help='Output file for results')
parser.add_argument('-f', '--format', choices=['json', 'csv', 'text'], default='json',
                   help='Output format (default: json)')
parser.add_argument('-s', '--stealth', action='store_true',
                   help='Enable stealth mode (slower scanning)')
parser.add_argument('-v', '--verbose', action='store_true',
                   help='Enable verbose output')

args = parser.parse_args()

# Display banner
print("""
```

╔═══════════════════════════════════════════════════════════════════╗
║           Network Security Auditor v1.0                           ║
║           Educational Security Scanning Tool                      ║
║                                                                   ║
║  WARNING: Only use on networks you own or have permission to     ║
║           scan. Unauthorized scanning may be illegal.            ║
╚═══════════════════════════════════════════════════════════════════╝
“””)

```
try:
    # Create auditor instance
    auditor = NetworkAuditor(
        target=args.target,
        ports=args.ports,
        threads=args.threads,
        timeout=args.timeout,
        stealth=args.stealth,
        verbose=args.verbose
    )
    
    # Perform scan
    auditor.scan()
    
    # Export results if requested
    if args.output:
        auditor.export_results(args.output, args.format)
    
except KeyboardInterrupt:
    print("\n\n[!] Scan interrupted by user")
    sys.exit(0)
except Exception as e:
    print(f"\n[!] Error: {e}")
    sys.exit(1)
```

if **name** == “**main**”:
main()
