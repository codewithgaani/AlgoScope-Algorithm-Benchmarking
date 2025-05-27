from datetime import datetime
import sys
import os

# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import save_report, save_report_before_search

def startSelectionSort(data, drawData, stepTime, on_complete, report):
    colorData = ['grey'] * len(data)
    n = len(data)
    i = [0]
    j = [1]
    min_idx = [0]
    root = drawData.__globals__['root']
    canvas = drawData.__globals__['canvas']

    # Initial draw and before screenshot
    drawData(data, colorData)
    save_report_before_search(report, canvas)

    def step():
        if i[0] < n - 1:
            if j[0] < n:
                colorData[min_idx[0]] = 'blue'
                colorData[j[0]] = 'white'
                drawData(data, colorData)
                report['comparisons'] += 1
                def after_compare():
                    colorData[j[0]] = 'grey'
                    if data[j[0]] < data[min_idx[0]]:
                        colorData[min_idx[0]] = 'grey'
                        min_idx[0] = j[0]
                    j[0] += 1
                    root.after(int(stepTime * 1000), step)
                root.after(int(stepTime * 1000), after_compare)
            else:
                data[i[0]], data[min_idx[0]] = data[min_idx[0]], data[i[0]]
                colorData[min_idx[0]] = colorData[i[0]] = 'red'
                drawData(data, colorData)
                report['swaps'] += 1
                def after_swap():
                    colorData[min_idx[0]] = colorData[i[0]] = 'green'
                    drawData(data, colorData)
                    i[0] += 1
                    j[0] = i[0] + 1
                    min_idx[0] = i[0]
                    root.after(int(stepTime * 1000), step)
                root.after(int(stepTime * 1000), after_swap)
        else:
            for k in range(n):
                colorData[k] = 'green'
            drawData(data, colorData)
            report['final_array'] = data[:]
            report['end_time'] = datetime.now().isoformat()
            report['duration_sec'] = (datetime.fromisoformat(report['end_time']) - datetime.fromisoformat(report['start_time'])).total_seconds()
            save_report(report, canvas)
            on_complete()
    step()