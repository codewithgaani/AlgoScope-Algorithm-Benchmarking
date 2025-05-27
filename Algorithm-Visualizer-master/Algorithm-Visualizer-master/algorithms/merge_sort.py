from datetime import datetime
import sys
import os

# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils import save_report, save_report_before_search


def startMergeSort(data, drawData, stepTime, on_complete, report):
    colorData = ['grey'] * len(data)
    n = len(data)
    root = drawData.__globals__['root']
    canvas = drawData.__globals__['canvas']

    # Initial draw and before screenshot
    drawData(data, colorData)
    save_report_before_search(report, canvas)

    def merge_sort_gen(arr, l, r):
        if l >= r:
            return
        m = (l + r) // 2
        yield from merge_sort_gen(arr, l, m)
        yield from merge_sort_gen(arr, m + 1, r)
        yield from merge_gen(arr, l, m, r)

    def merge_gen(arr, l, m, r):
        left = arr[l:m+1]
        right = arr[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            report['comparisons'] += 1
            # Highlight bars being compared
            for idx in range(len(arr)):
                if idx == k:
                    colorData[idx] = 'white'
                else:
                    colorData[idx] = 'grey'
            drawData(arr, colorData)
            yield
            if left[i] <= right[j]:
                arr[k] = left[i]
                report['swaps'] += 1
                i += 1
            else:
                arr[k] = right[j]
                report['swaps'] += 1
                j += 1
            k += 1
        while i < len(left):
            arr[k] = left[i]
            report['swaps'] += 1
            for idx in range(len(arr)):
                if idx == k:
                    colorData[idx] = 'white'
                else:
                    colorData[idx] = 'grey'
            drawData(arr, colorData)
            yield
            i += 1
            k += 1
        while j < len(right):
            arr[k] = right[j]
            report['swaps'] += 1
            for idx in range(len(arr)):
                if idx == k:
                    colorData[idx] = 'white'
                else:
                    colorData[idx] = 'grey'
            drawData(arr, colorData)
            yield
            j += 1
            k += 1

    gen = merge_sort_gen(data, 0, n-1)

    def animate():
        try:
            next(gen)
            root.after(int(stepTime * 1000), animate)
        except StopIteration:
            for i in range(n):
                colorData[i] = 'green'
            drawData(data, colorData)
            report['final_array'] = data[:]
            report['end_time'] = datetime.now().isoformat()
            report['duration_sec'] = (datetime.fromisoformat(report['end_time']) - datetime.fromisoformat(report['start_time'])).total_seconds()
            save_report(report, canvas)
            on_complete()
    animate()


def merge(data,start,end,drawData,stepTime):
    i=start
    j=(start+end)//2+1
    a=[]
    while i<=(start+end)//2 and j<=end:
        colorData[i]=colorData[j]='blue'
        drawData(data,colorData)
        colorData[i]=colorData[j]='grey'
        sleep(stepTime)
        if data[i]<data[j]:
            colorData[i]='green'
            drawData(data,colorData)
            sleep(stepTime)
            colorData[i]='grey'
            a.append(data[i])
            i+=1
        else:
            colorData[j]='green'
            drawData(data,colorData)
            sleep(stepTime)
            colorData[j]='grey'
            a.append(data[j])
            j+=1
    
    while i<=(start+end)//2:
        colorData[i]='green'
        drawData(data,colorData)
        sleep(stepTime)
        colorData[i]='grey'
        a.append(data[i])
        i+=1
    
    while j<=end:
        colorData[j]='green'
        drawData(data,colorData)
        sleep(stepTime)
        colorData[j]='grey'
        a.append(data[j])
        j+=1
    for x in range(start,end+1):
        data[x]=a[x-start]



def mergeSort(data,start,end,drawData,stepTime):
    
    if start>=end:
        return

    colorData[start:end+1]=['white' for x in range(start,end+1)]
    drawData(data,colorData)
    sleep(stepTime)
    colorData[start:end+1]=['grey' for x in range(start,end+1)]


    mergeSort(data,start,(start+end)//2,drawData,stepTime)
    mergeSort(data,(start+end)//2+1,end,drawData,stepTime)
    merge(data,start,end,drawData,stepTime)


    colorData[start:end+1]=['white' for x in range(start,end+1)]
    drawData(data,colorData)
    sleep(stepTime)
    colorData[start:end+1]=['grey' for x in range(start,end+1)]
    # for x in range(start,end+1):
    #     drawData(data,colorData)
    #     sleep(stepTime)
