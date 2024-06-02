from tkinter import Tk, Canvas, Button

class GiftWrappingStep:
    def __init__(self, points):
        self.points = points
        self.convex_hull = []
        self.point_on_hull = None
        self.endpoint = None
        self.j = 0
        self.finished = False
        self.current_point = None  # To track the current point being processed

    def step(self):
        if self.finished:
            return None

        if not self.convex_hull:
            # Initialization
            self.point_on_hull = self.lowest_point(self.points)
            self.convex_hull.append(self.point_on_hull)
            self.endpoint = self.points[0]
            self.j = 1
            print(f"Initialization: point_on_hull = {self.point_on_hull}")
            return self.point_on_hull

        if self.j < len(self.points):
            # Find the next endpoint
            self.current_point = self.points[self.j]
            if self.endpoint == self.point_on_hull or self.is_left(self.convex_hull[-1], self.endpoint, self.current_point):
                self.endpoint = self.current_point
            self.j += 1
            print(f"Checking point: {self.current_point}, current endpoint: {self.endpoint}")
            return None
        else:
            # Move to the next point on the hull
            self.point_on_hull = self.endpoint
            if self.endpoint == self.convex_hull[0]:
                self.finished = True
                print("Finished: closing the hull")
                print_line(hull_points[-1], hull_points[0])
            else:
                self.convex_hull.append(self.point_on_hull)
                self.endpoint = self.points[0]
                self.j = 1
                print(f"Adding point to hull: {self.point_on_hull}")
                return self.point_on_hull

    def lowest_point(self, points):
        lowest = points[0]
        for point in points:
            if point[1] < lowest[1] or (point[1] == lowest[1] and point[0] < lowest[0]):
                lowest = point
        return lowest

    def is_left(self, a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0

def print_point(x, y, color='black'):
    point = canvas.create_oval(x-3, y-3, x+3, y+3, fill=color, tags="point")
    ovals[(x, y)] = point

def print_line(a, b):
    canvas.create_line(a[0], a[1], b[0], b[1], fill="green", width=1, tags="lines")

def handle_click(click_event):
    x = canvas.canvasx(click_event.x)
    y = canvas.canvasy(click_event.y)
    print_point(x, y)
    points.append((x, y))

def step_through_algorithm():
    if not step_generator:
        return

    if step_generator.current_point:
        x, y = step_generator.current_point
        canvas.itemconfig(ovals[(x, y)], fill='black')  # Reset color of the last processed point

    result = step_generator.step()
    if result:
        hull_points.append(result)
        if len(hull_points) > 1:
            print_line(hull_points[-2], hull_points[-1])
        if step_generator.finished:
            print_line(hull_points[-1], hull_points[0])
            print("Computed updated gift wrapping for points")
            print(hull_points)

    if step_generator.current_point:
        x, y = step_generator.current_point
        canvas.itemconfig(ovals[(x, y)], fill='red')  # Highlight current point

# Global state variables
ovals = {}
points = []
hull_points = []
step_generator = None

# Tkinter initialization
root = Tk()
root.title("Gift Wrapping Algorithm")

canvas = Canvas(root)
canvas.pack(fill="both", expand=True)
canvas.bind("<Button-1>", handle_click)

def start_algorithm():
    global step_generator
    step_generator = GiftWrappingStep(points)
    hull_points.clear()
    canvas.delete("lines")
    step_through_algorithm()

def next_step():
    step_through_algorithm()

start_button = Button(root, text="Start", command=start_algorithm)
start_button.place(x=5, y=5)

next_button = Button(root, text="Next Step", command=next_step)
next_button.place(x=60, y=5)

root.mainloop()
