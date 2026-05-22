#!/bin/bash

# Setup script for auto-starting Consciousness Framework on macOS

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_FILE="$HOME/Library/LaunchAgents/com.consciousness.framework.plist"

echo "🔧 Consciousness Framework Auto-Start Setup"
echo "==========================================="

# Function to create launchd plist
create_plist() {
    echo "📝 Creating launchd service..."
    
    mkdir -p "$HOME/Library/LaunchAgents"
    
    cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.consciousness.framework</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PROJECT_DIR/start_consciousness_app.sh</string>
        <string>start</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
    <key>RunAtLoad</key>
    <false/>
    <key>KeepAlive</key>
    <false/>
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/consciousness_autostart.log</string>
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/consciousness_autostart.log</string>
</dict>
</plist>
EOF

    echo "✅ Service file created at: $PLIST_FILE"
}

# Function to install the service
install_service() {
    echo "🚀 Installing auto-start service..."
    
    # Load the service
    launchctl load "$PLIST_FILE"
    
    echo "✅ Service installed successfully!"
    echo ""
    echo "📋 Available commands:"
    echo "   launchctl start com.consciousness.framework    - Start the service"
    echo "   launchctl stop com.consciousness.framework     - Stop the service"
    echo "   launchctl unload '$PLIST_FILE'  - Uninstall the service"
}

# Function to uninstall the service
uninstall_service() {
    echo "🗑️  Uninstalling auto-start service..."
    
    if [ -f "$PLIST_FILE" ]; then
        launchctl unload "$PLIST_FILE" 2>/dev/null || true
        rm "$PLIST_FILE"
        echo "✅ Service uninstalled successfully!"
    else
        echo "ℹ️  Service not found."
    fi
}

# Function to show status
show_service_status() {
    echo "📊 Auto-Start Service Status"
    echo "============================"
    
    if [ -f "$PLIST_FILE" ]; then
        echo "✅ Service is installed"
        echo "📁 Service file: $PLIST_FILE"
        
        # Check if service is loaded
        if launchctl list | grep -q "com.consciousness.framework"; then
            echo "🟢 Service is loaded and ready"
        else
            echo "🟡 Service is installed but not loaded"
            echo "   Run: launchctl load '$PLIST_FILE'"
        fi
    else
        echo "❌ Service is not installed"
        echo "   Run: $0 install"
    fi
}

# Main logic
case "${1:-help}" in
    "install")
        create_plist
        install_service
        echo ""
        echo "🎉 Auto-start service is now installed!"
        echo "🌐 You can now start the Consciousness Framework with:"
        echo "   launchctl start com.consciousness.framework"
        ;;
        
    "uninstall")
        uninstall_service
        ;;
        
    "status")
        show_service_status
        ;;
        
    "help"|*)
        echo "Usage: $0 {install|uninstall|status}"
        echo ""
        echo "Commands:"
        echo "  install   - Install auto-start service"
        echo "  uninstall - Remove auto-start service" 
        echo "  status    - Show service status"
        echo ""
        echo "After installation, you can control the service with:"
        echo "  launchctl start com.consciousness.framework"
        echo "  launchctl stop com.consciousness.framework"
        ;;
esac 