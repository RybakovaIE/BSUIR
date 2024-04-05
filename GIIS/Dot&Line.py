from tkinter import *
import tkinter.scrolledtext as st
import math
width=700
height=425
x0=x1=y0=y1=0
pressed_button=None
pixels = []
color='#000000'
debug = False

root = Tk()
waiting_var = IntVar()
debug_image = PhotoImage(file='debug.png').subsample(20)
play_image = PhotoImage(file='play.png').subsample(20)

root.title = 'Dot&Line'
root.geometry('700x425')


def sign(number):
    if number < 0: return -1
    else: return 1

def mirror(x, y, center_x, center_y):
    mirrored_x = center_x - x - 1
    mirrored_y = center_y - y - 1
    draw_dot(mirrored_x, y + center_y, color)
    draw_dot(x + center_x, mirrored_y, color)
    draw_dot(mirrored_x, mirrored_y, color)

def draw_dot(x, y, color='black'):
    x1 = x*10
    y1 = y*10
    canvas.create_rectangle(x1, y1, x1+10, y1+10, fill=color, outline=color)

def convert_coordinates(x, y):
    return x//10, y//10

def get_color(base, alpha):
    background_r, background_g, background_b = 255, 255, 255
    rgb = root.winfo_rgb(base)
    new_r = round((1 - alpha) * background_r + alpha * rgb[0]/256)
    new_g = round((1 - alpha) * background_g + alpha * rgb[1]/256)
    new_b = round((1 - alpha) * background_b + alpha * rgb[2]/256)
    return f"#{new_r:02X}{new_g:02X}{new_b:02X}"

def line_diff_analyzer():
    global pixels
    if len(pixels) == 2:
        x, y, x2, y2 = pixels[0][0], pixels[0][1], pixels[1][0], pixels[1][1]
        length = max(abs(x2-x), abs(y2-y))
        dx = (x2-x)/length
        dy = (y2-y)/length
        if debug: solve_field.insert(END, f'x1 = {x}, y1 = {y}\nx2 = {x2}, y2 = {y2}\nlength={length}\ndx={dx}, dy={dy}')
        draw_dot(x, y, color)
        if debug: solve_field.insert(END, f'\n\nPlot({x}, {y})')
        i = 0
        while i < length:
            if debug:
                canvas.wait_variable(waiting_var)
                solve_field.insert(END, f'\n\nx = x + dx = {x+dx}\ny = y + dy = {y+dy}\n')
            x = x + dx
            y = y + dy
            round_x, round_y = round(x), round(y)
            draw_dot(round_x, round_y, color)
            if debug: solve_field.insert(END, f'Plot({round_x}, {round_y})')
            i += 1
        pixels = []
        solve_field.delete(1.0, END)

def line_brezenhem():
    global pixels
    if len(pixels) == 2:
        x, y, x2, y2 = pixels[0][0], pixels[0][1], pixels[1][0], pixels[1][1]
        dx = x2-x
        dy = y2-y
        if debug: solve_field.insert(END, f'x1 = {x}, y1 = {y}\nx2 = {x2}, y2 = {y2}\ndx = {dx}, dy = {dy}')
        if abs(dx) >= abs(dy):
            main, main_s = x, 'x'
            sec, sec_s = y, 'y'
            main_d = dx
            sec_d = dy
        else:
            main, main_s = y, 'y'
            sec, sec_s = x, 'x'
            main_d = dy
            sec_d = dx
        e = abs(2*sec_d) - abs(main_d)
        if debug: solve_field.insert(END, f'\ne = |2{sec_s}| - |2{main_s}| = {e}\n\nPlot({x}, {y})')
        draw_dot(x, y, color)
        i = 0
        while i < abs(main_d):
            if debug: canvas.wait_variable(waiting_var)
            if e >= 0:
                sec += 1*sign(sec_d)
                e -= abs(2*main_d)
                if debug: solve_field.insert(END, f'\n{sec_s} = {sec}\ne = e - |2d{main_s}|')
            main += 1*sign(main_d)
            e += abs(2*sec_d)
            if debug: solve_field.insert(END, f'\n{main_s} = {main}\ne = e + |2d{sec_s}| = {e}\n')
            i += 1
            if abs(dx) >= abs(dy): draw_dot(main, sec, color)
            else: draw_dot(sec, main, color)
        pixels = []
        solve_field.delete(1.0, END)


