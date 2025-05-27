import os
import json
from datetime import datetime
from PIL import ImageGrab
import tkinter as tk

def take_screenshot(canvas, timestamp, prefix):
    """Take a screenshot of the canvas and save it."""
    # Ensure the canvas is updated
    canvas.update()
    
    # Get canvas coordinates
    x = canvas.winfo_rootx()
    y = canvas.winfo_rooty()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    
    # Take screenshot
    screenshot = ImageGrab.grab(bbox=(x, y, x1, y1))
    
    # Create filename
    filename = f"reports/screenshot_{prefix}_{timestamp}.png"
    
    # Save screenshot
    screenshot.save(filename)
    return filename

def save_report_before_search(report_data, canvas):
    os.makedirs("reports", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_before = take_screenshot(canvas, timestamp, "before")
    report_data['screenshot_before'] = screenshot_before
    report_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_data['__ss_timestamp'] = timestamp  # store for after screenshot

def save_report(report_data, canvas):
    """Save report data and screenshots."""
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    
    # Use the same timestamp as before screenshot if available
    timestamp = report_data.get('__ss_timestamp') or datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Take screenshots
    screenshot_after = take_screenshot(canvas, timestamp, "after")
    
    # Add screenshot paths to report
    report_data['screenshot_after'] = f"reports/screenshot_after_{timestamp}.png"
    
    # Remove helper key
    if '__ss_timestamp' in report_data:
        del report_data['__ss_timestamp']
    
    # Save report
    filename = f"reports/report_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(report_data, f, indent=4) 