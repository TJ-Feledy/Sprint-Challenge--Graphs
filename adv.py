from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
visited = set()

# create a bfs for finding shortest path to unexplored rooms
def bfs(current_room, traversed, world):
    queue = Queue()
    queue.enqueue([('', current_room.id)])
    visited = set()

    visited.add(current_room.id)

    while queue.size() > 0:
        path = queue.dequeue()
        curr_room = path[-1]
        curr_room = world.rooms[curr_room[1]]

        for direction in curr_room.get_exits():
            # If the current room is not in traversed rooms, add it to the current path
            if curr_room.get_room_in_direction(direction) not in traversed:
                path.append((direction, curr_room.get_room_in_direction(direction).id))
                return path
            # If the current rooms id is not in visited, add it and enqueue new path
            if curr_room.get_room_in_direction(direction).id not in visited:
                new_room = curr_room.get_room_in_direction(direction)
                new_path = list(path)
                new_path.append((direction, new_room.id))
                visited.add(new_room.id)
                queue.enqueue(new_path)

# add the first room to visited
visited.add(player.current_room)

# find an unexplored exit in current room and travel to it
# Run loop until all rooms are visited
while len(visited) != len(room_graph):
    room_exits = player.current_room.get_exits()
    unexplored_exit = False
    # for each room_exits
    for direction in room_exits:
        # if the current direction is not in visited, add it to visited and traversal_path, and move the player
        if player.current_room.get_room_in_direction(direction) not in visited:
            player.travel(direction)
            visited.add(player.current_room)
            traversal_path.append(direction)
            unexplored_exit = True
            break
    
    if unexplored_exit:
            continue
    
    # no more rooms left to explore on this path, perform bfs
    backtrack = bfs(player.current_room, visited, world)

    # for each direction in backtrack, move the player and add it to traversal_path
    for i in range(1, len(backtrack)):
        direction = backtrack[i][0]
        print('backtracking')
        player.travel(direction)
        traversal_path.append(direction)

    visited.add(player.current_room)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