def line_smooth():
    global pixels
    if len(pixels) == 2:
        x, y, x2, y2 = pixels[0][0], pixels[0][1], pixels[1][0], pixels[1][1]
        length = max(abs(x2-x), abs(y2-y))
        dx = (x2-x)/length
        dy = (y2-y)/length
        if abs((x2-x)) >= abs(y2-y):
            main, main_s = x, 'x'
            sec, sec_s = y, 'y'
            main_d = dx
            sec_d = dy
        else:
            main, main_s = y, 'y'
            sec, sec_s = x, 'x'
            main_d = dy
            sec_d = dx
        draw_dot(x, y, color)
        if debug: solve_field.insert(END, f'x1 = {x}, y1 = {y}\nx2 = {x2}, y2 = {y2}\nlength={length}\ndx={dx}, dy={dy}\n')
        i = 0
        while i < length:
            if debug: canvas.wait_variable(waiting_var)
            main += main_d
            sec += sec_d
            sec_fractional = sec%1
            first_color, second_color = get_color(color, 1-sec_fractional), get_color(color, sec_fractional)
            sec1 = int(sec)
            sec2 = sec1+1
            if debug: solve_field.insert(END, f'\n{main_s} = {main_s} + d{main_s} = {main}\n{sec_s} = {sec_s} + d{sec_s} = {sec}\n')
            if abs((x2-x)) >= abs(y2-y):
                draw_dot(main, sec1, first_color)
                draw_dot(main, sec2, second_color)
            else:
                draw_dot(sec1, main, first_color)
                draw_dot(sec2, main, second_color)
            i += 1
        pixels = []
        solve_field.delete(1.0, END)

def circle():
    global pixels
    if len(pixels) == 2:
        x1, y1, x2, y2 = pixels[0][0], pixels[0][1], pixels[1][0], pixels[1][1]
        R = math.sqrt((x2-x1)**2+(y2-y1)**2)
        x, y = 0, round(R)
        limit = 0
        d = 2 - 2*R
        if debug: solve_field.insert(END, f'center = ({x1}, {y1}), R = {R}\nPlot({x1}, {round(y1+R)})\n\nd = 2 - 2R = {d}\n')
        draw_dot(x1, round(y1+R), color)
        mirror(0, round(R), x1, y1)
        diagonal = True
        while y > limit:
            if debug: canvas.wait_variable(waiting_var)
            diagonal = True
            if d > 0:
                d1 = 2*d - 2*x - 1
                if debug: solve_field.insert(END, f'\nd1 = 2d - 2x - 1 = {d1}')
                if d1 > 0: 
                    diagonal = False
                    y -= 1
                    d = d - 2*y + 1
                    if debug: solve_field.insert(END, f'\ny--\nd = d - 2y + 1\nV')
            elif d < 0:
                d1 = 2*d + 2*y - 1
                if debug: solve_field.insert(END, f'\nd1 = 2d + 2y - 1 = {d1}')
                if d1 <= 0: 
                    diagonal = False
                    x += 1
                    d = d + 2*x + 1
                    if debug: solve_field.insert(END, f'\nx++\nd = d + 2x + 1\nH')
            if diagonal:
                x += 1
                y -= 1
                d += 2*x - 2*y +2
                if debug: solve_field.insert(END, f'\nx++, y--\nd = d + 2x - 2y + 2\nD')
            draw_dot(x + x1, y + y1, color)
            mirror(x, y, x1, y1)
            if debug: solve_field.insert(END, f'   Plot({x+x1}, {y+y1})\n')
        pixels = []

