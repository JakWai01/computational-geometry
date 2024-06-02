from tkinter import Tk, Canvas, Entry

def gift_wrapping(S):
    # Helper function to find the point with the smallest y-coordinate (and leftmost if tie)
    def lowest_point(points):
        lowest = points[0]
        for point in points:
            if point[1] < lowest[1] or (point[1] == lowest[1] and point[0] < lowest[0]):
                lowest = point
        return lowest

    # Helper function to determine if point c is to the left of line formed by points a and b
    def is_left(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0

    # Initialize the convex hull set
    convex_hull = []

    # Find the lowest point
    point_on_hull = lowest_point(S)

    while True:
        # Add the current point to the convex hull
        convex_hull.append(point_on_hull)
        # Initialize endpoint for the candidate edge on the hull
        endpoint = S[0]

        for j in range(1, len(S)):
            # Check if we need to update the endpoint
            if endpoint == point_on_hull or is_left(convex_hull[-1], endpoint, S[j]):
                endpoint = S[j]

        # Move to the next point on the hull
        point_on_hull = endpoint

        # If we have wrapped around to the first hull point, break the loop
        if endpoint == convex_hull[0]:
            break

    return convex_hull

def print_point(x, y):
    point = canvas.create_oval(x, y, x, y, tags="point")
    ovals[(x, y)] = point

def print_line(a, b):
    canvas.create_line(a[0], a[1], b[0], b[1], fill="green", width=1, tags="lines")

def handle_click(click_event):
    x = canvas.canvasx(click_event.x)
    y = canvas.canvasy(click_event.y)
    print_point(x, y)
    points.append((x, y))
    hull = gift_wrapping(points)
    canvas.delete("lines")

    hull.append(hull[0])  # Close the loop by appending the first point at the end
    for i in range(len(hull) - 1):
        print(i)
        print((i + 1) % len(hull))
        print_line(hull[i], hull[(i + 1) % len(hull)])

    print("Computed updated gift wrapping for points")
    print(hull)
    
# Global state variables
ovals = {}
points = []

# Tkinter initialization
root = Tk()
root.title("Gift Wrapping Algorithm")

canvas = Canvas(root)
canvas.pack()

canvas.bind("<Button-1>", handle_click)
# Example usage:
# points = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3)]
# hull = gift_wrapping(points)
# print(hull)

root.mainloop()

