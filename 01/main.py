from tkinter import Tk, Canvas
import statistics
import random
import heapq

root = Tk()
canvas = Canvas(root)
canvas.pack()


def print_point(x, y):
    canvas.create_oval(x, y, x, y)


def print_line(a, b):
    canvas.create_line(a[0], a[1], b[0], b[1])


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


def generate_random_points(n):
    for i in range(0, n):
        coord = (random.randrange(0, 200), random.randrange(0, 200))
        points.append(coord)


generate_random_points(1000)

# Print points
for x, y in points:
    print_point(x, y)

# Print edges
print_line((0, 10), (30, 50))


# Computation of axis-aligned bounding box
def print_bounding_box(a, b):
    canvas.create_rectangle(a[0], a[1], b[0], b[1])


print_bounding_box((20, 20), (70, 80))


canvas.bind("<Button-1>", handle_click)
root.mainloop()


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
    return points[:index] + points[index + 1 :]


def calculate_median(data):
    return statistics.median(map(lambda point: point[0], data))


class Node:
    def __init__(self, node_key, node_point, left_subtree, right_subtree):
        self.node_key = node_key
        self.node_point = node_point
        self.left_subtree = left_subtree
        self.right_subtree = right_subtree


class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data


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
        return Node(None, Node, None, None)
    elif len(data) == 0:
        return None


class Node:
    def __init__(self, point):
        self.point = point
        self.left = None
        self.right = None


def build_pst(points):
    if not points:
        return None

    min_heap = [(point[0], point) for point in points]
    heapq.heapify(min_heap)

    root = None
    while min_heap:
        _, point = heapq.heappop(min_heap)
        root = insert(root, point)

    return root


def insert(root, point):
    if not root:
        return Node(point)

    if point[0] < root.point[0]:
        root.left = insert(root.left, point)
    else:
        root.right = insert(root.right, point)

    return root


def range_query(root, x_min, x_max, y_min, y_max):
    if not root:
        return []

    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        if x_min <= node.point[0] <= x_max and y_min <= node.point[1] <= y_max:
            result.append(node.point)

        if node.left and x_min <= node.point[0]:
            stack.append(node.left)

        if node.right and node.point[0] <= x_max:
            stack.append(node.right)

    return result


# node = construct_pst(points)
# print(node.node_point)
# print(node.left_subtree)
# print(node.right_subtree)
points = [(3, 5), (1, 2), (4, 6), (2, 3), (5, 7)]
pst_root = build_pst(points)

x_min, x_max, y_min, y_max = 2, 4, 4, 7
result = range_query(pst_root, x_min, x_max, y_min, y_max)
print(result)
