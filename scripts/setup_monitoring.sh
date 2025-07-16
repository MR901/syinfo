#!/bin/bash
# SyInfo Monitoring Setup Script
# Sets up monitoring system with proper permissions and configuration

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SYINFO_DIR="/usr/local/syinfo"
MONITORING_DIR="/var/log/syinfo/monitoring"
CONFIG_DIR="/etc/syinfo"
CRON_USER="root"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}                    SyInfo Monitoring Setup${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}❌ This script must be run as root${NC}"
   echo "   Please run: sudo $0"
   exit 1
fi

# Check OS compatibility
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}❌ This script is designed for Linux systems${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 System Information:${NC}"
echo "   OS: $(lsb_release -d | cut -f2)"
echo "   Kernel: $(uname -r)"
echo "   Architecture: $(uname -m)"
echo ""

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p "$MONITORING_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "/var/log/syinfo"

# Set proper permissions
echo -e "${YELLOW}🔐 Setting permissions...${NC}"
chown -R root:root "$MONITORING_DIR"
chmod 755 "$MONITORING_DIR"
chown -R root:root "$CONFIG_DIR"
chmod 755 "$CONFIG_DIR"
chown -R root:root "/var/log/syinfo"
chmod 755 "/var/log/syinfo"

echo -e "${GREEN}✅ Directories created and permissions set${NC}"

# Install system dependencies
echo -e "${YELLOW}📦 Installing system dependencies...${NC}"
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    apt-get update
    apt-get install -y python3-pip cron net-tools
elif command -v yum &> /dev/null; then
    # CentOS/RHEL
    yum install -y python3-pip cronie net-tools
elif command -v dnf &> /dev/null; then
    # Fedora
    dnf install -y python3-pip cronie net-tools
else
    echo -e "${RED}❌ Unsupported package manager${NC}"
    exit 1
fi

echo -e "${GREEN}✅ System dependencies installed${NC}"

# Install Python dependencies
echo -e "${YELLOW}🐍 Installing Python dependencies...${NC}"
pip3 install --upgrade pip
pip3 install psutil pandas matplotlib seaborn pyyaml

echo -e "${GREEN}✅ Python dependencies installed${NC}"

# Copy configuration files
echo -e "${YELLOW}⚙️  Setting up configuration...${NC}"
if [ -f "config/monitoring.yaml" ]; then
    cp config/monitoring.yaml "$CONFIG_DIR/"
    chmod 644 "$CONFIG_DIR/monitoring.yaml"
    echo -e "${GREEN}✅ Configuration file copied${NC}"
else
    echo -e "${YELLOW}⚠️  Configuration file not found, using defaults${NC}"
fi

# Create logrotate configuration
echo -e "${YELLOW}📝 Creating logrotate configuration...${NC}"
cat > /etc/logrotate.d/syinfo-monitoring << EOF
/var/log/syinfo/monitoring.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        systemctl reload rsyslog >/dev/null 2>&1 || true
    endscript
}
EOF

echo -e "${GREEN}✅ Logrotate configuration created${NC}"

# Generate cron template
echo -e "${YELLOW}⏰ Generating cron job template...${NC}"
cat > /tmp/syinfo_cron_template << EOF
# SyInfo Monitoring Cron Jobs
# Generated on: $(date)
# Add these lines to your crontab using: crontab -e

# System monitoring (every minute)
* * * * * cd $MONITORING_DIR && python3 -m syinfo.monitoring.core.monitor --system --config $CONFIG_DIR/monitoring.yaml --output-dir $MONITORING_DIR >> $MONITORING_DIR/monitoring.log 2>&1

# Process monitoring (every minute)
* * * * * cd $MONITORING_DIR && python3 -m syinfo.monitoring.core.monitor --process --config $CONFIG_DIR/monitoring.yaml --output-dir $MONITORING_DIR >> $MONITORING_DIR/monitoring.log 2>&1

# Cleanup old data (daily at 2 AM)
0 2 * * * find $MONITORING_DIR -name "*.csv" -mtime +7 -delete >> $MONITORING_DIR/cleanup.log 2>&1

# Log rotation (weekly on Sunday at 3 AM)
0 3 * * 0 logrotate /etc/logrotate.d/syinfo-monitoring >> $MONITORING_DIR/logrotate.log 2>&1
EOF

echo -e "${GREEN}✅ Cron template generated${NC}"

# Test monitoring functionality
echo -e "${YELLOW}🧪 Testing monitoring functionality...${NC}"
if python3 -c "import syinfo.monitoring" 2>/dev/null; then
    echo -e "${GREEN}✅ Monitoring module import successful${NC}"
else
    echo -e "${RED}❌ Monitoring module import failed${NC}"
    echo "   Please ensure all dependencies are installed correctly"
fi

# Final instructions
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 SyInfo Monitoring Setup Completed Successfully!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}📋 Next Steps:${NC}"
echo "   1. Review the cron template at: /tmp/syinfo_cron_template"
echo "   2. Add monitoring jobs to crontab:"
echo "      sudo crontab -e"
echo "   3. Copy the contents from /tmp/syinfo_cron_template"
echo ""
echo -e "${YELLOW}📁 Important Directories:${NC}"
echo "   Monitoring data: $MONITORING_DIR"
echo "   Configuration: $CONFIG_DIR"
echo "   Logs: /var/log/syinfo/monitoring.log"
echo ""
echo -e "${YELLOW}🔧 Manual Commands:${NC}"
echo "   Start monitoring: syinfo --monitor --monitor-interval 60"
echo "   View system info: syinfo -s"
echo "   Analyze data: syinfo analyze --data-file <file> --report"
echo ""
echo -e "${YELLOW}📞 Support:${NC}"
echo "   Email: mohitrajput901@gmail.com"
echo "   GitHub: https://github.com/MR901/syinfo"
echo ""
echo -e "${GREEN}✅ Setup completed!${NC}" 