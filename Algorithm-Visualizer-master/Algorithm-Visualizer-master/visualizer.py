from tkinter import *
from tkinter import ttk
import random
import sys
import os
from datetime import datetime
import json

# Get the directory containing visualizer.py
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add both current directory and algorithms directory to Python path
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

target_label = None  # Will be set in main()

# Modern font
FONT = ("Segoe UI", 14, "bold")

# Theme definitions
THEMES = {
    "Forest Fusion": {
        "bg": "#2d6a4f",
        "fg": "#f1faee",
        "bar": "#52b788",
        "checked": "#e63946",
        "found": "#a7c957",
        "current": "#40916c",
        "border": "#1b4332",
        "button": "#40916c",
        "button_fg": "#f1faee"
    },
    "Tropical Fusion": {
        "bg": "#ffb4a2",
        "fg": "#22223b",
        "bar": "#f28482",
        "checked": "#9d0208",
        "found": "#6a994e",
        "current": "#ff006e",
        "border": "#ffb4a2",
        "button": "#f28482",
        "button_fg": "#22223b"
    },
    "Ice Burst": {
        "bg": "#f8f9fa",
        "fg": "#222831",
        "bar": "#1e90ff",
        "checked": "#ff7675",
        "found": "#00b894",
        "current": "#0984e3",
        "border": "#dfe6e9",
        "button": "#dfe6e9",
        "button_fg": "#222831"
    },
    "Blueberry Variance": {
        "bg": "#23272e",
        "fg": "#f5f6fa",
        "bar": "#70a1ff",
        "checked": "#ff7675",
        "found": "#00b894",
        "current": "#5352ed",
        "border": "#393e46",
        "button": "#393e46",
        "button_fg": "#f5f6fa"
    },
    "igen": {
        "bg": "#1e3d59",
        "fg": "#f5f0e1",
        "bar": "#28b5b5",
        "checked": "#f76b8a",
        "found": "#38b000",
        "current": "#3aafa9",
        "border": "#1e3d59",
        "button": "#3aafa9",
        "button_fg": "#f5f0e1"
    }
}
current_theme_name = "Forest Fusion"
current_theme = THEMES[current_theme_name]

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def interpolate_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return rgb_to_hex((r, g, b))

def apply_theme():
    root.config(bg=current_theme["bg"])
    titlef.config(bg=current_theme["bg"], highlightthickness=0, bd=0)
    sizel.config(bg=current_theme["bg"], fg=current_theme["fg"])
    delayl.config(bg=current_theme["bg"], fg=current_theme["fg"])
    topf.config(bg=current_theme["bg"], highlightthickness=0, bd=0)
    canvas.config(bg=current_theme["bg"], highlightbackground=current_theme["border"], highlightthickness=0, bd=0)
    for widget in topf.winfo_children():
        if isinstance(widget, Label):
            widget.config(bg=current_theme["bg"], fg=current_theme["fg"], font=FONT)
        elif isinstance(widget, Button):
            widget.config(bg=current_theme["button"], fg=current_theme["button_fg"], font=FONT)
    for widget in titlef.winfo_children():
        if isinstance(widget, Button):
            widget.config(bg=current_theme["button"], fg=current_theme["button_fg"], font=FONT)
    # Update classic Scale widgets for theme
    speed_scale.config(bg=current_theme["bg"], fg=current_theme["fg"], troughcolor=current_theme["border"])
    size_scale.config(bg=current_theme["bg"], fg=current_theme["fg"], troughcolor=current_theme["border"])
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TCombobox', fieldbackground=current_theme["button"], background=current_theme["button"], foreground=current_theme["button_fg"], font=FONT, borderwidth=0)
    style.map('TCombobox', fieldbackground=[('readonly', current_theme["button"])] )
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
        'algorithm': algorithm,
        'size': len(data),
        'step_delay_sec': stepTime,
        'initial_array': initial_array,
        'comparisons': 0,
        'swaps': 0,
        'start_time': datetime.now().isoformat()
    }
    def done():
        enable_buttons()
    global target_label
    if algorithm == "Linear Search":
        if not data:
            done()
            return
        target = random.choice(data)
        if target_label:
            target_label.config(text=f"Searching for: {target}")
        print(f"Searching for: {target}")
        startLinearSearch(data, drawData, stepTime, done, report, target)
    elif algorithm == "Binary Search":
        if not data:
            done()
            return
        sorted_data = sorted(data)
        target = random.choice(sorted_data)
        if target_label:
            target_label.config(text=f"Searching for: {target}")
        print(f"Searching for: {target}")
        # Sort data in place for binary search
        data[:] = sorted_data
        startBinarySearch(data, drawData, stepTime, done, report, target)
    elif algorithm == "Bubble Sort":
        if target_label:
            target_label.config(text="")
        startBubbleSort(data, drawData, stepTime, done, report)
    elif algorithm == "Selection Sort":
        if target_label:
            target_label.config(text="")
        startSelectionSort(data, drawData, stepTime, done, report)
    elif algorithm == "Insertion Sort":
        if target_label:
            target_label.config(text="")
        startInsertionSort(data, drawData, stepTime, done, report)
    elif algorithm == "Merge Sort":
        if target_label:
            target_label.config(text="")
        startMergeSort(data, drawData, stepTime, done, report)
    else:
        done()

def genData(data_size):
    global data, colorData
    data = []
    colorData = [current_theme["bar"] for _ in range(int(float(data_size)))]
    for _ in range(int(float(data_size))):
        data.append(random.randrange(1, 100))
    drawData(data, colorData)
    sizel.config(text=str(format(int(float(data_size)), "0>3d")))

