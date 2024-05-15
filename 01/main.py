from tkinter import Tk, Canvas, Entry
import statistics
import random
import heapq
from time import process_time

# Global state variables
ovals = {}
points = []

# Tkinter initialization
root = Tk()
root.title("PST Visualisation")

canvas = Canvas(root)
canvas.pack()

class Node:
    def __init__(self, node_key, node_point, left_subtree, right_subtree):
        self.node_key = node_key
        self.node_point = node_point
        self.left_subtree = left_subtree
        self.right_subtree = right_subtree

def print_point(x, y):
    point = canvas.create_oval(x, y, x, y, tags="point")
    ovals[(x, y)] = point

def handle_click(click_event):
    x = canvas.canvasx(click_event.x)
    y = canvas.canvasy(click_event.y)
    print_point(x, y)
    points.append((x, y))
    construct_pst(points)
    print("Computed updated pst for points")

def generate_random_points(n):
    for i in range(0, n):
        coord = (random.randrange(0, 200), random.randrange(0, 200))
        points.append(coord)

# Computation of axis-aligned bounding box
def print_bounding_box(a, b):
    canvas.create_rectangle(a[0], a[1], b[0], b[1], tags="bounding_box")

def find_min_y_point(points):
    if not points:
        return None

    min_point = points[0]
    # Think of better default value
    min_index = 0
    for i, point in enumerate(points):
        if point[1] < min_point[1]:
            min_point = point
            min_index = i

    return min_point, min_index


def remove_point_from_data(index, data):
    return data[:index] + data[index + 1 :]


def calculate_median(data):
    return statistics.median(map(lambda point: point[0], data))

def construct_pst(data):
    if len(data) > 1:
        node_point, index = find_min_y_point(data)
        reduced_data = remove_point_from_data(index, data)
        node_key = calculate_median(reduced_data)

        left_data = []
        right_data = []

        for point in reduced_data:
            if point[0] <= node_key:
                left_data.append(point)
            else:
                right_data.append(point)

        left_subtree = construct_pst(left_data)
        right_subtree = construct_pst(right_data)

        return Node(node_key, node_point, left_subtree, right_subtree)
    elif len(data) == 1:
        return Node(None, data[0], None, None)
    elif len(data) == 0:
        return None

def range_query_2d(node, query_range_x, query_range_y):
    if node is None:
        return []

    result = []

    # Check if the node's point is within the query range
    if (
        query_range_x[0] <= node.node_point[0] <= query_range_x[1]
        and query_range_y[0] <= node.node_point[1] <= query_range_y[1]
    ):
        result.append(node.node_point)

    # Recursively search left subtree if it could intersect with the query range
    if node.left_subtree is not None and query_range_x[0] <= node.node_key:
        result.extend(range_query_2d(node.left_subtree, query_range_x, query_range_y))

    # Recursively search right subtree if it could intersect with the query range
    if node.right_subtree is not None and query_range_x[1] >= node.node_key:
        result.extend(range_query_2d(node.right_subtree, query_range_x, query_range_y))

    return result

def on_input(event):
    input_text = input_entry.get()
    print("Input received:", input_text)
    segments = input_text.split(" ")
    if len(segments) != 4:
        print("Incorrect number of arguments")
    (x0, x1, y0, y1) = map(lambda s: int(s), segments)
    canvas.delete("bounding_box")
    print_bounding_box((x0, y0), (x1, y1))

    # Start PST query
    start = process_time()
    result = range_query_2d(tree, (x0, x1), (y0, y1))
    end = process_time()
    print(f"PST query took {end - start} seconds")
    canvas.itemconfig("point", outline="black")
    for coord in result:
        canvas.itemconfig(ovals[coord], outline="red")
    print(f"Result contains: {len(result)} points")
    print(f"Query result: {result}")

    # Start naive query
    naive_start = process_time()
    naive_result = []
    for point in points:
        if x0 <= point[0] <= x1 and y0 <= point[1] <= y1:
            naive_result.append(point)
    naive_end = process_time()
    print(f"Naive query took {naive_end - naive_start} seconds")
    print(f"Result contains: {len(naive_result)} points")
    print(f"Query result: {naive_result}")

generate_random_points(1000)

# Print points to canvas
for x, y in points:
    print_point(x, y)

tree = construct_pst(points)

canvas.bind("<Button-1>", handle_click)

input_entry = Entry(root)
input_entry.pack()
input_entry.bind("<Return>", on_input)

root.mainloop()
