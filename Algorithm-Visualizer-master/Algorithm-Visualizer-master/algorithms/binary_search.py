from datetime import datetime
import sys
import os

# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import save_report, save_report_before_search

def startBinarySearch(data, drawData, stepTime, on_complete, report, target):
    data.sort()
    n = len(data)
    colorData = ['grey'] * n
    left = [0]
    right = [n - 1]
    found = [False]
    mid = [0]
    root = drawData.__globals__['root']
    canvas = drawData.__globals__['canvas']
    # At the start, highlight the target bar as blue
    if target in data:
        colorData[data.index(target)] = 'blue'
    drawData(data, colorData)
    save_report_before_search(report, canvas)

    def step():
        if left[0] <= right[0]:
            mid[0] = (left[0] + right[0]) // 2
            # Set all to grey except found (green) and target (blue if not found yet)
            for k in range(n):
                if colorData[k] != 'green' and not (k == data.index(target) and not found[0]):
                    colorData[k] = 'grey'
            # Set current checked (mid) bar to red
            if colorData[mid[0]] != 'green':
                colorData[mid[0]] = 'red'
            drawData(data, colorData)
            report['comparisons'] += 1
            def after_compare():
                if data[mid[0]] == target:
                    colorData[mid[0]] = 'green'
                    drawData(data, colorData)
                    found[0] = True
                    report['final_array'] = data[:]
                    report['end_time'] = datetime.now().isoformat()
                    report['duration_sec'] = (datetime.fromisoformat(report['end_time']) - datetime.fromisoformat(report['start_time'])).total_seconds()
                    print(f"Element found at index: {mid[0]}")
                    save_report(report, canvas)
                    on_complete()
                elif data[mid[0]] < target:
                    colorData[mid[0]] = 'grey'
                    left[0] = mid[0] + 1
                    drawData(data, colorData)
                    root.after(int(stepTime * 1000), step)
                else:
                    colorData[mid[0]] = 'grey'
                    right[0] = mid[0] - 1
                    drawData(data, colorData)
                    root.after(int(stepTime * 1000), step)
            root.after(int(stepTime * 1000), after_compare)
        else:
            report['final_array'] = data[:]
            report['end_time'] = datetime.now().isoformat()
            report['duration_sec'] = (datetime.fromisoformat(report['end_time']) - datetime.fromisoformat(report['start_time'])).total_seconds()
            print("Element not found")
            save_report(report, canvas)
            on_complete()
    # Start after a short delay to show the initial blue
    root.after(int(stepTime * 1000), step)

