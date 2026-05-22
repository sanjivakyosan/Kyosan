#!/bin/bash

# Consciousness Framework Auto-Starter
# This script automatically starts the server and opens the browser

set -e

# Configuration
PORT=5001
URL="http://localhost:$PORT"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_SCRIPT="run.py"
VENV_PATH="$PROJECT_DIR/venv"

echo "🧠 Consciousness Framework Auto-Starter"
echo "========================================"

# Function to check if server is running
check_server() {
    if curl -s "$URL/api/units" >/dev/null 2>&1; then
        return 0  # Server is running
    else
        return 1  # Server is not running
    fi
}

# Function to start server
start_server() {
    echo "🚀 Starting consciousness framework server..."
    
    # Change to project directory
    cd "$PROJECT_DIR"
    
    # Activate virtual environment if it exists
    if [ -d "$VENV_PATH" ]; then
        echo "📦 Activating virtual environment..."
        source "$VENV_PATH/bin/activate"
    else
        echo "⚠️  Virtual environment not found at $VENV_PATH"
        echo "   Running with system Python..."
    fi
    
    # Start the server in the background
    echo "🔄 Launching server on port $PORT..."
    nohup python "$SERVER_SCRIPT" > consciousness_server.log 2>&1 &
    SERVER_PID=$!
    
    echo "📝 Server PID: $SERVER_PID"
    echo "$SERVER_PID" > consciousness_server.pid
    
    # Wait for server to start
    echo "⏳ Waiting for server to start..."
    for i in {1..30}; do
        if check_server; then
            echo "✅ Server is ready!"
            return 0
        fi
        sleep 1
        echo -n "."
    done
    
    echo ""
    echo "❌ Server failed to start within 30 seconds"
    echo ""
    echo "🔍 Diagnostic information:"
    echo "   Port: $PORT"
    echo "   Project Directory: $PROJECT_DIR"
    echo "   Server Script: $SERVER_SCRIPT"
    echo "   Virtual Environment: $VENV_PATH"
    echo ""
    echo "📋 Checking server log for errors..."
    if [ -f consciousness_server.log ]; then
        echo "   Last 10 lines of consciousness_server.log:"
        tail -n 10 consciousness_server.log | sed 's/^/   /'
    else
        echo "   No log file found"
    fi
    echo ""
    echo "🔧 Troubleshooting suggestions:"
    echo "   1. Check if port $PORT is already in use: lsof -i :$PORT"
    echo "   2. Verify virtual environment: ls -la $VENV_PATH"
    echo "   3. Check server script: ls -la $SERVER_SCRIPT"
    echo "   4. Try running manually: python $SERVER_SCRIPT"
    echo ""
    return 1
}

# Function to open browser
open_browser() {
    echo "🌐 Opening browser..."
    
    # Detect OS and open browser accordingly
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        open "$URL"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v xdg-open > /dev/null; then
            xdg-open "$URL"
        elif command -v gnome-open > /dev/null; then
            gnome-open "$URL"
        else
            echo "📋 Please open your browser and go to: $URL"
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        # Windows
        start "$URL"
    else
        echo "📋 Please open your browser and go to: $URL"
    fi
}

# Function to stop server
stop_server() {
    echo "🛑 Stopping consciousness framework server..."
    
    if [ -f consciousness_server.pid ]; then
        PID=$(cat consciousness_server.pid)
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            echo "✅ Server stopped (PID: $PID)"
        else
            echo "⚠️  Server with PID $PID is not running"
        fi
        rm -f consciousness_server.pid
    else
        echo "⚠️  PID file not found"
        # Try to find and kill the process
        PROCESS_PID=$(lsof -ti:$PORT 2>/dev/null || true)
        if [ -n "$PROCESS_PID" ]; then
            kill "$PROCESS_PID"
            echo "✅ Server stopped (PID: $PROCESS_PID)"
        else
            echo "ℹ️  No server process found on port $PORT"
        fi
    fi
}

# Function to show server status
show_status() {
    echo "📊 Consciousness Framework Status"
    echo "================================"
    
    if check_server; then
        echo "✅ Server is running at $URL"
        
        if [ -f consciousness_server.pid ]; then
            PID=$(cat consciousness_server.pid)
            echo "📝 Server PID: $PID"
        fi
        
        # Show recent log entries
        if [ -f consciousness_server.log ]; then
            echo ""
            echo "📋 Recent log entries:"
            tail -n 5 consciousness_server.log
        fi
    else
        echo "❌ Server is not running"
    fi
}

# Main logic
case "${1:-start}" in
    "start")
        echo "🔍 Checking if server is already running..."
        if check_server; then
            echo "✅ Server is already running at $URL"
        else
            if start_server; then
                echo "🎉 Server started successfully!"
            else
                echo "❌ Failed to start server"
                exit 1
            fi
        fi
        
        # Always try to open browser
        open_browser
        
        echo ""
        echo "🎯 Consciousness Framework is ready!"
        echo "   📱 Web Interface: $URL"
        echo "   📊 API Endpoint: $URL/api/units"
        echo "   📝 Logs: $PROJECT_DIR/consciousness_server.log"
        echo ""
        echo "💡 Commands:"
        echo "   ./start_consciousness_app.sh stop    - Stop the server"
        echo "   ./start_consciousness_app.sh status  - Check server status"
        echo "   ./start_consciousness_app.sh restart - Restart the server"
        ;;
        
    "stop")
        stop_server
        ;;
        
    "status")
        show_status
        ;;
        
    "restart")
        echo "🔄 Restarting consciousness framework..."
        stop_server
        sleep 2
        if start_server; then
            echo "🎉 Server restarted successfully!"
            open_browser
        else
            echo "❌ Failed to restart server"
            exit 1
        fi
        ;;
        
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        echo ""
        echo "Commands:"
        echo "  start   - Start server and open browser (default)"
        echo "  stop    - Stop the server"
        echo "  status  - Show server status"
        echo "  restart - Restart the server"
        exit 1
        ;;
esac 