def drawData(data, colorData):
    canvas.delete("all")
    canvas_h = canvas.winfo_height()
    canvas_w = canvas.winfo_width()
    spacing = 2
    rectangle_w = (canvas_w - spacing * (len(data) - 1)) / len(data) if data else 0
    if data and canvas_h > 0:
        max_val = max(data)
    else:
        return
    for i, value in enumerate(data):
        rect_height = value / max_val if max_val != 0 else 0
        x0 = i * rectangle_w + (i + 1) * spacing
        y0 = canvas_h - rect_height * (canvas_h - 20)
        x1 = (i + 1) * rectangle_w + (i + 1) * spacing
        y1 = canvas_h
        # Draw shadow
        canvas.create_rectangle(x0+2, y0+2, x1+2, y1+2, fill=current_theme["border"], outline="")
        # Draw bar
        canvas.create_rectangle(x0, y0, x1, y1, fill=colorData[i], outline="")
    root.update_idletasks()

def dispDelay(delay):
    delayl.config(text=str(format(float(delay)/10,">03.1f")+" sec"))

def set_theme(theme_name):
    global current_theme_name, current_theme
    current_theme_name = theme_name
    current_theme = THEMES[theme_name]
    apply_theme()
    drawData(data, colorData)

def main():
    global width, height
    width = 1000
    height = 610

    global root
    root = Tk()
    root.title("Algorithm Visualizer")
    style = ttk.Style()
    style.theme_use('clam')
    root.resizable(True, True)
    root.config(bg=current_theme["bg"])

    # Make the grid expand
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    global titlef, delayl, sizel, theme_menu, speed_scale, size_scale, target_label
    titlef = Frame(root, width=width, height=height, bg=current_theme["bg"], highlightthickness=0, bd=0)
    titlef.grid(row=0, column=0, sticky="ew")

    sizel = Label(titlef, text="50", bg=current_theme["bg"], fg=current_theme["fg"], font=FONT)
    sizel.pack(side=LEFT, padx=(10, 200))
    Label(titlef, text="Algorithms Visualizer", bg=current_theme["bg"], fg=current_theme["fg"], font=(FONT[0], 20, "bold"), bd=0, highlightthickness=0).pack(pady=10, side=LEFT)
    delayl = Label(titlef, text="0.0 sec", bg=current_theme["bg"], fg=current_theme["fg"], font=FONT)
    delayl.pack(side=LEFT, padx=(190, 10))

    # Theme Dropdown
    theme_var = StringVar(value=current_theme_name)
    theme_menu = ttk.Combobox(titlef, textvariable=theme_var, state='readonly', values=list(THEMES.keys()), font=FONT, width=16)
    theme_menu.pack(side=LEFT, padx=(20, 10))
    def on_theme_change(event):
        set_theme(theme_var.get())
    theme_menu.bind("<<ComboboxSelected>>", on_theme_change)

    global topf
    topf = Frame(root, width=width, height=250, bg=current_theme["bg"])
    topf.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    global size, speed
    size = IntVar()
    speed = IntVar()
    speed.set(0)
    size.set(50)
    Label(topf, text="Step Delay (sec)", bg=current_theme["bg"], fg=current_theme["fg"], font=FONT).grid(row=0, column=0, padx=5, pady=5, sticky=E)
    speed_scale = Scale(topf, variable=speed, from_=0, to=10, orient=HORIZONTAL,
                    command=dispDelay, bg=current_theme["bg"], fg=current_theme["fg"],
                    troughcolor=current_theme["border"], highlightthickness=0, bd=0,
                    sliderrelief=FLAT, font=FONT, length=180)
    speed_scale.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    algorithm = StringVar()
    Label(topf, text="Select Algorithm", bg=current_theme["bg"], fg=current_theme["fg"], font=FONT).grid(row=0, column=3, padx=(50, 0), pady=5, sticky=E)
    algorithm_menu = ttk.Combobox(topf, textvariable=algorithm, state='readonly', values=['Linear Search', 'Binary Search', 'Bubble Sort', 'Selection Sort', 'Insertion Sort', 'Merge Sort'], font=FONT)
    algorithm_menu.grid(row=0, column=4, padx=5, pady=5, sticky=W)
    algorithm_menu.current(0)

    Label(topf, text="Size", bg=current_theme["bg"], fg=current_theme["fg"], font=FONT).grid(row=1, column=0, padx=5, pady=5, sticky=E)
    size_scale = Scale(topf, variable=size, from_=3, to=100, orient=HORIZONTAL,
                   command=genData, bg=current_theme["bg"], fg=current_theme["fg"],
                   troughcolor=current_theme["border"], highlightthickness=0, bd=0,
                   sliderrelief=FLAT, font=FONT, length=180)
    size_scale.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    Button(topf, text="Visualise", bg=current_theme["button"], fg=current_theme["button_fg"], command=lambda: visualize(algorithm.get(), speed.get()), font=FONT).grid(row=1, column=3, padx=(50, 0), pady=5, ipadx=10, sticky=W)

    # Add target label above the canvas
    target_label = Label(root, text="", bg=current_theme["bg"], fg=current_theme["fg"], font=(FONT[0], 16, "bold"))
    target_label.grid(row=2, column=0, sticky="ew", pady=(0, 0))

    global canvas
    canvas = Canvas(root, bg=current_theme["bg"], highlightbackground=current_theme["border"], highlightthickness=0, bd=0)
    canvas.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")

    def on_resize(event):
        drawData(data, colorData)

    canvas.bind("<Configure>", on_resize)

    genData(50)
    root.mainloop()

if __name__ == "__main__":
    main()
