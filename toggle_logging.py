#!/usr/bin/env python
"""Toggle Django logging on/off"""

import os
import sys

def toggle_logging(enable=True):
    """Enable or disable Django file logging"""
    
    settings_file = "core/settings.py"
    
    if not os.path.exists(settings_file):
        print("Settings file not found!")
        return
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    if enable:
        # Enable logging by uncommenting
        content = content.replace("# LOGGING = {", "LOGGING = {")
        content = content.replace("# 'version':", "'version':")
        print("✅ Django file logging ENABLED")
        print("📁 Log location: logs/django.log")
        print("📝 Error logs will be written to file")
    else:
        # Disable logging by commenting out
        content = content.replace("LOGGING = {", "# LOGGING = {")
        content = content.replace("'version':", "# 'version':")
        print("❌ Django file logging DISABLED")
        print("📺 Errors will only show in console")
    
    with open(settings_file, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1].lower()
        if action in ['on', 'enable', 'true', '1']:
            toggle_logging(True)
        elif action in ['off', 'disable', 'false', '0']:
            toggle_logging(False)
        else:
            print("Usage: python toggle_logging.py [on|off]")
    else:
        print("Django Logging Control")
        print("Usage:")
        print("  python toggle_logging.py on   # Enable file logging")
        print("  python toggle_logging.py off  # Disable file logging")
        print("")
        print("Current log location: logs/django.log")