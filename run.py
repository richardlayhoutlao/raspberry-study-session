#!/usr/bin/env python3
import subprocess
import sys
import os
import webbrowser
import time
import threading

if __name__ == "__main__":
    # Function to open browser after a delay
    def open_browser():
        time.sleep(2)  # Wait 2 seconds for server to start
        webbrowser.open("http://127.0.0.1:8000/docs")
    
    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Run uvicorn with reload
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--reload"], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
