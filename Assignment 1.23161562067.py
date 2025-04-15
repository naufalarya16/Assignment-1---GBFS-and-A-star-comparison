import heapq
import time

grid_str = [
    "S..#......",
    ".#.#.####.",
    ".#......#.",
    ".#####..#.",
    ".....#..#G",
    "####.#..##",
    "...#.#....",
    ".#.#.####.",
    ".#........",
    "....#####."
]

grid = [list(row) for row in grid_str]
ROWS, COLS = len(grid), len(grid[0])


for r in range(ROWS):
    for c in range(COLS):
        if grid[r][c] == 'S':
            start = (r, c)
        elif grid[r][c] == 'G':
            goal = (r, c)

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def neighbors(pos):
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    result = []
    for dr, dc in directions:
        nr, nc = pos[0]+dr, pos[1]+dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] != '#':
            result.append((nr, nc))
    return result

def greedy_bfs(start, goal):
    visited = set()
    came_from = {}
    heap = [(manhattan(start, goal), start)]
    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)
        for neighbor in neighbors(current):
            if neighbor not in visited:
                came_from[neighbor] = current
                heapq.heappush(heap, (manhattan(neighbor, goal), neighbor))
    return reconstruct_path(came_from, start, goal), visited

def a_star(start, goal):
    visited = set()
    came_from = {}
    g_score = {start: 0}
    heap = [(manhattan(start, goal), start)]
    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)
        for neighbor in neighbors(current):
            temp_g = g_score[current] + 1
            if neighbor not in g_score or temp_g < g_score[neighbor]:
                g_score[neighbor] = temp_g
                f = temp_g + manhattan(neighbor, goal)
                came_from[neighbor] = current
                heapq.heappush(heap, (f, neighbor))
    return reconstruct_path(came_from, start, goal), visited

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []  
    path.append(start)
    path.reverse()
    return path

def print_grid_with_path(path):
    grid_copy = [row.copy() for row in grid]
    for r, c in path:
        if grid_copy[r][c] not in ('S', 'G'):
            grid_copy[r][c] = '*'
    for row in grid_copy:
        print("".join(row))

def run_and_compare():
    print("=== Greedy Best-First Search ===")
    t1 = time.time()
    path_gbfs, visited_gbfs = greedy_bfs(start, goal)
    t2 = time.time()
    print_grid_with_path(path_gbfs)
    print(f"Time: {t2 - t1:.6f}s")
    print(f"Path length: {len(path_gbfs)}")
    print(f"Nodes explored: {len(visited_gbfs)}\n")

    print("=== A* Search ===")
    t1 = time.time()
    path_astar, visited_astar = a_star(start, goal)
    t2 = time.time()
    print_grid_with_path(path_astar)
    print(f"Time: {t2 - t1:.6f}s")
    print(f"Path length: {len(path_astar)}")
    print(f"Nodes explored: {len(visited_astar)}")

run_and_compare()