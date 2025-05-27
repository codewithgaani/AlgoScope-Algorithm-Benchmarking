from datetime import datetime
import sys
import os

# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import save_report, save_report_before_search

def startInsertionSort(data, drawData, stepTime, on_complete, report):
    colorData = ['grey'] * len(data)
    n = len(data)
    i = [1]
    root = drawData.__globals__['root']
    canvas = drawData.__globals__['canvas']

    # Initial draw and before screenshot
    drawData(data, colorData)
    save_report_before_search(report, canvas)

    def step():
        if i[0] < n:
            key = data[i[0]]
            j = [i[0] - 1]
            def inner_step():
                if j[0] >= 0:
                    report['comparisons'] += 1
                    if data[j[0]] > key:
                        data[j[0]+1] = data[j[0]]
                        colorData[j[0]+1] = 'red'
                        drawData(data, colorData)
                        colorData[j[0]+1] = 'grey'
                        report['swaps'] += 1
                        j[0] -= 1
                        root.after(int(stepTime * 1000), inner_step)
                    else:
                        data[j[0]+1] = key
                        colorData[i[0]] = 'green'
                        drawData(data, colorData)
                        i[0] += 1
                        root.after(int(stepTime * 1000), step)
                else:
                    data[j[0]+1] = key
                    colorData[i[0]] = 'green'
                    drawData(data, colorData)
                    i[0] += 1
                    root.after(int(stepTime * 1000), step)
            inner_step()
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

