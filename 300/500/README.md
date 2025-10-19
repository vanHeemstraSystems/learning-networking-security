# Docker - Containerized Security Testing Environments

## 📖 Overview

**Docker** enables you to create isolated, reproducible environments for security testing. By containerizing your tests and targets, you can safely practice security techniques without risking damage to production networks or systems.

### Why Use Docker for Security Testing?

- **Isolation**: Tests run in contained environments, separated from your actual network
- **Reproducibility**: Easily recreate testing scenarios
- **Safety**: Practice exploits without real-world consequences
- **Portability**: Share testing environments with others
- **Quick Setup**: Spin up vulnerable targets in seconds
- **Learning**: Understand containerization security issues

### Key Concepts

- **Container**: Isolated process with its own filesystem, network, and resources
- **Image**: Template for creating containers
- **Dockerfile**: Instructions for building images
- **Docker Compose**: Tool for defining multi-container applications
- **Network**: Isolated network for container communication
- **Volume**: Persistent storage for containers

## 🔧 Installation

### Linux (Ubuntu/Debian)

```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group (avoid sudo)
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

### Linux (RHEL/CentOS/Fedora)

```bash
# Remove old versions
sudo dnf remove docker docker-client docker-client-latest docker-common docker-latest

# Add Docker repository
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Install Docker
sudo dnf install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
```

### macOS

```bash
# Download Docker Desktop from:
# https://www.docker.com/products/docker-desktop/

# Or use Homebrew
brew install --cask docker

# Launch Docker Desktop
# Verify installation
docker --version
docker compose version
```

### Windows

1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
1. Run installer (requires WSL 2)
1. Follow installation wizard
1. Launch Docker Desktop
1. Verify in PowerShell:

```powershell
docker --version
docker compose version
```

## 💻 Basic Docker Commands

### Container Management

```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Run a container
docker run [OPTIONS] IMAGE [COMMAND]

# Start a stopped container
docker start CONTAINER_ID

# Stop a running container
docker stop CONTAINER_ID

# Remove a container
docker rm CONTAINER_ID

# Remove all stopped containers
docker container prune
```

### Image Management

```bash
# List images
docker images

# Pull an image
docker pull IMAGE_NAME

# Remove an image
docker rmi IMAGE_NAME

# Build an image
docker build -t IMAGE_NAME .

# Remove unused images
docker image prune
```

### Network Management

```bash
# List networks
docker network ls

# Create a network
docker network create NETWORK_NAME

# Inspect a network
docker network inspect NETWORK_NAME

# Connect container to network
docker network connect NETWORK_NAME CONTAINER_ID

# Remove a network
docker network rm NETWORK_NAME
```

### Logs and Debugging

```bash
# View container logs
docker logs CONTAINER_ID

# Follow logs in real-time
docker logs -f CONTAINER_ID

# Execute command in running container
docker exec -it CONTAINER_ID /bin/bash

# Inspect container details
docker inspect CONTAINER_ID

# View container resource usage
docker stats
```

## 🔒 Isolated Security Testing Lab

### Creating an Isolated Network

```bash
# Create a custom bridge network for testing
docker network create --driver bridge --subnet 172.20.0.0/16 security-lab

# List networks to verify
docker network ls

# Inspect network
docker network inspect security-lab
```

### Basic Testing Container

**Dockerfile for Security Testing**

```dockerfile
FROM kalilinux/kali-rolling

# Update and install tools
RUN apt update && apt install -y \
    nmap \
    nikto \
    sqlmap \
    netcat-traditional \
    curl \
    wget \
    dnsutils \
    net-tools \
    iputils-ping \
    tcpdump \
    python3 \
    python3-pip

# Set working directory
WORKDIR /security

# Keep container running
CMD ["/bin/bash"]
```

**Build and Run**

```bash
# Build the image
docker build -t security-toolkit .

# Run with network access
docker run -it --name attacker --network security-lab security-toolkit

# Run with host network (for some tools)
docker run -it --network host security-toolkit
```

## 🎯 Vulnerable Target Containers

### 1. DVWA (Damn Vulnerable Web Application)

**docker-compose.yml**

```yaml
version: '3.8'

services:
  dvwa:
    image: vulnerables/web-dvwa
    container_name: dvwa
    ports:
      - "80:80"
    networks:
      security-lab:
        ipv4_address: 172.20.0.10
    environment:
      - MYSQL_HOST=dvwa-db
      - MYSQL_DATABASE=dvwa
      - MYSQL_USER=dvwa
      - MYSQL_PASSWORD=dvwa

  dvwa-db:
    image: mysql:5.7
    container_name: dvwa-db
    networks:
      security-lab:
        ipv4_address: 172.20.0.11
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=dvwa
      - MYSQL_USER=dvwa
      - MYSQL_PASSWORD=dvwa

