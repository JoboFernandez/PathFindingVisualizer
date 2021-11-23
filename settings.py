WIDTH, HEIGHT = 600, 600
EXTENSION = 300

ALGORITHMS = [
    "A* Search - Euclidian Heuristic",
    "A* Search - Manhattan Heuristic",
    "Bellman-Ford Algorithm",
    "Breadth-First Search",
    "Depth-First Search",
    "Dijkstra's Algorithm",
    "Greedy Best First Search - Euclidian",
    "Greedy Best First Search - Manhattan",
    "Iterative Deepening Search",
    "Uniform Cost Search",
]
algo_index = 0

RED = (255, 0, 0)                 # Starting Point
BLUE = (0, 0, 255)                # Ending Point
WHITE = (255, 255, 255)           # Passable Terrain
BLACK = (0, 0, 0)                 # Impassable Terrain
GRAY = (100, 100, 100)            # Terrain Boundary / Neutral
EMERALD = (0, 135, 15)            # Terrain on Visit Queue
SEAFOAM = (60, 235, 150)          # Visited Terrain
CHARTREUSE = (210, 215, 105)    # Shortest Path
