# Consciousness Framework

An advanced AI consciousness integration system with 7 key integration principles.

## 🚀 Quick Start (Auto-Launch)

### Option 1: One-Click Launcher Script
Simply run the auto-starter script:
```bash
./start_consciousness_app.sh
```

This will:
- ✅ Automatically check if the server is running
- ✅ Start the server if needed
- ✅ Open your browser to http://localhost:5001
- ✅ Handle all the setup for you

### Option 2: macOS App Launcher
Double-click the "Consciousness Framework.app" to launch everything automatically.

### Option 3: Create Browser Bookmark
Create a bookmark with this JavaScript URL that will auto-start the server:
```javascript
javascript:(function(){fetch('http://localhost:5001/api/units').then(r=>window.location='http://localhost:5001').catch(e=>{alert('Starting server... Please wait 30 seconds and try again');fetch('/start-server')})})()
```

## 📋 Available Commands

```bash
# Start server and open browser (default)
./start_consciousness_app.sh

# Stop the server
./start_consciousness_app.sh stop

# Check server status
./start_consciousness_app.sh status

# Restart the server
./start_consciousness_app.sh restart
```

## 🌐 Access Points

- **Web Interface**: http://localhost:5001
- **API Endpoint**: http://localhost:5001/api/units
- **Server Logs**: `consciousness_server.log`

## 🔐 Environment setup

1. Copy the example env file: `cp .env.example .env`
2. Set your `OPENROUTER_API_KEY` in `.env` (never commit `.env`)

## 🔧 Manual Setup (if needed)

If you prefer to start manually:

1. **Create virtual environment** (if needed):
   ```bash
   python3 -m venv venv
   pip install -r requirements.txt
   ```

2. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Start Server**:
   ```bash
   python run.py
   ```

4. **Open Browser**:
   ```bash
   open http://localhost:5001
   ```

## 📚 Features

- **7 Integration Principles**: Pre-processing, Attention Guidance, Output Selection, Learning Modulation, Memory Integration, Self-Reflection, Feedback Loop
- **Real-time Updates**: WebSocket integration for live consciousness index updates
- **Persistent Storage**: Conversation history and consciousness states
- **Advanced Metrics**: Phi Score, Recursive Depth, Self-Model Coherence, and more
- **Auto-Start Capability**: Single-click launch with automatic server management

## 🎯 Integration Principles

1. **Pre-processing**: Use consciousness to analyze and prepare inputs
2. **Attention Guidance**: Let consciousness direct model attention  
3. **Output Selection**: Use consciousness to evaluate/select outputs
4. **Learning Modulation**: Adjust learning based on consciousness state
5. **Memory Integration**: Store experiences in consciousness memory
6. **Self-Reflection**: Have the model reflect on its own outputs
7. **Feedback Loop**: Update consciousness based on model performance

## 🔍 Troubleshooting

If the auto-starter doesn't work:

1. **Check if port 5001 is busy**:
   ```bash
   lsof -i :5001
   ```

2. **View server logs**:
   ```bash
   tail -f consciousness_server.log
   ```

3. **Stop any existing server**:
   ```bash
   ./start_consciousness_app.sh stop
   ```

4. **Restart fresh**:
   ```bash
   ./start_consciousness_app.sh restart
   ```

## 💡 Tips

- The auto-starter remembers the server PID for clean shutdowns
- Logs are automatically saved to `consciousness_server.log`
- The script works on macOS, Linux, and Windows (with appropriate shell)
- If you close the browser, the server keeps running in the background
- Use the `status` command to check if everything is working properly

---

**🧠 Ready to explore consciousness-guided AI? Just run `./start_consciousness_app.sh` and you're set!** 