networks:
  security-lab:
    external: true
```

**Deploy DVWA**

```bash
# Create network first
docker network create --subnet 172.20.0.0/16 security-lab

# Start DVWA
docker compose up -d

# Access at http://localhost
# Default credentials: admin / password
```

### 2. Metasploitable3

```bash
# Pull Metasploitable3 image
docker pull tleemcjr/metasploitable3

# Run on isolated network
docker run -it --name metasploitable3 \
    --network security-lab \
    --ip 172.20.0.20 \
    tleemcjr/metasploitable3
```

### 3. WebGoat (OWASP)

```yaml
version: '3.8'

services:
  webgoat:
    image: webgoat/webgoat-8.0
    container_name: webgoat
    ports:
      - "8080:8080"
      - "9090:9090"
    networks:
      security-lab:
        ipv4_address: 172.20.0.30
    environment:
      - WEBGOAT_HOST=0.0.0.0
      - WEBGOAT_PORT=8080

networks:
  security-lab:
    external: true
```

### 4. Vulnerable Node.js Application

**Dockerfile**

```dockerfile
FROM node:14

WORKDIR /app

# Create vulnerable app
RUN npm init -y && \
    npm install express sqlite3

# Create vulnerable server
COPY vulnerable-app.js .

EXPOSE 3000

CMD ["node", "vulnerable-app.js"]
```

**vulnerable-app.js**

```javascript
const express = require('express');
const sqlite3 = require('sqlite3');
const app = express();

app.use(express.urlencoded({ extended: true }));

const db = new sqlite3.Database(':memory:');

db.run(`CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)`);

db.run(`INSERT INTO users (username, password) VALUES 
    ('admin', 'admin123'),
    ('user', 'password')`);

// Vulnerable to SQL Injection
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const query = `SELECT * FROM users WHERE username='${username}' AND password='${password}'`;
    
    db.get(query, (err, row) => {
        if (err) {
            res.send('Error: ' + err.message);
        } else if (row) {
            res.send('Login successful! Welcome ' + row.username);
        } else {
            res.send('Invalid credentials');
        }
    });
});

// Vulnerable to XSS
app.get('/search', (req, res) => {
    const query = req.query.q;
    res.send(`<h1>Search Results for: ${query}</h1>`);
});

app.get('/', (req, res) => {
    res.send(`
        <h1>Vulnerable Node.js App</h1>
        <form action="/login" method="POST">
            <input name="username" placeholder="Username"><br>
            <input name="password" type="password" placeholder="Password"><br>
            <button type="submit">Login</button>
        </form>
    `);
});

app.listen(3000, () => {
    console.log('Vulnerable app running on port 3000');
});
```

## 🏗️ Complete Security Lab Setup

### docker-compose.yml (Full Lab)

```yaml
version: '3.8'

services:
  # Attacker machine with tools
  kali:
    image: kalilinux/kali-rolling
    container_name: kali-attacker
    tty: true
    stdin_open: true
    networks:
      security-lab:
        ipv4_address: 172.20.0.5
    volumes:
      - ./shared:/shared
    command: /bin/bash

  # DVWA - Web vulnerabilities
  dvwa:
    image: vulnerables/web-dvwa
    container_name: dvwa-target
    networks:
      security-lab:
        ipv4_address: 172.20.0.10
    depends_on:
      - dvwa-db

  dvwa-db:
    image: mysql:5.7
    container_name: dvwa-db
    networks:
      security-lab:
        ipv4_address: 172.20.0.11
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: dvwa
      MYSQL_USER: dvwa
      MYSQL_PASSWORD: dvwa

  # WebGoat - OWASP training
  webgoat:
    image: webgoat/webgoat-8.0
    container_name: webgoat-target
    networks:
      security-lab:
        ipv4_address: 172.20.0.30

  # Vulnerable SSH server
  ssh-target:
    image: linuxserver/openssh-server
    container_name: ssh-target
    networks:
      security-lab:
        ipv4_address: 172.20.0.40
    environment:
      - PUID=1000
      - PGID=1000
      - PASSWORD_ACCESS=true
      - USER_PASSWORD=weakpassword
      - USER_NAME=admin

  # Vulnerable FTP server
  ftp-target:
    image: fauria/vsftpd
    container_name: ftp-target
    networks:
      security-lab:
        ipv4_address: 172.20.0.50
    environment:
      FTP_USER: ftpuser
      FTP_PASS: ftppass
      PASV_ADDRESS: 172.20.0.50

