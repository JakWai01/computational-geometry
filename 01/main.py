from tkinter import Tk, Canvas

root = Tk()
canvas = Canvas(root)
canvas.pack()


def print_point(x, y):
    canvas.create_oval(x, y, x, y)


def handle_click(click_event):
    x = canvas.canvasx(click_event.x)
    y = canvas.canvasy(click_event.y)
    print_point(x, y)


points = []

with open("coords.txt") as f:
    for line in f:
        x_str, y_str = line.split()
        coords = (float(x_str), float(y_str))
        points.append(coords)

for x, y in points:
    print_point(x, y)

canvas.bind("<Button-1>", handle_click)
root.mainloop()
