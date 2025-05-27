import tkinter as tk

# Raw data
data = [10, 20, 30, 40, 50]

# Normalize the data
max_val = max(data)
normalized_data = [x / max_val for x in data]

# GUI setup
window = tk.Tk()
window.title("Bar Chart - Normalized Data")
canvas_width = 500
canvas_height = 400
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# Drawing bars
bar_width = canvas_width / len(normalized_data)
for i, val in enumerate(normalized_data):
    # Calculate coordinates
    x0 = i * bar_width + 10
    y0 = canvas_height - val * (canvas_height - 50)
    x1 = (i + 1) * bar_width - 10
    y1 = canvas_height

    # Draw rectangle
    canvas.create_rectangle(x0, y0, x1, y1, fill="skyblue")

    # Draw value text
    canvas.create_text((x0 + x1) / 2, y0 - 10, text=f"{val:.2f}", fill="black")

window.mainloop()