networks:
  security-lab:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
          gateway: 172.20.0.1

volumes:
  shared:
```

### Deploy Complete Lab

```bash
# Create and start all containers
docker compose up -d

# Verify all containers are running
docker ps

# Access Kali attacker
docker exec -it kali-attacker /bin/bash

# Inside Kali, scan the network
apt update && apt install -y nmap
nmap -sn 172.20.0.0/16

# Scan specific target
nmap -sV -p- 172.20.0.10
```

## 🔍 Practical Testing Scenarios

### Scenario 1: Port Scanning Practice

```bash
# From attacker container
docker exec -it kali-attacker bash

# Inside container, scan targets
nmap -sV 172.20.0.10  # DVWA
nmap -sV 172.20.0.30  # WebGoat
nmap -sV 172.20.0.40  # SSH target

# Comprehensive scan
nmap -sS -sV -O -A 172.20.0.0/24
```

### Scenario 2: Web Application Testing

```bash
# Access DVWA from host
# http://localhost (if port is exposed)

# Or from attacker container
docker exec -it kali-attacker bash
apt install -y curl nikto

# Scan DVWA
nikto -h http://172.20.0.10

# Test SQL injection
curl "http://172.20.0.10/vulnerabilities/sqli/?id=1' OR '1'='1&Submit=Submit"
```

### Scenario 3: Password Attacks

```bash
# SSH brute force with Hydra
docker exec -it kali-attacker bash
apt install -y hydra

# Create wordlist
echo -e "admin\npassword\nweakpassword\n123456" > passwords.txt

# Attack SSH target
hydra -l admin -P passwords.txt ssh://172.20.0.40
```

### Scenario 4: Network Traffic Analysis

```bash
# Run tcpdump in target container
docker exec dvwa-target tcpdump -i any -w /tmp/capture.pcap

# Copy capture file to host
docker cp dvwa-target:/tmp/capture.pcap ./capture.pcap

# Analyze with Wireshark on host
wireshark capture.pcap
```

## 🛡️ Network Isolation Techniques

### 1. No External Network Access

```yaml
version: '3.8'

services:
  isolated-target:
    image: vulnerables/web-dvwa
    networks:
      - isolated
    # No ports exposed to host

networks:
  isolated:
    driver: bridge
    internal: true  # No external connectivity
```

### 2. Limited Network Access

```bash
# Create network with no internet access
docker network create --internal isolated-lab

# Run container on isolated network
docker run -it --network isolated-lab nginx
```

### 3. Custom Firewall Rules

```dockerfile
FROM ubuntu:22.04

# Install iptables
RUN apt update && apt install -y iptables

# Add firewall rules
RUN iptables -A INPUT -p tcp --dport 80 -j ACCEPT && \
    iptables -A INPUT -p tcp --dport 443 -j ACCEPT && \
    iptables -A INPUT -j DROP
```

## 🔧 Running Security Tools in Containers

### Nmap Container

```bash
# Official Nmap container
docker run --rm -it instrumentisto/nmap

# Scan target from container
docker run --rm -it \
    --network security-lab \
    instrumentisto/nmap -sV 172.20.0.10
```

### Metasploit Container

```bash
# Run Metasploit container
docker run --rm -it \
    --network security-lab \
    metasploitframework/metasploit-framework

# Inside container
msfconsole
```

### Burp Suite Container

```bash
# Run Burp Suite (requires X11 forwarding on Linux)
docker run --rm -it \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --network security-lab \
    raesene/burp-free
```

### SQLMap Container

```bash
# Pull SQLMap image
docker pull paoloo/sqlmap

# Run SQLMap
docker run --rm -it \
    --network security-lab \
    paoloo/sqlmap \
    -u "http://172.20.0.10/vulnerabilities/sqli/?id=1" \
    --cookie="security=low; PHPSESSID=xyz"
```

## 📊 Monitoring and Logging

### Container Logs

```bash
# View logs from specific container
docker logs dvwa-target

# Follow logs in real-time
docker logs -f dvwa-target

# Save logs to file
docker logs dvwa-target > dvwa-logs.txt
```

### Resource Monitoring

```bash
# Monitor all containers
docker stats

# Monitor specific container
docker stats dvwa-target

# Limit container resources
docker run -it \
    --memory="512m" \
    --cpus="1.0" \
    vulnerables/web-dvwa
