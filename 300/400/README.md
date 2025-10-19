# Burp Suite - Web Application Security Testing

## 📖 Overview

**Burp Suite** is the industry-standard toolkit for web application security testing. Developed by PortSwigger, it’s an integrated platform for performing security testing of web applications.

### What Burp Suite Does

- Intercepts and modifies HTTP/HTTPS traffic
- Discovers security vulnerabilities in web applications
- Maps application content and functionality
- Tests for common web vulnerabilities (OWASP Top 10)
- Automates custom security tests
- Provides comprehensive reporting

### Key Features

- **Proxy**: Intercepts and modifies web traffic
- **Scanner**: Automated vulnerability scanner (Pro only)
- **Intruder**: Automated attacks and fuzzing
- **Repeater**: Manual request modification and testing
- **Sequencer**: Tests randomness of session tokens
- **Decoder**: Encodes/decodes data
- **Comparer**: Compares application responses
- **Extender**: Plugin architecture for custom extensions

## 🔧 Installation

### Burp Suite Versions

#### Community Edition (Free)

- Basic manual testing tools
- Limited functionality
- No automated scanner
- Throttled Intruder

#### Professional Edition (Paid)

- Full automated scanner
- Advanced tools and features
- Faster scanning
- Save/restore projects
- Commercial support

### Download and Install

#### All Platforms

1. Visit: https://portswigger.net/burp/releases
1. Download appropriate version:
- JAR file (cross-platform)
- Platform-specific installer
1. Run installer or JAR file

#### Linux Installation

```bash
# Download JAR file
wget https://portswigger-cdn.net/burp/releases/download?product=community&type=jar -O burpsuite.jar

# Make executable (for installer)
chmod +x burpsuite_community_linux_v*.sh
./burpsuite_community_linux_v*.sh

# Or run JAR directly
java -jar burpsuite.jar
```

#### macOS Installation

```bash
# Using Homebrew Cask
brew install --cask burp-suite

# Or download DMG from PortSwigger website
# Drag to Applications folder
```

#### Windows Installation

1. Download `.exe` installer
1. Run installer as Administrator
1. Follow installation wizard
1. Launch from Start Menu

### Requirements

- Java Runtime Environment (JRE) 17 or later
- Minimum 4GB RAM (8GB recommended)
- Modern web browser (Chrome, Firefox)

### Verify Installation

```bash
# Check Java version
java -version

# Launch Burp Suite
java -jar burpsuite.jar
```

## 💻 Initial Setup

### First Launch Configuration

1. **Project Selection** (Pro only)
- Temporary project (Community/Pro)
- New project on disk (Pro)
- Open existing project (Pro)
1. **Configuration**
- Use Burp defaults
- Load from configuration file

### Browser Configuration

#### Firefox Configuration

1. Open Firefox → Settings → Network Settings
1. Select “Manual proxy configuration”
1. HTTP Proxy: `127.0.0.1`, Port: `8080`
1. Check “Also use this proxy for HTTPS”
1. No proxy for: (leave empty)

#### Chrome Configuration

```bash
# Launch Chrome with proxy
chrome.exe --proxy-server="127.0.0.1:8080"

# Or use FoxyProxy extension
# Install FoxyProxy Standard
# Configure proxy: 127.0.0.1:8080
```

### SSL Certificate Installation

#### Why Install Certificate?

- View HTTPS traffic without errors
- Intercept encrypted communications
- Required for testing modern web apps

#### Install Certificate Steps

1. **Generate Certificate in Burp**
- Navigate to http://burp (while proxy is running)
- Click “CA Certificate”
- Save `cacert.der`
1. **Firefox Installation**
- Settings → Privacy & Security → Certificates
- View Certificates → Authorities → Import
- Select `cacert.der`
- Trust for websites
1. **Chrome/Windows Installation**
- Run: `certmgr.msc`
- Trusted Root Certification Authorities → Import
- Select `cacert.der`
1. **Linux Installation**

```bash
# Convert DER to PEM
openssl x509 -in cacert.der -inform DER -out burp.crt

# Copy to certificates directory
sudo cp burp.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

1. **macOS Installation**
- Open Keychain Access
- File → Import Items → Select `cacert.der`
- Find certificate → Get Info → Trust → Always Trust

## 🎯 Core Tools

### 1. Proxy

The Proxy sits between your browser and target application, intercepting all HTTP/HTTPS traffic.

#### Basic Operations

```
Proxy → Intercept
- Turn intercept on/off
- Forward: Send request/response
- Drop: Discard request/response
- Action: Send to other tools

