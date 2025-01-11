from math import cos, sin, tan, pi, sqrt, log, exp, fabs
from ezTK import *
from random import randrange as rr

def main():
    global app
    
    app = Win(title="Parametric Function Plotter", grow=False)
    
    create_ui_components()
    update_labels("Cartesian")
    
    app.loop()

def create_ui_components():
    create_coord_selection()
    create_cartesian_input()
    create_polar_input()
    create_plot_button()
    create_canvas()
    app.after(500, show_instructions)

def create_coord_selection():
    coord_frame = Frame(app, flow='EW', border=2, grow=False)
    Label(coord_frame, text="Coordinate System:")
    Button(coord_frame, text="Cartesian", command=lambda: update_labels("Cartesian"))
    Button(coord_frame, text="Polar", command=lambda: update_labels("Polar"))

def create_cartesian_input():
    app.cartesian_frame = Frame(app, flow='EW', border=2, grow=False)
    Label(app.cartesian_frame, text="x(t) = ")
    app.x_entry = Entry(app.cartesian_frame)
    
    y_frame = Frame(app.cartesian_frame, flow='EW', border=2, grow=False)
    Label(y_frame, text="y(t) = ")
    app.y_entry = Entry(y_frame)
    
    t_frame = Frame(app.cartesian_frame, flow='EW', border=2, grow=False)
    Label(t_frame, text="t min = ")
    app.t_min_entry = Entry(t_frame, width=5)
    
    Label(t_frame, text=" scale = ")
    app.scale_entry = Entry(t_frame, width=5)
    
    Label(t_frame, text=" t max = ")
    app.t_max_entry = Entry(t_frame, width=5)

def create_polar_input():
    app.polar_frame = Frame(app, flow='EW', border=2, grow=False)
    Label(app.polar_frame, text="r(t) = ")
    app.r_entry = Entry(app.polar_frame)
    
    theta_frame = Frame(app.polar_frame, flow='EW', border=2, grow=False)
    Label(theta_frame, text="θ(t) = ")
    app.theta_entry = Entry(theta_frame)
    
    pt_frame = Frame(app.polar_frame, flow='EW', border=2, grow=False)
    Label(pt_frame, text="t min = ")
    app.p_t_min_entry = Entry(pt_frame, width=5)
    
    Label(pt_frame, text=" scale = ")
    app.p_scale_entry = Entry(pt_frame, width=5)
    
    Label(pt_frame, text=" t max = ")
    app.p_t_max_entry = Entry(pt_frame, width=5)

def create_plot_button():
    Button(app, text="Plot", command=table_values)

def create_canvas():
    app.canvas = Canvas(app, width=800, height=500, border=2)
    app.width, app.height = int(app.canvas['width']), int(app.canvas['height'])

def update_labels(coord_system):
    if coord_system == "Cartesian":
        app.polar_frame.pack_forget()
        app.cartesian_frame.pack()
        app.coord_system = "Cartesian"
    else:
        app.cartesian_frame.pack_forget()
        app.polar_frame.pack()
        app.coord_system = "Polar"

def show_instructions():
    instruction_win = Win(title="Instructions", grow=False)
    Frame(instruction_win, flow='W', grow=False)
    Label(instruction_win, text="1. Use brackets for better results.\n2. Make sure the input function has 't' as variable.\nPreferable scale is 10 or 50.")
    Button(instruction_win, text="OK", command=instruction_win.exit)

def show_errors(error_type):
    app_errors = Win(title="Error", grow=False)
    Label(app_errors, text=f'{error_type}')
    Button(app_errors, text="OK", command=app_errors.exit)

def draw_axes(new_width, new_height, scale):
    color_list = {"white": "#FFF", "black": "#000", "red": "#F00", "green": "#0F0", "blue": "#00F"}
    scale = int(scale)
    line_width = 4
    
    max_x = new_width
    x_0 = new_width // 2
    max_y = new_height
    y_0 = new_height // 2
    
    app.canvas.create_line(0, y_0, max_x, y_0, width=line_width, fill=color_list["black"], tag='axes')
    app.canvas.create_line(x_0, 0, x_0, max_y, width=line_width, fill=color_list["black"], tag='axes')
    
    for x in range(0, max_x, scale):
        app.canvas.create_line(x, 0, x, 2*y_0, width=1, fill="#D3D3D3", tag='axes')
    
    for y in range(0, max_y, scale):
        app.canvas.create_line(0, y, 2*x_0, y, width=1, fill="#D3D3D3", tag='axes')

def evaluate_expression(expression, t):
    try:
        if not expression.strip():
            return None
        globals_dict = {
            'cos': cos, 'sin': sin, 'tan': tan, 'pi': pi, 't': t,
            'sqrt': sqrt, 'log': log, 'exp': exp, 'fabs': fabs
        }
        return eval(expression, globals_dict)
    except Exception:
        return None