def ellips():
    global pixels
    if len(pixels) == 2:
        x1, y1, x2, y2 = pixels[0][0], pixels[0][1], pixels[1][0], pixels[1][1]
        a = round(abs((x2-x1))/2)
        b = round(abs((y2-y1))/2)
        center_x = round((x2+x1)/2)
        center_y = round((y2+y1)/2)
        x, y = 0, b
        limit = 0
        d = b**2 - 2*b*a**2 + a**2
        if debug: solve_field.insert(END, f'center = ({center_x}, {center_y}), a = {a}, b = {b}\nPlot({center_x}, {round(center_y+b)})\n\nd = b^2 - 2ba^2 + a^2= {d}\n')
        draw_dot(center_x, round(center_y+b), color)
        mirror(0, round(b), center_x, center_y)
        diagonal = True
        while y > limit:
            if debug: canvas.wait_variable(waiting_var)
            diagonal = True
            if d > 0:
                d1 = 2*d - 2*x*b**2 - b**2
                if debug: solve_field.insert(END, f'\nd1 = 2d - 2xb^2 - b^2 = {d1}')
                if d1 > 0: 
                    diagonal = False
                    y -= 1
                    d = d - 2*y*a**2 + a**2
                    if debug: solve_field.insert(END, f'\ny--\nd = d - 2ya^2 + a^2\nV')
            elif d < 0:
                d1 = 2*d + 2*y*a**2 - a**2
                if debug: solve_field.insert(END, f'\nd1 = 2d + 2ay - a = {d1}')
                if d1 <= 0: 
                    diagonal = False
                    x += 1
                    d = d + 2*x*b**2 + b**2
                    if debug: solve_field.insert(END, f'\nx++\nd = d + 2xb^2 + b^2 = {d}\nH')
            if diagonal:
                x += 1
                y -= 1
                d += 2*x*b**2 - 2*y*a**2 + b**2 + a**2
                if debug: solve_field.insert(END, f'\nx++, y--\nd = d + 2xb^2 - 2ya^2 + 2 = {d}\nD')
            draw_dot(x + center_x, y + center_y, color)
            mirror(x, y, center_x, center_y)
            if debug: solve_field.insert(END, f'   Plot({x+center_x}, {y+center_y})\n')
        pixels = []

def calculate_d(x, y, a, b):
    if pressed_button == hyperbole:
        return b**2*(x+1)**2 - a**2*(y+1)**2 - a**2*b**2
    if pressed_button == parable:
        return b**2*(x+1)**2 - a**2*(y+1)**2 + a**2*b**2
    else:
        return b**2*(x+1)**2 + a**2*(y+1)**2 - a**2*b**2
    
def calculate_v_d1(x, d, b):
    if pressed_button == parable:
        return 2*d - 2*x*b**2 - b**2
    else:
        return 2*d - 2*x*b**2 - b**2
    
def calculate_h_d1(y, d, a):
    if pressed_button == hyperbole:
        return 2*d + 2*y*a**2 + a**2
    elif pressed_button == parable:
        return 2*d + 2*y*a**2 + a**2
    else:
        return 2*d - 2*y*a**2 - a**2
    
def get_start_curve(a, b, center_x, center_y):
    canvas_height = 41
    canvas_width = 44
    if pressed_button == hyperbole:
        return a, 0, max(canvas_height-center_y, center_y, canvas_width-center_x, center_x)
    elif pressed_button == parable:
        return 0, b, max(canvas_height-center_y, center_y, canvas_width-center_x, center_x)
    else:
        return 0, -b, 0


def curve(center_x, center_y, a, b):
    x, y, limit = get_start_curve(a, b, center_x, center_y)
    d = calculate_d(x, y, a, b)
    if debug: solve_field.insert(END, f'center = ({center_x}, {center_y}), a = {a}, b = {b}\nPlot({x+center_x}, {y+center_y})\n\nd = {d}\n')
    draw_dot(x + center_x, y + center_y, color)
    mirror(x, y, center_x, center_y)
    i = 0
    diagonal = True
    while i < limit or (pressed_button==ellipse and y < 0):
        if debug: canvas.wait_variable(waiting_var)
        diagonal = True
        if d > 0:
            d1 = calculate_v_d1(x, d, b)
            if debug: solve_field.insert(END, f'\nd1 = |d| - |v| = {d1}')
            if d1 > 0: 
                diagonal = False
                y += 1
                d = calculate_d(x, y, a, b)
                if debug: solve_field.insert(END, f'\ny++\nd = {d1}\nV')
        elif d < 0:
            d1 = calculate_h_d1(y, d, a)
            if debug: solve_field.insert(END, f'\nd1 = |d| - |h| = {d1}')
            if d1 <= 0: 
                diagonal = False
                x += 1
                d = calculate_d(x, y, a, b)
                if debug: solve_field.insert(END, f'\nx++\nd = {d}\nH')
        if diagonal:
            x += 1
            y += 1
            d = calculate_d(x, y, a, b)
            if debug: solve_field.insert(END, f'\nx++, y++\nd = {d}\nD')
        draw_dot(x + center_x, y + center_y, color)
        mirror(x, y, center_x, center_y)
        if debug: solve_field.insert(END, f'   Plot({x+center_x}, {y+center_y})\n')
        i+=1

