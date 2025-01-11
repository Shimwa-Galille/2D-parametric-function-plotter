
from math import*
from new_plotter import plot_function

def evaluate(expression, t):
    """Evaluate the given app.expression with parameter t"""
    try:
        
        globals_dict = {'cos': cos, 'sin': sin, 'tan': tan}
        return eval(expression, globals_dict, locals())
    except Exception as e:
        print(f"Error evaluating app.expression: {e}")
        return None

def get_values(expression, t_min, t_max):
   
    for x in range (t_min, t_max):
        y = evaluate(expression, x)
        x_1 = x + 1
        y_1 = evaluate(expression, x_1) 
        if y == None:
            get_horizontal_asymptote(x,t_min, t_max)
        elif y_1 == None:
            get_horizontal_asymptote(x_1, t_min, t_max)
            

def get_horizontal_asymptote(t, t_max, t_min) -> None:

    for x in range(t_min, t_max):
        y= evaluate(f'{t}', x)
        x_1 = x+1
        y_1 = evaluate(f't', x_1)

        plot_function(x,y,x_1,y_1, 0)
