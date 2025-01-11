from tkinter import *
from math import *
from ezTK import *
from random import randrange as rr

def main():
    global app
    
    app = Win(title="Parametric Function Plotter", grow=False)

    frame = Frame(app, flow='EW', border=2, grow=False)
    Label(frame, text="x(t) = ")
    app.x_entry = Entry(frame)

    frame = Frame(app, flow='EW', border=2, grow=False)
    Label(frame, text="y(t) = ")
    app.y_entry = Entry(frame)

    frame = Frame(app, flow='EW', border=2, grow=False)
    Label(frame, text="t min = ")
    app.t_min_entry = Entry(frame, width=5)
    
    Label(frame, text=" t max = ")
    app.t_max_entry = Entry(frame, width=5)

    frame = Frame(app, flow='EW', border=2, grow=False)
    Label(frame, text="Plot Type: ")

    plot_button = Button(app, text="Plot", command=table_values)

    app.canvas = Canvas(app, width=500, height=500, border=2)
    app.width, app.height = int(app.canvas['width']), int(app.canvas['height'])  # store canvas size

    draw_axes(app.width, app.height)
    app.loop()

def draw_axes(new_width, new_height):
    color_list = {
        "white": "#FFF",
        "black": "#000",
        "red": "#F00",
        "green": "#0F0",
        "blue": "#00F",
    }
    scale = 10
    line_width = 2

    max_x = new_width
    x_0 = new_width // 2
    max_y = new_height
    y_0 = new_height // 2
    # X-axis
    app.canvas.create_line(0, y_0, max_x, y_0, width=line_width, fill=color_list["black"], tag='axes')
    # Y-axis
    app.canvas.create_line(x_0, 0, x_0, max_y, width=line_width, fill=color_list["black"], tag='axes')
    
    for x in range(0, max_x, scale*2):
        x1 = x
        y1 = 0
        y2 = 2*y_0
        app.canvas.create_line(x1, y1, x1, y2, width=1, fill="#D3D3D3")

    for y in range(0, max_y, scale*2):
        y1 = y
        x1 = 0
        x2 = 2*x_0
        app.canvas.create_line(x1, y1, x2, y1, width=1, fill="#D3D3D3")

def frange(start, stop=None, step=None):
    start = float(start)
    if stop is None:
        stop = start + 0.0
        start = 0.0
    if step is None:
        step = 1.0

    count = 0
    while True:
        temp = float(start + count * step)
        if step > 0 and temp >= stop:
            break
        elif step < 0 and temp <= stop:
            break
        yield temp
        count += 1

def generate_asymptote_values(x_1, step, num_values=500):
    left_values = list(frange(x_1 - 1, x_1, step))[-num_values:]
    right_values = list(frange(x_1 + step, x_1 + 1, step))[:num_values]
    return left_values + right_values

def evaluate_expression(t):
    """Evaluate the given expression with parameter t"""
    try:
        expression = app.x_entry.get()
        globals_dict = {'cos': cos, 'sin': sin, 'tan': tan}
        return eval(expression, globals_dict, locals())
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None

def table_values():
    app.canvas.delete('drawing')
    t_min = int(app.t_min_entry.get())
    t_max = int(app.t_max_entry.get())
    color_list = ["#FF0F0F",  # red
                  "#00FF00",  # green
                  "#0000FF",  # blue
                  "#FFFF00",  # yellow
                  "#00FFFF",  # cyan
                  "#FF00FF",  # magenta
                  "#FFA500",  # orange
                  "#800080"]  # purple

    i = rr(len(color_list))
    x_values = []
    y_values = []

    for x in frange(t_min, t_max):
        if abs(x - (t_min + 1)) < 1:
            asymptote_values = generate_asymptote_values(t_min + 1, 0.01)
            for ax in asymptote_values:
                x_values.append(ax)
                y_values.append(evaluate_expression(ax))
            break
        x_values.append(x)
        y_values.append(evaluate_expression(x))

    for x in frange(t_min + 1, t_max):
        x_values.append(x)
        y_values.append(evaluate_expression(x))

    for x, y in zip(x_values, y_values):
        if y is not None:
            plot_function(x, y, x + 1, y, i)

def plot_function(x_a, y_a, x_b, y_b, i):
    color_list = ["#FFF", "#0F0", "#00F", "#FF0", "#0FF", "#F0F", "#FFA500", "#800080"]
    scale = 10
    max_x = app.width
    x_0 = app.width // (2 * scale)
    
    max_y = app.height
    y_0 = app.height // (2 * scale)
    
    line_width = 2
    
    x_a = (x_0 + x_a) * scale 
    y_a = (y_0 - y_a) * scale
    
    x_b = (x_0 + x_b) * scale
    y_b = (y_0 - y_b) * scale
    
    app.canvas.create_line(x_a, y_a, x_b, y_b, width=line_width, fill=color_list[i], smooth=True, tag='drawing')

if __name__ == '__main__':
    main()