def draw_hermite():
    global pixels
    if len(pixels) == 4:
        p1, p2, r1, r2 = pixels
        ax = 2*p1[0] - 2*p2[0] + r1[0] + r2[0]
        ay = 2*p1[1] - 2*p2[1] + r1[1] + r2[1]
        bx = -3*p1[0] + 3*p2[0] -2*r1[0] - r2[0]
        by = -3*p1[1] + 3*p2[1] -2*r1[1] - r2[1]
        cx = r1[0]
        cy = r1[1]
        dx = p1[0]
        dy = p1[1]
        t = 0
        x = dx
        y = dy
        while t <= 1:
            x1 = ax*t**3 + bx*t**2 + cx*t + dx
            y1 = ay*t**3 + by*t**2 + cy*t + dy
            canvas.create_line(x, y, x1, y1)
            x, y = x1, y1
            t += 0.05
        pixels = []
            
def draw(click):
    global pixels
    x, y = convert_coordinates(click.x, click.y)
    #x, y = click.x, click.y
    pixels.append((x, y))
    if pressed_button == diff_analyzer:
        line_diff_analyzer()
    elif pressed_button == brezenhem:
        line_brezenhem()
    elif pressed_button == smooth:
        line_smooth()
    elif pressed_button == circumference:
        circle()
    elif pressed_button == ellipse:
        ellips()
    elif pressed_button == hermite:
        canvas.create_rectangle(x, y, x, y, fill=color, outline=color)
        draw_hermite()
    else: pixels = []

# def draw(click):
#     global pixels
#     x, y = convert_coordinates(click.x, click.y)
#     pixels.append((x, y))
#     match(pressed_button):
#         case diff_analyzer:
#             line_diff_analyzer()
#         case brezenhem:
#             line_brezenhem()


def change_color(new_color):
    global color
    color = new_color

def change_button(button):
    global pressed_button
    if pressed_button == None:
        pressed_button = button
        button['state'] = 'disabled'
    elif pressed_button == button:
        pressed_button = None
        button['state'] = 'active'
    else:
        pressed_button['state'] = 'active'
        pressed_button = button
        button['state'] = 'disabled'
        
def change_debug():
    global debug
    if debug:
        debug = False
        debug_button['bg'] = 'white'
    else:
        debug = True
        debug_button['bg'] = 'green'

def clear_canvas():
    canvas.delete('all')

debug_panel = Frame(root, highlightbackground='red', highlightthickness=1)
debug_panel.grid(row=0, rowspan=2, column=1, sticky='ne')
toolbar = Frame(root, highlightbackground='purple', highlightthickness=1)
toolbar.grid(row=0, column=0, sticky='ew')
straight_line_panel = Frame(toolbar)
straight_line_panel.grid(row=0, column=0)
        
diff_analyzer = Button(straight_line_panel, text='line1', pady=3, command=lambda:change_button(diff_analyzer))
diff_analyzer.grid(row=0, column=0)
brezenhem = Button(straight_line_panel, text='line2', pady=3, command=lambda:change_button(brezenhem))
brezenhem.grid(row=1, column=0)
smooth = Button(straight_line_panel, text='line3', pady=3, command=lambda:change_button(smooth))
smooth.grid(row=2, column=0)

color_panel = Frame(toolbar)
color_panel.grid(row=0, column=1)