def table_values():
    app.canvas.delete('axes')
    app.canvas.delete('drawing')
    app.canvas.delete('asymptote')
    
    if app.coord_system == "Cartesian":
        x_expression = app.x_entry.get().strip()
        y_expression = app.y_entry.get().strip()
        t_min = app.t_min_entry.get().strip()
        t_max = app.t_max_entry.get().strip()
        scale = app.scale_entry.get().strip()
        
        if not x_expression or not y_expression:
            show_errors("Input(s) for Cartesian coordinates is/are empty")
            return
        
        if not t_min or not t_max or not scale:
            show_errors("t_min, t_max or scale is empty")
            return
        
        try:
            t_min = float(t_min)
            t_max = float(t_max)
            scale = int(scale)
        except ValueError:
            show_errors("t_min, t_max or scale is invalid")
            return
        
        draw_axes(app.width, app.height, scale)
        plot_function(x_expression, y_expression, t_min, t_max, scale)
        
        asymptote_y = calculate_horizontal_asymptote(y_expression)
        if asymptote_y is not None:
            draw_horizontal_asymptote(asymptote_y, scale)
            
        m, b = calculate_oblique_asymptote(x_expression, y_expression)
        if m is not None and b is not None:
            draw_oblique_asymptote(m, b, scale)
        
    else:
        r_expression = app.r_entry.get().strip()
        theta_expression = app.theta_entry.get().strip()
        t_min = app.p_t_min_entry.get().strip()
        t_max = app.p_t_max_entry.get().strip()
        scale = app.p_scale_entry.get().strip()
        
        if not r_expression or not theta_expression:
            show_errors("Input(s) for Polar coordinates is/are empty")
            return
        
        if not t_min or not t_max or not scale:
            show_errors("t_min, t_max or scale is empty")
            return
        
        try:
            t_min = float(t_min)
            t_max = float(t_max)
            scale = int(scale)
        except ValueError:
            show_errors("t_min, t_max or scale is invalid")
            return
        
        draw_axes(app.width, app.height, scale)
        plot_polar_function(r_expression, theta_expression, t_min, t_max, scale)

def plot_function(x_expression, y_expression, t_min, t_max, scale):
    color_list = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#FFA500", "#800080"]
    color = color_list[rr(len(color_list))]
    
    scale = int(scale)
    x_0 = app.width // 2
    y_0 = app.height // 2
    
    prev_x, prev_y = None, None
    for t in range(int(t_min * 100), int(t_max * 100)):
        t /= 100.0
        x = evaluate_expression(x_expression, t)
        y = evaluate_expression(y_expression, t)
        
        if x is None or y is None:
            prev_x, prev_y = None, None
            continue
        
        screen_x = x_0 + x * scale
        screen_y = y_0 - y * scale
        
        if prev_x is not None and prev_y is not None:
            if abs(screen_y - prev_y) < app.height:
                app.canvas.create_line(prev_x, prev_y, screen_x, screen_y, width=2, fill=color, tag='drawing')
            elif abs(screen_y - prev_y) >= app.height and (y_expression != 'exp(t)' and x_expression != 'exp(t)'):
                app.canvas.create_line(prev_x, 0, prev_x, app.height, fill="black", dash=(4, 2), tag='drawing')
            elif abs(screen_x - prev_x) >= app.width:
                app.canvas.create_line(0, prev_y, app.width, prev_y, fill="black", dash=(4, 2), tag='drawing')
        
        prev_x, prev_y = screen_x, screen_y

def plot_polar_function(r_expression, theta_expression, t_min, t_max, scale):
    color_list = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#FFA500", "#800080"]
    color = color_list[rr(len(color_list))]
    
    scale = int(scale)
    x_0 = app.width // 2
    y_0 = app.height // 2
    
    prev_x, prev_y = None, None
    for t in range(int(t_min * 100), int(t_max * 100)):
        t /= 100.0
        r = evaluate_expression(r_expression, t)
        theta = evaluate_expression(theta_expression, t)
        
        if r is None or theta is None:
            prev_x, prev_y = None, None
            continue
        
        x = r * cos(theta)
        y = r * sin(theta)
        
        screen_x = x_0 + x * scale
        screen_y = y_0 - y * scale
        
        if prev_x is not None and prev_y is not None:
            if abs(screen_y - prev_y) < app.height:
                app.canvas.create_line(prev_x, prev_y, screen_x, screen_y, width=2, fill=color, tag='drawing')
            else:
                prev_x, prev_y = None, None
                continue
        
        prev_x, prev_y = screen_x, screen_y

def calculate_horizontal_asymptote(y_expression):
    t_values = range(500, 10000, 500)
    y_values = [evaluate_expression(y_expression, t) for t in t_values]
    
    if None in y_values:
        return None
    
    asymptote_y = sum(y_values) / len(y_values)
    return asymptote_y

def draw_horizontal_asymptote(y, scale):
    scale = int(scale)
    x_0 = app.width // 2
    y_0 = app.height // 2
    
    screen_y = y_0 - y * scale
    
    if 0 <= screen_y <= app.height:
        app.canvas.create_line(0, screen_y, app.width, screen_y, fill="red", dash=(4, 2), tag='asymptote')

def calculate_oblique_asymptote(x_expression, y_expression):
    t_values = range(500, 10000, 500)
    x_values = [evaluate_expression(x_expression, t) for t in t_values]
    y_values = [evaluate_expression(y_expression, t) for t in t_values]

    if None in x_values or None in y_values:
        return None, None

    m_values = [(y2 - y1) / (x2 - x1) if x2 != x1 else None for (x1, y1), (x2, y2) in zip(zip(x_values, y_values), zip(x_values[1:], y_values[1:]))]
    m_values = [m for m in m_values if m is not None]

    if not m_values:
        return None, None

    m = sum(m_values) / len(m_values)
    b_values = [y - m * x for x, y in zip(x_values, y_values)]
    b = sum(b_values) / len(b_values)

    return m, b

def draw_oblique_asymptote(m, b, scale):
    scale = int(scale)
    x_0 = app.width // 2
    y_0 = app.height // 2
    
    x_min = -x_0 / scale
    x_max = (app.width - x_0) / scale
    
    y_min = m * x_min + b
    y_max = m * x_max + b
    
    screen_x_min = x_0 + x_min * scale
    screen_y_min = y_0 - y_min * scale
    screen_x_max = x_0 + x_max * scale
    screen_y_max = y_0 - y_max * scale
    
    app.canvas.create_line(screen_x_min, screen_y_min, screen_x_max, screen_y_max, fill="black", dash=(4, 2), tag='asymptote')

if __name__ == '__main__':
    main()
