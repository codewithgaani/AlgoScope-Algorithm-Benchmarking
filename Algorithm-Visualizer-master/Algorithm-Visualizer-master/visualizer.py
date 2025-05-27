from tkinter import *
from tkinter import ttk
import random
import sys
import os
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'algorithms'))

from utils import save_report
from linear_search import startLinearSearch
from binary_search import startBinarySearch
from bubble_sort import startBubbleSort
from insertion_sort import startInsertionSort
from selection_sort import startSelectionSort
from merge_sort import startMergeSort

data = []
colorData = []

FONT = ("Segoe UI", 14, "bold")
current_theme_name = "Forest Fusion"

THEMES = {
    "Forest Fusion": {
        "bg": "#2d6a4f", "fg": "#f1faee", "bar": "#52b788", "checked": "#e63946", "found": "#a7c957",
        "current": "#40916c", "border": "#1b4332", "button": "#40916c", "button_fg": "#f1faee",
        "trough": "#14532d"
    },
    "Tropical Fusion": {
        "bg": "#ffb4a2", "fg": "#22223b", "bar": "#f28482", "checked": "#9d0208", "found": "#6a994e",
        "current": "#ff006e", "border": "#9d0208", "button": "#f28482", "button_fg": "#22223b",
        "trough": "#9d0208"
    },
    "Ice Burst": {
        "bg": "#f8f9fa", "fg": "#222831", "bar": "#1e90ff", "checked": "#ff7675", "found": "#00b894",
        "current": "#0984e3", "border": "#dfe6e9", "button": "#dfe6e9", "button_fg": "#222831",
        "trough": "#adb5bd"
    },
    "Blueberry Variance": {
        "bg": "#23272e", "fg": "#f5f6fa", "bar": "#70a1ff", "checked": "#ff7675", "found": "#00b894",
        "current": "#5352ed", "border": "#393e46", "button": "#393e46", "button_fg": "#f5f6fa",
        "trough": "#2f3542"
    },
    "igen": {
        "bg": "#1e3d59", "fg": "#f5f0e1", "bar": "#28b5b5", "checked": "#f76b8a", "found": "#38b000",
        "current": "#3aafa9", "border": "#0b2b43", "button": "#3aafa9", "button_fg": "#f5f0e1",
        "trough": "#0b2b43"
    }
}
current_theme = THEMES[current_theme_name]

def apply_theme():
    root.config(bg=current_theme["bg"])
    titlef.config(bg=current_theme["bg"])
    sizel.config(bg=current_theme["bg"], fg=current_theme["fg"])
    delayl.config(bg=current_theme["bg"], fg=current_theme["fg"])
    title_label.config(bg=current_theme["bg"], fg=current_theme["fg"])
    topf.config(bg=current_theme["bg"])
    canvas.config(bg=current_theme["bg"], highlightbackground=current_theme["border"])
    target_label.config(bg=current_theme["bg"], fg=current_theme["fg"])

    for widget in topf.winfo_children():
        if isinstance(widget, Label):
            widget.config(bg=current_theme["bg"], fg=current_theme["fg"], font=FONT)
        elif isinstance(widget, Button):
            widget.config(bg=current_theme["button"], fg=current_theme["button_fg"], font=FONT)

    for widget in titlef.winfo_children():
        if isinstance(widget, Button):
            widget.config(bg=current_theme["button"], fg=current_theme["button_fg"], font=FONT)

    speed_scale.config(bg=current_theme["bg"], fg=current_theme["fg"], troughcolor=current_theme["trough"])
    size_scale.config(bg=current_theme["bg"], fg=current_theme["fg"], troughcolor=current_theme["trough"])

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TCombobox', fieldbackground=current_theme["button"], background=current_theme["button"],
                    foreground=current_theme["button_fg"], font=FONT, borderwidth=0)
    style.map('TCombobox', fieldbackground=[('readonly', current_theme["button"])])
    style.configure('TButton', background=current_theme["button"], foreground=current_theme["button_fg"], font=FONT)

def disable_buttons():
    for widget in topf.winfo_children():
        if isinstance(widget, Button):
            widget.config(state=DISABLED)
    for widget in titlef.winfo_children():
        if isinstance(widget, Button):
            widget.config(state=DISABLED)

def enable_buttons():
    for widget in topf.winfo_children():
        if isinstance(widget, Button):
            widget.config(state=NORMAL)
    for widget in titlef.winfo_children():
        if isinstance(widget, Button):
            widget.config(state=NORMAL)

def visualize(algorithm, stepTime):
    stepTime /= 10
    disable_buttons()
    initial_array = data[:]
    report = {
        'algorithm': algorithm, 'size': len(data), 'step_delay_sec': stepTime,
        'initial_array': initial_array, 'comparisons': 0, 'swaps': 0,
        'start_time': datetime.now().isoformat()
    }

    def done(): enable_buttons()

    if algorithm == "Linear Search":
        if not data: done(); return
        target = random.choice(data)
        target_label.config(text=f"Searching for: {target}")
        startLinearSearch(data, drawData, stepTime, done, report, target)
    elif algorithm == "Binary Search":
        if not data: done(); return
        sorted_data = sorted(data)
        target = random.choice(sorted_data)
        data[:] = sorted_data
        target_label.config(text=f"Searching for: {target}")
        startBinarySearch(data, drawData, stepTime, done, report, target)
    elif algorithm == "Bubble Sort":
        target_label.config(text="")
        startBubbleSort(data, drawData, stepTime, done, report)
    elif algorithm == "Selection Sort":
        target_label.config(text="")
        startSelectionSort(data, drawData, stepTime, done, report)
    elif algorithm == "Insertion Sort":
        target_label.config(text="")
        startInsertionSort(data, drawData, stepTime, done, report)
    elif algorithm == "Merge Sort":
        target_label.config(text="")
        startMergeSort(data, drawData, stepTime, done, report)
    else:
        done()

