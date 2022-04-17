from flask import Flask, render_template, request, redirect
from heapq import *
from configparser import MAX_INTERPOLATION_DEPTH
from math import fabs
import random
import requests
app = Flask(__name__)

@app.route('/', methods=['GET'])
def indexGET():
    rows = [grid, []]
    # [grid: [[0, 1, 3],[1, 2, 1]]]
    return render_template('index.html', rows=rows)


@app.route('/r-<ax>-<ay>-<int0>', methods=['GET'])
def indexwpathAnGET(ax, ay, int0):
    render_form(int(ax), int(ay), int(int0))
    rows = [grid, []]
    return render_template('index.html', rows=rows)

@app.route('/<ax>-<ay>-<bx>-<by>', methods=['GET'])
def indexwpathGET(ax, ay, bx, by):
    path = count_path(int(ax), int(ay), int(bx), int(by))
    rows = [grid, path]
    return render_template('index.html', rows=rows)

@app.route('/', methods=['POST'])
def indexPOST():
    form = request.form
    render_form(form)
    redirect('/')

@app.route('/<ax>-<ay>-<bx>-<by>', methods=['POST'])
def indexwpathPOST(ax, ay, bx, by):
    form = request.form
    render_form(form)
    return redirect(f'/{ax}-{ay}-{bx}-{by}')



def render_form(new_x, new_y, new_int):
    global grid, anomalies
    anomalies.add((new_x, new_y, new_int))
    grid = generate_map(get_anomalies(parse_data()) + list(anomalies))

anomalies = set()


def count_path(ax, ay, bx, by):
    path = best_path(grid, (ax, ay), (bx, by))
    npath = []
    for k in path:
        npath.append([k[1], k[0]])
    return npath

grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 4, 4, 4, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 5, 7, 8, 7, 5, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 5, 9, 14, 18, 14, 9, 5, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 7, 14, 35, 70, 35, 14, 7, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 8, 18, 70, 70, 70, 18, 8, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 7, 14, 35, 70, 35, 14, 7, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 5, 9, 14, 18, 14, 9, 5, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 2, 2, 8, 7, 5, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 2, 2, 3, 4, 5, 6, 5, 4, 3, 2, 4, 4, 3, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 2, 3, 4, 4, 4, 4, 4, 2, 4, 6, 10, 12, 10, 6, 4, 2, 3, 2, 2, 6, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 2, 3, 4, 5, 7, 8, 7, 5, 3, 5, 10, 25, 50, 25, 10, 5, 3, 60, 60, 15, 7, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 2, 4, 5, 9, 14, 18, 14, 2, 3, 6, 12, 50, 50, 50, 12, 6, 3, 2, 30, 12, 6, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 3, 4, 7, 14, 35, 70, 35, 14, 3, 5, 10, 25, 50, 25, 10, 5, 3, 15, 12, 8, 5, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 3, 4, 8, 18, 70, 70, 70, 18, 2, 4, 6, 10, 12, 10, 6, 4, 2, 7, 6, 5, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 3, 4, 7, 14, 35, 70, 35, 14, 2, 3, 4, 5, 6, 5, 4, 3, 2, 4, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 2, 4, 5, 9, 14, 18, 14, 9, 5, 2, 2, 3, 3, 3, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 2, 3, 4, 5, 7, 8, 7, 5, 4, 3, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 2, 3, 4, 4, 4, 4, 4, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 2, 2, 0, 0, 0, 0, 2, 3, 4, 4, 4, 3, 2, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 5, 6, 5, 4, 3, 2, 0, 0, 2, 3, 5, 6, 7, 6, 5, 3, 2, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 6, 10, 12, 10, 6, 4, 2, 0, 2, 3, 5, 8, 12, 15, 12, 8, 5, 3, 2, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 10, 25, 50, 25, 10, 5, 3, 0, 2, 4, 6, 12, 30, 60, 30, 12, 6, 4, 2, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 6, 12, 50, 50, 50, 12, 6, 3, 2, 2, 4, 7, 15, 60, 60, 60, 15, 7, 4, 2, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 5, 10, 25, 50, 25, 10, 5, 3, 0, 2, 4, 6, 12, 30, 60, 30, 12, 6, 4, 2, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 6, 10, 12, 10, 6, 4, 2, 0, 2, 3, 5, 8, 12, 15, 12, 8, 5, 3, 2, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 4, 5, 6, 5, 4, 3, 2, 0, 0, 2, 3, 5, 6, 7, 6, 5, 3, 2, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 2, 2, 0, 0, 0, 0, 2, 3, 4, 4, 4, 3, 2, 0, 0, 0, 0, 0, 0]]