red = Button(color_panel, text= '    ', pady=3, bg='red', command=lambda:change_color('red'))
red.grid(row=0, column=0)
orange = Button(color_panel, text= '    ', pady=3, bg='orange', command=lambda:change_color('orange'))
orange.grid(row=0, column=1)
yellow = Button(color_panel, text= '    ', pady=3, bg='yellow', command=lambda:change_color('yellow'))
yellow.grid(row=0, column=2)
blue = Button(color_panel, text= '    ', pady=3, bg='deep sky blue', command=lambda:change_color('deep sky blue'))
blue.grid(row=1, column=0)
green2 = Button(color_panel, text= '    ', pady=3, bg='SpringGreen2', command=lambda:change_color('SpringGreen2'))
green2.grid(row=1, column=1)
green = Button(color_panel, text= '    ', pady=3, bg='green2', command=lambda:change_color('green2'))
green.grid(row=1, column=2)
purple = Button(color_panel, text= '    ', pady=3, bg='SlateBlue2', command=lambda:change_color('SlateBlue2'))
purple.grid(row=2, column=0)
violet = Button(color_panel, text= '    ', pady=3, bg='blue violet', command=lambda:change_color('blue violet'))
violet.grid(row=2, column=1)
pink = Button(color_panel, text= '    ', pady=3, bg='magenta2', command=lambda:change_color('magenta2'))
pink.grid(row=2, column=2)

second_line_panel = Frame(toolbar)
second_line_panel.grid(row=0, column=2)

circumference = Button(second_line_panel, text='    circle    ', pady=3, command=lambda:change_button(circumference))
circumference.grid(row=0, column=0, columnspan=3)
ellipse = Button(second_line_panel, text='    ellipse   ', pady=3, command=lambda:change_button(ellipse))
ellipse.grid(row=1, column=0, columnspan=3)
hyperbole = Button(second_line_panel, text='hyperbole', pady=3, command=lambda:change_button(hyperbole))
hyperbole.grid(row=2, column=0, columnspan=3)
parable = Button(second_line_panel, text='   parable  ', pady=3, command=lambda:change_button(parable))
parable.grid(row=3, column=0, columnspan=3)

curve_params_panel = Frame(toolbar)
curve_params_panel.grid(row=0, column=3)

center_label = Label(curve_params_panel, text='center x & y')
a_label = Label(curve_params_panel, text='a')
b_label = Label(curve_params_panel, text='b')
center_label.grid(row=0, column=0, columnspan=2)
a_label.grid(row=1, column=0)
b_label.grid(row=1, column=2)

center_x = Entry(curve_params_panel, width=3)
center_y = Entry(curve_params_panel, width=3)
a = Entry(curve_params_panel, width=3)
b = Entry(curve_params_panel, width=3)
draw_curve_button = Button(curve_params_panel, text='draw', pady=3, command=lambda:curve(int(center_x.get()), int(center_y.get()), int(a.get()), int(b.get())))
center_x.grid(row=0, column=2)
center_y.grid(row=0, column=3)
a.grid(row=1, column=1)
b.grid(row=1, column=3)
draw_curve_button.grid(row=3, column=0, columnspan=4)

approximation_panel = Frame(toolbar)
approximation_panel.grid(row=0, column=4)

hermite = Button(approximation_panel, text='Hermite', pady=3, command=lambda:change_button(hermite))
hermite.grid(row=0, column=0)
bezier = Button(approximation_panel, text='Bezier', pady=3, command=lambda:change_button(bezier))
bezier.grid(row=1, column=0)
bspline = Button(approximation_panel, text='B-Spline', pady=3, command=lambda:change_button(bspline))
bspline.grid(row=2, column=0)

debug_button = Button(debug_panel, image=debug_image, pady=3, command=change_debug)
debug_button.grid(row=0, column=0, sticky='ew')
next_step = Button(debug_panel, image=play_image, command=lambda:(waiting_var.set(waiting_var.get()+1)))
next_step.grid(row=0, column=1, sticky='ew')
ghostframe = Frame(debug_panel)
ghostframe.grid(row=0, column=2)

#clear = Button(toolbar, image='debug_image', pady=3, command=clear_canvas)

solve_field = st.ScrolledText(debug_panel,width = 25)
solve_field.grid(row=1, column=0, columnspan=2)

canvas = Canvas(root, width=440, height=410, bd=2)
canvas.grid(row=1, column=0)

canvas.bind('<Button-1>', draw)


root.mainloop()