Proxy → HTTP History
- View all requests/responses
- Filter by various criteria
- Right-click for options

Proxy → WebSockets History
- View WebSocket messages

Proxy → Options
- Configure proxy listeners
- Intercept rules
- Match and replace
```

#### Common Tasks

**Intercept and Modify Request**

1. Enable intercept: Proxy → Intercept → Intercept is on
1. Browse to target site
1. Request appears in Intercept tab
1. Modify parameters, headers, body
1. Click Forward to send modified request

**Send to Other Tools**

- Right-click request → Send to Repeater
- Right-click request → Send to Intruder
- Right-click request → Send to Scanner (Pro)

### 2. Target

Organizes information about target applications.

#### Site Map

```
Target → Site map
- Tree view of application structure
- Automatically built from proxy traffic
- Color-coded by response codes
- Right-click for scanning options
```

#### Scope

```
Target → Scope
- Define testing boundaries
- Include/exclude URLs
- Use scope for proxy filtering
```

**Define Scope**

1. Right-click domain in Site map
1. Add to scope
1. Proxy → Options → Filter by scope

### 3. Repeater

Manual request modification and testing tool.

#### Using Repeater

1. Send request from Proxy/Target
1. Modify request as needed
1. Click Send
1. Analyze response
1. Repeat with different inputs

#### Practical Examples

**Test SQL Injection**

```
1. Find parameter in request
2. Send to Repeater
3. Add SQL payload: ' OR '1'='1
4. Send and observe response
5. Try different payloads
```

**Test Authentication Bypass**

```
1. Capture login request
2. Modify credentials
3. Test with various inputs
4. Analyze responses
```

### 4. Intruder

Automated customized attacks.

#### Attack Types

**Sniper** - Single payload position, one payload at a time

```
Example: Testing username enumeration
POST /login
username=§admin§&password=test
```

**Battering Ram** - Same payload in all positions

```
Example: Testing same value everywhere
POST /login
username=§admin§&password=§admin§
```

**Pitchfork** - Different payload sets, parallel iteration

```
Example: Testing username:password pairs
POST /login
username=§admin§&password=§password123§
Payload set 1: admin, user, test
Payload set 2: pass123, pass456, pass789
```

**Cluster Bomb** - All combinations

```
Example: Brute force attack
POST /login
username=§admin§&password=§pass§
Tests all username × password combinations
```

#### Using Intruder

1. Send request to Intruder
1. Set payload positions (§ markers)
1. Configure attack type
1. Configure payloads
1. Start attack
1. Analyze results

**Payload Types**

- Simple list
- Runtime file
- Numbers
- Dates
- Brute forcer
- Null payloads
- Character substitution
- Many more…

### 5. Decoder

Encode/decode data in various formats.

**Supported Formats**

- URL encoding/decoding
- HTML encoding/decoding
- Base64 encode/decode
- ASCII hex
- Hex, Octal, Binary
- Hash (MD5, SHA-1, SHA-256, etc.)

**Usage**

1. Paste data in Decoder
1. Select encode/decode operation
1. Chain multiple operations
1. Copy result

### 6. Comparer

Compares two pieces of data to find differences.

**Usage**

1. Send two requests/responses to Comparer
1. Click “Compare”
1. View differences highlighted
1. Useful for:
- Session token analysis
- Finding hidden parameters
- Comparing responses

### 7. Sequencer

Analyzes randomness and predictability of session tokens.

**Usage**

1. Capture request that generates tokens
1. Send to Sequencer
1. Configure token location
1. Start live capture
1. Analyze randomness after 100+ tokens
1. Review entropy analysis

**Tests**

- Character-level analysis
- Bit-level analysis
- Correlation analysis
- Compression analysis

### 8. Scanner (Professional Only)

Automated vulnerability scanner.

#### Scan Types

**Crawl**

- Discovers application content
- Maps site structure
- Identifies entry points

**Active Scan**

- Tests for vulnerabilities
- Sends malicious payloads
- Generates findings

**Passive Scan**

- Analyzes traffic without attacking
- Low-risk assessment
- Always running in background

#### Using Scanner

**Quick Scan**

1. Right-click target → Scan
1. Select scan type
1. Configure scan settings
1. Start scan
1. Review issues in Dashboard

**Manual Testing with Scanner**

1. Browse application through proxy
1. Scanner passively analyzes traffic
1. Review Issues tab for findings
1. Manually verify issues

## 🔍 Common Vulnerabilities Testing

### SQL Injection

**Manual Testing**

```
1. Find input parameter
2. Send to Repeater
3. Test payloads:
   ' OR '1'='1
   ' OR '1'='1'--
   admin'--
   1' UNION SELECT NULL--
