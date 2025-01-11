import tkinter as tk
from math import *
from ezTK import *

def evaluate_expression(expression, t):
    """Evaluate the given expression with parameter t"""
    try:
        return eval(expression, {'t': float(t)})
    except Exception as e:
        print(f"Error evaluating expression: {e}")
        return None

def plot_parametric_function(canvas, x_expr, y_expr, t_min, t_max, num_points=(200,20), color='blue', plot_type='line'):
    """Plot the parametric function on the given canvas"""
    canvas.delete('plot')  # Clear previous plots
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    app.width, app.height = int(app.width), int(app.height)
    points = []
    
    if plot_type == 'line':
        for i in range(0,num_points[0]):
            t = t_min +0.05*app.height+ i
            xt = evaluate_expression(x_expr, t)
            if xt is not None:
                points.append((xt, t))
        print(points)
        x0, y0 = app.height//2, app.width//2
        xf, yf = points[len(points)-1]
        app.canvas.create_line(x0, height - y0, xf, height - yf, fill=color, tags='plot')
    elif plot_type == 'curve':
        t_min = t_min + int(0.05*app.height)
        t_max = t_max + int(0.165*app.height)
        difference = int(t_max - t_min)
        t_values = []
        for i in range(difference):
            t_values.append(t_min + i)
            print(t_values)
        points = [(t, evaluate_expression(x_expr, t)) for t in t_values if evaluate_expression(x_expr, t) is not None]
        #print(points)
        # Normalize points so that the origin is at the bottom-left corner
        normalized_points = [(t, height + height//2 - xt) for t, xt in points]
        #print(normalized_points)
        # Draw the curve
        xa,ya = normalized_points[0]
        i=1
        while i<len(normalized_points):
            xb,yb = normalized_points[i]
            app.canvas.create_line(xa,ya,xb,yb, fill=color, smooth=True, tags='plot')
            i+=1
            xa,ya = xb,yb
    elif plot_type == 'dots':
        for x, y in points:
            canvas.create_oval(x - 2, height - y - 2, x + 2, height - y + 2, fill=color, outline=color, tags='plot')
    # Add support for other plot types as needed
def draw_line():
 app.width, app.height = int(app.width), int(app.height)
 for yb in range(app.width):
   xb=app.height - 0.995*app.height
   app.canvas.create_line(xb,0,xb,yb,fill='#000')
 for xb in range(app.height):
   yb=0.165*app.height
   app.canvas.create_line(0,yb,xb,yb,fill='#000')

def on_plot_clicked():
    """Callback function for the 'Plot' button"""
    global app
    x_expr = x_entry.get()
    y_expr = y_entry.get()
    t_min = float(t_min_entry.get())
    t_max = float(t_max_entry.get())
    plot_parametric_function(app.canvas, x_expr, y_expr, t_min, t_max, plot_type=plot_type.get())

app = Win(title="Parametric Function Plotter", grow=True)

frame = Frame(app, flow='EW', border=2, grow=False)
Label(frame, text="x(t) = ").pack(side='left')
x_entry = Entry(frame)
x_entry.pack(side='left', expand=True, fill='x')
frame.pack(expand=True, fill='x')

frame = Frame(app, flow='EW', border=2, grow=False)
Label(frame, text="y(t) = ").pack(side='left')
y_entry = Entry(frame)
y_entry.pack(side='left', expand=True, fill='x')
frame.pack(expand=True, fill='x')

frame = Frame(app, flow='EW', border=2, grow=False)
Label(frame, text="t min = ").pack(side='left')
t_min_entry = Entry(frame, width=5)
t_min_entry.pack(side='left')
Label(frame, text=" t max = ").pack(side='left')
t_max_entry = Entry(frame, width=5)
t_max_entry.pack(side='left')
frame.pack(expand=True, fill='x')

frame = Frame(app, flow='EW', border=2, grow=False)
Label(frame, text="Plot Type: ").pack(side='left')
plot_type = StringVar()
plot_type.set('line')
Radiobutton(frame, text="Line", variable=plot_type, value='line').pack(side='left')
Radiobutton(frame, text="Curve", variable=plot_type, value='curve').pack(side='left')
Radiobutton(frame, text="Dots", variable=plot_type, value='dots').pack(side='left')
frame.pack(expand=True, fill='x')

plot_button = Button(app, text="Plot", command=on_plot_clicked)
plot_button.pack(side='top', pady=10)

app.canvas = Canvas(app, width=3000, height=3000, border=2)
app.width, app.height = app.canvas['width'], app.canvas['height'] # store canvas size
#print(app.width, app.height)
app.canvas.pack(expand=True, fill='both')

draw_line()

app.loop()
