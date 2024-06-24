from tkinter import Tk, Canvas, Entry
import random
import math
from time import process_time

ovals = {}
points = []

root = Tk()
root.title("Smallest Enclosing Circle Visualization")

canvas = Canvas(root, width=500, height=500, bg="white")
canvas.pack()

def print_point(x, y):
    point = canvas.create_oval(x-2, y-2, x+2, y+2, fill="black", tags="point")
    ovals[(x, y)] = point

def handle_click(click_event):
    x = canvas.canvasx(click_event.x)
    y = canvas.canvasy(click_event.y)
    print_point(x, y)
    points.append((x, y))
    create_enclosing_circle()

def generate_random_points(n):
    for _ in range(n):
        coord = (random.randrange(50, 450), random.randrange(50, 450))
        points.append(coord)
        print_point(coord[0], coord[1])
    create_enclosing_circle()

def create_enclosing_circle():
    canvas.delete("circle")
    if len(points) < 2:
        return
    
    msw_start = process_time()
    msw_circle = msw(points[:], [])
    msw_end = process_time()

    msw_runtime = msw_end - msw_start

    if msw_circle:
        x, y, r = msw_circle
        canvas.create_oval(x-r, y-r, x+r, y+r, outline="red", width=2, tags="circle")

    naive_start = process_time()
    naive_circle = naive_smallest_enclosing_circle(points)
    naive_end = process_time()

    naive_runtime = naive_end - naive_start

    if naive_circle:
        x, y, r = naive_circle
        canvas.create_oval(x-r, y-r, x+r, y+r, outline="blue", width=2, tags="circle")

    print(f"MSW took: {msw_runtime:.6f} s, Naive took: {naive_runtime:.6f} s")

def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def circlep(p1, p2, p3):
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax**2 + ay**2) * (by - cy) + (bx**2 + by**2) * (cy - ay) + (cx**2 + cy**2) * (ay - by)) / d
    uy = ((ax**2 + ay**2) * (cx - bx) + (bx**2 + by**2) * (ax - cx) + (cx**2 + cy**2) * (bx - ax)) / d
    center = (ux, uy)
    radius = distance(center, p1)
    return (ux, uy, radius)

def circled(p1, p2):
    center = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    radius = distance(p1, p2) / 2
    return (center[0], center[1], radius)

def is_in_circle(point, circle):
    if not circle:
        return False
    return distance(point, (circle[0], circle[1])) <= circle[2]

def draw_circle(circle, color):
    if circle:
        x, y, r = circle
        canvas.create_oval(x-r, y-r, x+r, y+r, outline=color, tags="circle")

def msw(points, boundary, depth=0):
    if not points or len(boundary) == 3:
        if len(boundary) == 0:
            return None
        elif len(boundary) == 1:
            return (boundary[0][0], boundary[0][1], 0)
        elif len(boundary) == 2:
            return circled(boundary[0], boundary[1])
        elif len(boundary) == 3:
            circle = circlep(boundary[0], boundary[1], boundary[2])
            draw_circle(circle, "blue")
            root.update()
            return circle
    else:
        p = points.pop(random.randint(0, len(points) - 1))
        circle = msw(points[:], boundary[:], depth + 1)

        if circle and is_in_circle(p, circle):
            return circle
        else:
            boundary.append(p)
            circle = msw(points[:], boundary[:], depth + 1)
            draw_circle(circle, "blue")
            canvas.itemconfig(ovals[p], outline="red")
            root.update()
            canvas.after(500)
            return circle

def naive_smallest_enclosing_circle(points):
    if len(points) == 0:
        return None
    elif len(points) == 1:
        return (points[0][0], points[0][1], 0)
    elif len(points) == 2:
        return circled(points[0], points[1])

    min_circle = None

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                circle = circlep(points[i], points[j], points[k])
                if all(is_in_circle(p, circle) for p in points):
                    if min_circle is None or circle[2] < min_circle[2]:
                        min_circle = circle

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            circle = circled(points[i], points[j])
            if all(is_in_circle(p, circle) for p in points):
                if min_circle is None or circle[2] < min_circle[2]:
                    min_circle = circle

    return min_circle

# Uncomment to generate random points
# generate_random_points(20)

# Print points to canvas
for x, y in points:
    print_point(x, y)

canvas.bind("<Button-1>", handle_click)

root.mainloop()
