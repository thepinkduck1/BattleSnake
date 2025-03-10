import heapq

def moveHead(direction: str, head_position: dict[str, int]) -> dict[str, int]:
    if direction == "left":
        return {"x": head_position["x"]-1, "y": head_position["y"]}
    if direction == "up":
        return {"x": head_position["x"], "y": head_position["y"] + 1}
    if direction == "down":
        return {"x": head_position["x"], "y": head_position["y"] - 1}
    if direction == "right":
        return {"x": head_position["x"]+1, "y": head_position["y"]}

class Node:
    def __init__(self, position, g):
        self.position = position
        self.g = g
        self.parent = None

    def __lt__(self, other):
        return self.g < other.g
    
def a_star(start, goals, obstacles, grid_width, grid_height):
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    open_list = []
    heapq.heappush(open_list, Node(start, 0))

    closed_list = set()
    
    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position in goals:
            while current_node:
                if current_node.parent.position == start:
                    return current_node
                else:
                    current_node = current_node.parent
        
        closed_list.add(current_node.position)

        for direction in directions:
            neighbour_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])

            # Check neighbour in bounds and not an obstacle
            if (0 <= neighbour_position[0] <= grid_width 
                and 0 <= neighbour_position[1] <= grid_height 
                and neighbour_position not in obstacles
                and neighbour_position not in closed_list):
                
                g = current_node.g + 1
                neighbour_node = Node(neighbour_position, g)
                neighbour_node.parent = current_node

                heapq.heappush(open_list, neighbour_node)
    
    return None