cols = 40
rows = 30

def get_neighbours(x, y):
    check_neighbour = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_neighbour(x + dx, y + dy)]

def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])

def dijkstra(start, goal, graph):
    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        neighbours = graph[cur_node]
        for neighbour in neighbours:
            neigh_cost, neigh_node = neighbour
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node
    return visited


def best_path(grid, start, end):
    path = []
    graph = {}
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_neighbours(x, y)

    goal = end
    queue = []
    heappush(queue, (0, start))
    visited = {start: None}
    visited = dijkstra(start, goal, graph)
    while visited[goal] != None:
        path.append(goal)
        goal = visited[goal]
    path.append(goal)
    return path


url = "https://dt.miet.ru/ppo_it_final"
header = {
    'X-Auth-Token': 'kooxicjx'
}

def vector_length(x1, x2, y1, y2):
    return (x2 - x1) ** 2 + (y2 - y1) ** 2

def calculate_dot(x1, y1, int1, x2, y2, int2):
    coords = set()

    for x0 in range(0, 40):
        for y0 in range(0, 30):
            if x0 == x1 and y0 == y1:
                continue
            frac1 = vector_length(x0, x2, y0, y2) / vector_length(x0, x1, y0, y1)
            frac2 = int1 / int2
            if frac2 <= 1:
                if round(frac1, 3) == round(frac2, 3):
                    coords.add((x0, y0))
            else:
                if fabs(frac1-frac2) <= 0.05:
                    coords.add((x0, y0))
    
    return coords

def parse_data():
    r = requests.get(url, headers=header)

    message = r.json()['message']

    anomalies = {}

    for data in message:
        coords = data['coords']
        for swan in data['swans']:
            swan_id = swan['id']
            rate = swan['rate']

            anomalies[swan_id] = anomalies.get(swan_id, [])
            anomalies[swan_id].append((*coords, rate))

    return anomalies

def get_anomalies(anomalies):
    answer = []
    for anomaly in anomalies.values():
        coords = None
        for i in range(0, len(anomaly)):
            for j in range(i+1, len(anomaly)):
                x1, y1, int1 = anomaly[i]
                x2, y2, int2 = anomaly[j]

                result = calculate_dot(x1, y1, int1, x2, y2, int2)
                if coords is None:
                    coords = result
                else:
                    if result != set():
                        coords = coords.intersection(result)


        x0, y0 = list(coords)[0]
        rx, ry, rate = random.choice(anomaly)
        r2 = vector_length(x0, rx, y0, ry)
        int0 = round(rate * r2)
        answer.append((x0, y0, int0))

    return answer

def generate_map(anomalies):
    grid = []
    for _ in range(0, 30):
        grid.append([0] * 40)

    for anomaly in anomalies:
        x0, y0, int0 = anomaly
        max_dist = int0 // 2
        for x in range(-max_dist, max_dist):
            for y in range(-max_dist, max_dist):
                if x ** 2 + y ** 2 <= max_dist:
                    if x ** 2 + y ** 2 != 0:
                        if 0 <= y0 + y < 30:
                            if 0 <= x0 + x < 40:
                                grid[y0+y][x0+x] = round(int0 / (x ** 2 + y ** 2))
                    else:
                        grid[y0][x0] = int0

    return grid


if __name__ == '__main__':
    app.run()