```

## 🎓 Advanced Techniques

### 1. Custom Vulnerable Container

**Dockerfile**

```dockerfile
FROM ubuntu:22.04

# Install vulnerable software
RUN apt update && apt install -y \
    apache2 \
    php \
    php-mysql \
    mysql-server \
    openssh-server \
    vsftpd

# Configure SSH with weak password
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Add vulnerable PHP code
RUN echo '<?php system($_GET["cmd"]); ?>' > /var/www/html/cmd.php

# Expose services
EXPOSE 22 80 21

CMD service ssh start && \
    service apache2 start && \
    service mysql start && \
    tail -f /dev/null
```

### 2. Network Segmentation

```yaml
version: '3.8'

services:
  attacker:
    image: kalilinux/kali-rolling
    networks:
      - dmz

  web-server:
    image: nginx
    networks:
      - dmz
      - internal

  database:
    image: mysql
    networks:
      - internal

networks:
  dmz:
    driver: bridge
  internal:
    driver: bridge
    internal: true
```

### 3. Automated Testing Pipeline

```bash
#!/bin/bash
# automated-test.sh

# Start lab environment
docker compose up -d

# Wait for services
sleep 30

# Run automated tests
docker exec kali-attacker nmap -sV 172.20.0.0/24 -oX /shared/scan-results.xml

# Run web scanner
docker exec kali-attacker nikto -h http://172.20.0.10 -o /shared/nikto-results.txt

# Cleanup
docker compose down
```

## 💡 Best Practices

### 1. Regular Cleanup

```bash
# Remove unused containers
docker container prune -f

# Remove unused images
docker image prune -a -f

# Remove unused networks
docker network prune -f

# Remove everything
docker system prune -a --volumes -f
```

### 2. Use Docker Compose

```bash
# Instead of long docker run commands
# Use docker-compose.yml files
docker compose up -d
docker compose down
```

### 3. Version Control

```bash
# Keep Dockerfiles and compose files in Git
git init
echo "*.pcap" >> .gitignore
echo "shared/" >> .gitignore
git add Dockerfile docker-compose.yml
git commit -m "Add security lab setup"
```

### 4. Document Your Lab

```bash
# Create README.md for each lab
# Include:
# - Purpose of the lab
# - How to deploy
# - What to test
# - Expected results
```

### 5. Security Considerations

```bash
# Never expose vulnerable containers to internet
# Use internal networks only
# Don't use in production
# Keep containers updated
# Remove labs when not in use
```

## 📚 Learning Resources

### Official Documentation

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Security](https://docs.docker.com/engine/security/)

### Docker Security

- [Docker Bench for Security](https://github.com/docker/docker-bench-security)
- [Container Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)

### Vulnerable Containers

- [Vulhub](https://github.com/vulhub/vulhub) - Pre-built vulnerable environments
- [OWASP Docker Images](https://hub.docker.com/u/owasp)
- [Awesome Docker Security](https://github.com/myugan/awesome-docker-security)

### Books

- “Docker Deep Dive” by Nigel Poulton
- “Docker Security” by Adrian Mouat

## ⚠️ Common Issues and Solutions

### Issue: Cannot connect to Docker daemon

**Solution**:

```bash
# Start Docker service
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Issue: Port already in use

**Solution**:

```bash
# Find process using port
sudo lsof -i :80

# Kill process or change port mapping
docker run -p 8080:80 image_name
```

### Issue: Container exits immediately

**Solution**:

```bash
# Keep container running
docker run -it --entrypoint /bin/bash image_name

# Or use tty and stdin
docker run -it image_name
```

### Issue: Network isolation not working

**Solution**:

```bash
# Verify network is internal
docker network inspect network_name

# Recreate network with internal flag
docker network create --internal isolated-network
```

## 🔍 Quick Reference

### Essential Commands

```bash
# Build and run
docker build -t myimage .
docker run -it --rm myimage

# Compose
docker compose up -d
docker compose down
docker compose logs -f

# Network
docker network create mynetwork
docker network connect mynetwork container

# Cleanup
docker system prune -a
docker volume prune

# Inspect
docker inspect container_name
docker logs container_name
docker exec -it container_name /bin/bash
```

### Useful Flags

```bash
-d              # Detached mode
-it             # Interactive with TTY
--rm            # Remove after exit
--name          # Container name
--network       # Connect to network
-p              # Port mapping
-v              # Volume mount
--ip            # Static IP address
```

-----

**Last Updated**: October 2025  
**Docker Version**: 24.x+  
**License**: Docker is licensed under Apache 2.0
