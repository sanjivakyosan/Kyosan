-- Consciousness Framework Desktop Launcher
-- This AppleScript launches the Consciousness Framework

on run
    set projectPath to "/Users/sanjivakyosan/Desktop/spiegle im spiegle"
    
    -- Display a nice starting message
    display dialog "🧠 Starting Consciousness Framework..." with title "Consciousness Framework" with icon note buttons {"Cancel", "Start"} default button "Start"
    
    if button returned of result is "Start" then
        try
            -- Check if project directory exists
            do shell script "test -d '" & projectPath & "'"
            
            -- Check if startup script exists
            do shell script "test -f '" & projectPath & "/start_consciousness_app.sh'"
            
            -- Launch the consciousness framework
            tell application "Terminal"
                activate
                do script "cd '" & projectPath & "' && ./start_consciousness_app.sh"
            end tell
            
            -- Optional: Show success message
            display dialog "🎉 Consciousness Framework is starting!" with title "Success" with icon note buttons {"OK"} default button "OK" giving up after 3
            
        on error errorMessage
            -- Handle errors gracefully
            display dialog "❌ Error starting Consciousness Framework: " & errorMessage with title "Error" with icon stop buttons {"OK"} default button "OK"
        end try
    end if
end run 