def genData(data_size):
    global data, colorData
    data = [random.randint(1, 100) for _ in range(int(data_size))]
    colorData = [current_theme["bar"] for _ in data]
    drawData(data, colorData)
    sizel.config(text=str(format(int(data_size), "0>3d")))

def drawData(data, colorData):
    canvas.delete("all")
    canvas_h = canvas.winfo_height()
    canvas_w = canvas.winfo_width()
    spacing = 2
    rect_w = (canvas_w - spacing * (len(data) - 1)) / len(data) if data else 0
    max_val = max(data) if data else 1
    for i, val in enumerate(data):
        height = val / max_val
        x0 = i * rect_w + (i + 1) * spacing
        y0 = canvas_h - height * (canvas_h - 20)
        x1 = (i + 1) * rect_w + (i + 1) * spacing
        y1 = canvas_h
        canvas.create_rectangle(x0+2, y0+2, x1+2, y1+2, fill=current_theme["border"], outline="")
        canvas.create_rectangle(x0, y0, x1, y1, fill=colorData[i], outline="")
    root.update_idletasks()

def dispDelay(delay):
    delayl.config(text=str(format(float(delay)/10, ">03.1f") + " sec"))

def set_theme(theme_name):
    global current_theme_name, current_theme, colorData
    current_theme_name = theme_name
    current_theme = THEMES[theme_name]
    apply_theme()
    colorData = [current_theme["bar"] for _ in data]
    drawData(data, colorData)

def main():
    global root, titlef, delayl, sizel, theme_menu, speed_scale, size_scale, target_label, title_label, topf, canvas, size, speed

    root = Tk()
    root.title("Algorithm Visualizer")
    root.config(bg=current_theme["bg"])
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)

    titlef = Frame(root, bg=current_theme["bg"])
    titlef.grid(row=0, column=0, sticky="ew")

    sizel = Label(titlef, text="050", bg=current_theme["bg"], fg=current_theme["fg"], font=FONT)
    sizel.pack(side=LEFT, padx=(10, 200))

    title_label = Label(titlef, text="Algorithms Visualizer", bg=current_theme["bg"], fg=current_theme["fg"],
                        font=(FONT[0], 20, "bold"))
    title_label.pack(pady=10, side=LEFT)

    delayl = Label(titlef, text="0.0 sec", bg=current_theme["bg"], fg=current_theme["fg"], font=FONT)
    delayl.pack(side=LEFT, padx=(190, 10))

    theme_var = StringVar(value=current_theme_name)
    theme_menu = ttk.Combobox(titlef, textvariable=theme_var, state='readonly', values=list(THEMES.keys()), font=FONT, width=16)
    theme_menu.pack(side=LEFT, padx=(20, 10))
    theme_menu.bind("<<ComboboxSelected>>", lambda event: set_theme(theme_var.get()))

    topf = Frame(root, bg=current_theme["bg"])
    topf.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    size = IntVar()
    speed = IntVar()
    size.set(50)
    speed.set(0)

    Label(topf, text="Step Delay (sec)", bg=current_theme["bg"], fg=current_theme["fg"], font=FONT).grid(row=0, column=0, padx=5, pady=5, sticky=E)
    speed_scale = Scale(topf, variable=speed, from_=0, to=10, orient=HORIZONTAL, command=dispDelay,
                        bg=current_theme["bg"], fg=current_theme["fg"], troughcolor=current_theme["trough"],
                        highlightthickness=0, bd=0, sliderrelief=FLAT, font=FONT, length=180)
    speed_scale.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    algorithm = StringVar()
    Label(topf, text="Select Algorithm", bg=current_theme["bg"], fg=current_theme["fg"], font=FONT).grid(row=0, column=3, padx=(50, 0), pady=5, sticky=E)
    algorithm_menu = ttk.Combobox(topf, textvariable=algorithm, state='readonly',
                                  values=['Linear Search', 'Binary Search', 'Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort'],
                                  font=FONT)
    algorithm_menu.grid(row=0, column=4, padx=5, pady=5, sticky=W)
    algorithm_menu.current(0)

    Label(topf, text="Size", bg=current_theme["bg"], fg=current_theme["fg"], font=FONT).grid(row=1, column=0, padx=5, pady=5, sticky=E)
    size_scale = Scale(topf, variable=size, from_=3, to=100, orient=HORIZONTAL, command=genData,
                       bg=current_theme["bg"], fg=current_theme["fg"], troughcolor=current_theme["trough"],
                       highlightthickness=0, bd=0, sliderrelief=FLAT, font=FONT, length=180)
    size_scale.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    Button(topf, text="Visualise", bg=current_theme["button"], fg=current_theme["button_fg"],
           command=lambda: visualize(algorithm.get(), speed.get()), font=FONT).grid(row=1, column=3, padx=(50, 0), pady=5, ipadx=10, sticky=W)

    target_label = Label(root, text="", bg=current_theme["bg"], fg=current_theme["fg"], font=(FONT[0], 16, "bold"))
    target_label.grid(row=2, column=0, sticky="nsew")

    canvas = Canvas(root, bg=current_theme["bg"], highlightbackground=current_theme["border"])
    canvas.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
    canvas.bind("<Configure>", lambda event: drawData(data, colorData))

    genData(50)
    root.mainloop()

if __name__ == "__main__":
    main()