```

**With Intruder**

```
1. Mark injection point
2. Load SQL injection payload list
3. Attack type: Sniper
4. Look for:
   - Different response lengths
   - Error messages
   - Successful authentication
```

### Cross-Site Scripting (XSS)

**Reflected XSS**

```
Test payloads:
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
```

**Stored XSS**

```
1. Find input that gets stored
2. Submit XSS payload
3. Navigate to page displaying input
4. Check if script executes
```

### Authentication Testing

**Brute Force**

```
1. Capture login request
2. Send to Intruder
3. Mark username and password
4. Load wordlists
5. Attack type: Pitchfork or Cluster Bomb
6. Look for different response codes/lengths
```

**Session Management**

```
1. Login and capture session cookie
2. Analyze with Sequencer
3. Test session expiration
4. Test session fixation
5. Test cookie security flags
```

### Access Control

**Horizontal Privilege Escalation**

```
1. Login as User A
2. Access User A's resources
3. Note User A's identifiers
4. Change to User B's identifiers
5. Check if access granted
```

**Vertical Privilege Escalation**

```
1. Login as regular user
2. Access admin functionality
3. Check for authorization bypass
4. Test forced browsing
```

### CSRF (Cross-Site Request Forgery)

**Testing**

```
1. Generate anti-CSRF tokens tool
2. Submit form without token
3. Submit form with wrong token
4. Check if action succeeds
5. Test token validation
```

## 💡 Best Practices

### 1. Define Scope

```
Always define testing scope to:
- Avoid testing out-of-scope targets
- Focus proxy history
- Prevent accidental attacks
```

### 2. Save Your Work (Pro)

```
File → Save project
- Save regularly
- Organize by client/application
- Include notes and findings
```

### 3. Use Target Filters

```
Proxy → Options → Intercept Client Requests
- Only intercept in-scope items
- Exclude static resources (images, CSS, JS)
- Filter by file extension
```

### 4. Organize Testing

```
1. Reconnaissance
2. Map application
3. Analyze attack surface
4. Test vulnerabilities
5. Verify findings
6. Document results
```

### 5. Throttle Attacks

```
Intruder → Options → Request Engine
- Limit threads for stealth
- Add delays between requests
- Respect rate limits
```

## 🔧 Extensions (BApps)

Burp Suite supports extensions via the BApp Store.

### Popular Extensions

**Essential Extensions**

- **Autorize** - Authorization testing
- **Active Scan++** - Additional scan checks
- **Logger++** - Advanced logging
- **Param Miner** - Parameter discovery
- **Turbo Intruder** - Fast Intruder alternative
- **Upload Scanner** - File upload testing
- **Collaborator Everywhere** - Out-of-band testing
- **J2EEScan** - Java application testing

### Installing Extensions

```
Extender → BApp Store
1. Browse available extensions
2. Click Install
3. Configure if needed
4. Access from new tab or context menu
```

### Custom Extensions

```
Extender → Extensions
1. Click Add
2. Select extension type (Java, Python, Ruby)
3. Load extension file
4. Configure settings
```

## 📚 Learning Resources

### Official Resources

- [PortSwigger Web Security Academy](https://portswigger.net/web-security) - Free training
- [Burp Suite Documentation](https://portswigger.net/burp/documentation)
- [PortSwigger Research](https://portswigger.net/research)
- [Daily Swig](https://portswigger.net/daily-swig) - Security news

### Certifications

- **Burp Suite Certified Practitioner (BSCP)**
  - Practical web security exam
  - Uses Burp Suite Professional
  - Highly regarded certification

### Books

- “The Web Application Hacker’s Handbook” by Dafydd Stuttard
- “Web Security Testing Cookbook” by Paco Hope
- “Burp Suite Essentials” by Akash Mahajan

### Practice Platforms

- [PortSwigger Web Security Academy Labs](https://portswigger.net/web-security/all-labs)
- [HackTheBox](https://www.hackthebox.com/)
- [PentesterLab](https://pentesterlab.com/)
- [OWASP WebGoat](https://owasp.org/www-project-webgoat/)
- [DVWA](https://github.com/digininja/DVWA)

### Video Tutorials

- [PortSwigger YouTube Channel](https://www.youtube.com/c/PortSwiggerTV)
- [STÖK - Web Security](https://www.youtube.com/c/STOKfredrik)
- [The Cyber Mentor](https://www.youtube.com/c/TheCyberMentor)

## ⚠️ Common Issues and Solutions

### Issue: Can’t intercept HTTPS traffic

**Solution**:

1. Install Burp CA certificate in browser
1. Verify proxy settings (127.0.0.1:8080)
1. Check Intercept is on
1. Verify browser using proxy

### Issue: Browser shows certificate errors

**Solution**:

- Certificate not installed properly
- Reinstall Burp CA certificate
- Trust certificate in system/browser

### Issue: Slow performance

**Solutions**:

- Increase Java heap size: `java -jar -Xmx4g burpsuite.jar`
- Disable unnecessary extensions
- Limit proxy history size
- Exclude static resources from scope

### Issue: Intruder is slow (Community)

**Explanation**:

- Community Edition is throttled
- Upgrade to Professional for full speed
- Use Python/other tools for heavy brute forcing

### Issue: Can’t save project

**Explanation**:

- Feature only in Professional Edition
- Use temporary projects in Community
- Export specific data (Site map, etc.)

## 🎓 Practical Workflow

### Standard Testing Process

#### Phase 1: Setup

```
1. Configure browser proxy
2. Install SSL certificate
3. Define scope
4. Configure display filters
```

#### Phase 2: Mapping

```
1. Browse application manually
2. Use spider/crawler (Pro)
3. Review site map
4. Identify entry points
```

#### Phase 3: Analysis

```
1. Review HTTP history
2. Analyze parameters
3. Identify technologies
4. Map attack surface
```

#### Phase 4: Testing

```
1. Test for injection flaws
2. Test authentication
3. Test authorization
4. Test session management
5. Test business logic
6. Test for XSS
7. Test file uploads
8. Test APIs
```

#### Phase 5: Verification

```
1. Manually verify findings
2. Eliminate false positives
3. Assess impact
4. Document vulnerabilities
```

#### Phase 6: Reporting

```
1. Generate reports (Pro)
2. Document with screenshots
3. Provide reproduction steps
4. Include remediation advice
```

## 🔒 Security and Ethics

### Legal Considerations

- **Authorization Required**: Only test applications you own or have permission to test
- **Bug Bounty Programs**: Follow program rules and scope
- **Responsible Disclosure**: Report vulnerabilities responsibly
- **Legal Consequences**: Unauthorized testing violates laws (CFAA, etc.)

### Responsible Use

- ✅ Test your own applications
- ✅ Participate in bug bounty programs
- ✅ Practice in intentionally vulnerable apps
- ✅ Educational purposes with permission
- ❌ Never test without authorization
- ❌ Don’t exploit vulnerabilities maliciously
- ❌ Avoid damaging applications
- ❌ Respect data privacy

### Professional Conduct

- Follow scope of engagement
- Document all findings
- Report vulnerabilities promptly
- Maintain client confidentiality
- Provide clear remediation guidance

## 📝 Quick Reference

### Keyboard Shortcuts

```
Ctrl+T          Send to Repeater
Ctrl+I          Send to Intruder
Ctrl+Shift+B    Send to Burp
Ctrl+R          Repeat request in Repeater
Ctrl+Space      Show/hide decoder list
Ctrl+F          Find
Ctrl+E          URL encode
Ctrl+Shift+E    URL decode
```

### Common Proxy Intercept Rules

```
# Intercept only in-scope items
Proxy → Options → Intercept Client Requests
And → URL → Is in target scope

# Exclude images
Proxy → Options → Intercept Client Requests
And → File extension → Matches regex: \.(jpg|png|gif|css|js)$

# Intercept only POST requests
Proxy → Options → Intercept Client Requests
And → Method → Matches regex: POST
```

### Useful Intruder Payloads

```
SQL Injection: /usr/share/wordlists/wfuzz/Injections/SQL.txt
XSS: /usr/share/wordlists/wfuzz/Injections/XSS.txt
Directories: /usr/share/wordlists/dirb/common.txt
Passwords: /usr/share/wordlists/rockyou.txt
```

## 🔗 Related Tools

### Complementary Tools

- **OWASP ZAP**: Alternative web proxy
- **Fiddler**: HTTP debugging proxy
- **Postman**: API testing
- **SQLMap**: Automated SQL injection
- **Nikto**: Web server scanner

### Browser Extensions

- **FoxyProxy**: Proxy management
- **Cookie Editor**: Cookie manipulation
- **Wappalyzer**: Technology detection
- **User-Agent Switcher**: Change user agent

-----

**Last Updated**: October 2025  
**Tool Version**: Burp Suite 2023.x+  
**License**: Community (Free) / Professional (Commercial)  
**Website**: https://portswigger.net/burp
