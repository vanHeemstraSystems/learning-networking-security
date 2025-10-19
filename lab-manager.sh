#!/bin/bash

# Security Lab Manager Script

# Manages Docker-based security testing environment

set -e

# Colors for output

RED=’\033[0;31m’
GREEN=’\033[0;32m’
YELLOW=’\033[1;33m’
BLUE=’\033[0;34m’
NC=’\033[0m’ # No Color

# Functions

print_banner() {
echo -e “${BLUE}”
echo “╔════════════════════════════════════════════════════════════╗”
echo “║         Security Testing Lab Manager                       ║”
echo “║         Safe, Isolated Network Testing Environment        ║”
echo “╚════════════════════════════════════════════════════════════╝”
echo -e “${NC}”
}

print_success() {
echo -e “${GREEN}[✓]${NC} $1”
}

print_error() {
echo -e “${RED}[✗]${NC} $1”
}

print_info() {
echo -e “${BLUE}[i]${NC} $1”
}

print_warning() {
echo -e “${YELLOW}[!]${NC} $1”
}

check_docker() {
if ! command -v docker &> /dev/null; then
print_error “Docker is not installed. Please install Docker first.”
exit 1
fi

```
if ! docker info &> /dev/null; then
    print_error "Docker daemon is not running. Please start Docker."
    exit 1
fi

print_success "Docker is installed and running"
```

}

check_compose() {
if ! docker compose version &> /dev/null; then
print_error “Docker Compose is not installed.”
exit 1
fi
print_success “Docker Compose is installed”
}

create_directories() {
print_info “Creating required directories…”
mkdir -p shared captures scripts
print_success “Directories created”
}

start_lab() {
print_info “Starting security lab environment…”
docker compose up -d

```
echo ""
print_success "Security lab is starting up!"
print_info "Waiting for services to initialize (30 seconds)..."
sleep 30

show_status
```

}

stop_lab() {
print_info “Stopping security lab environment…”
docker compose down
print_success “Security lab stopped”
}

restart_lab() {
print_info “Restarting security lab environment…”
docker compose restart
print_success “Security lab restarted”
}

destroy_lab() {
print_warning “This will destroy all lab containers and data!”
read -p “Are you sure? (yes/no): “ confirm
if [ “$confirm” = “yes” ]; then
print_info “Destroying security lab…”
docker compose down -v
print_success “Security lab destroyed”
else
print_info “Operation cancelled”
fi
}

show_status() {
echo “”
print_info “Lab Status:”
docker compose ps

```
echo ""
print_info "Network Information:"
docker network inspect security-lab --format '{{range .Containers}}{{.Name}}: {{.IPv4Address}}{{"\n"}}{{end}}' 2>/dev/null || echo "Network not created yet"

echo ""
print_info "Access Points:"
echo "  DVWA:       http://localhost:8001 (admin/password)"
echo "  WebGoat:    http://localhost:8002"
echo "  bWAPP:      http://localhost:8003 (bee/bug)"
echo "  Juice Shop: http://localhost:8004"
echo "  Wireshark:  http://localhost:3000"
echo ""
echo "  SSH:        ssh admin@localhost -p 2222 (password123)"
echo "  FTP:        ftp localhost 21 (ftpuser/ftppass)"
echo "  MySQL:      mysql -h localhost -u root -p (root)"
echo ""
```

}

access_kali() {
print_info “Accessing Kali attacker container…”
docker exec -it kali-attacker /bin/bash
}

run_scan() {
print_info “Running network scan from Kali container…”
docker exec kali-attacker nmap -sn 172.20.0.0/24
}

show_logs() {
if [ -z “$1” ]; then
print_error “Please specify a container name”
echo “Available containers:”
docker compose ps –format “table {{.Name}}”
exit 1
fi
docker compose logs -f “$1”
}

backup_lab() {
print_info “Creating backup of lab data…”
timestamp=$(date +%Y%m%d_%H%M%S)
backup_dir=“backups/lab_backup_${timestamp}”

```
mkdir -p "$backup_dir"

# Backup volumes
docker run --rm \
    -v security-lab_dvwa-db-data:/data \
    -v "$(pwd)/${backup_dir}:/backup" \
    alpine tar czf /backup/dvwa-db.tar.gz -C /data .

# Copy shared files
cp -r shared "$backup_dir/" 2>/dev/null || true
cp -r captures "$backup_dir/" 2>/dev/null || true

print_success "Backup created at: $backup_dir"
```

}

install_tools() {
print_info “Installing additional tools in Kali container…”
docker exec kali-attacker bash -c “
apt update &&
apt install -y   
nmap   
nikto   
sqlmap   
hydra   
metasploit-framework   
netcat-traditional   
dnsutils   
net-tools   
iputils-ping   
tcpdump   
wireshark   
aircrack-ng   
john   
hashcat &&
echo ‘Tools installed successfully’
“
print_success “Additional tools installed”
}

show_targets() {
echo “”
print_info “Available Targets:”
echo “”
echo “Web Applications:”
echo “  172.20.0.10 - DVWA (Damn Vulnerable Web App)”
echo “  172.20.0.30 - WebGoat (OWASP Training)”
echo “  172.20.0.35 - bWAPP (Buggy Web App)”
echo “  172.20.0.36 - Juice Shop (Modern JS App)”
echo “”
echo “Network Services:”
echo “  172.20.0.40 - SSH Server (port 2222)”
echo “  172.20.0.50 - FTP Server (port 21)”
echo “  172.20.0.60 - Telnet Server (port 23)”
echo “”
echo “Databases:”
echo “  172.20.0.70 - MySQL (port 3306)”
echo “  172.20.0.75 - PostgreSQL (port 5432)”
echo “  172.20.0.80 - Redis (port 6379)”
echo “  172.20.0.85 - MongoDB (port 27017)”
echo “”
echo “Monitoring:”
echo “  172.20.0.90 - Wireshark”
echo “”
}

run_example_tests() {
print_info “Running example security tests…”

```
echo ""
echo "1. Network Discovery:"
docker exec kali-attacker nmap -sn 172.20.0.0/24

echo ""
echo "2. Port Scan of DVWA:"
docker exec kali-attacker nmap -sV 172.20.0.10

echo ""
echo "3. HTTP Headers of WebGoat:"
docker exec kali-attacker curl -I http://172.20.0.30:8080

print_success "Example tests completed"
```

}

show_help() {
echo “Usage: $0 [command]”
echo “”
echo “Commands:”
echo “  start        - Start the security lab”
echo “  stop         - Stop the security lab”
echo “  restart      - Restart the security lab”
echo “  destroy      - Destroy lab and all data”
echo “  status       - Show lab status and access points”
echo “  kali         - Access Kali attacker shell”
echo “  scan         - Run quick network scan”
echo “  logs [name]  - Show logs for specific container”
echo “  targets      - List all available targets”
echo “  backup       - Backup lab data”
echo “  tools        - Install additional tools in Kali”
echo “  examples     - Run example security tests”
echo “  help         - Show this help message”
echo “”
}

# Main script

print_banner

if [ $# -eq 0 ]; then
show_help
exit 0
fi

check_docker
check_compose
create_directories

case “$1” in
start)
start_lab
;;
stop)
stop_lab
;;
restart)
restart_lab
;;
destroy)
destroy_lab
;;
status)
show_status
;;
kali)
access_kali
;;
scan)
run_scan
;;
logs)
show_logs “$2”
;;
targets)
show_targets
;;
backup)
backup_lab
;;
tools)
install_tools
;;
examples)
run_example_tests
;;
help)
show_help
;;
*)
print_error “Unknown command: $1”
show_help
exit 1
;;
esac

exit 0
