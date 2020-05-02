from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


def dft_recursive(starting_vertex, path={}):
    # add starting vertex to visited
    path[starting_vertex.id] = {}
    print('vertex', starting_vertex.id)
    # get the neighbors of the starting vertex
    # build a graph for exits
    directions = starting_vertex.get_exits()


    # if no neighbors, return
    # else for each neighbor
        # if it is not in visited, run recursion with neighbor as starting vertex
        # else return
    if len(directions) == 1:
        # ********if nowhere to go, find shortest path back to next unexplored room********
        print(traversal_path)
    else:
        for direction in directions:
            if direction not in dict(path[starting_vertex.id]):
                if direction == 'n':
                    path[starting_vertex.id].update({'n': starting_vertex.n_to.id})
                    dft_recursive(starting_vertex.n_to)
                if direction == 's':
                    path[starting_vertex.id].update({'s': starting_vertex.s_to.id})
                    dft_recursive(starting_vertex.s_to)
                if direction == 'e':
                    path[starting_vertex.id].update({'e': starting_vertex.e_to.id})
                    dft_recursive(starting_vertex.e_to)
                if direction == 'w':
                    path[starting_vertex.id].update({'w': starting_vertex.w_to.id})
                    dft_recursive(starting_vertex.w_to)
                traversal_path.append(direction)
            # if direction not in path:
            #     dft_recursive(direction, path)
            else:
                print('hey, hey, hey')
    print('endPath', path)
dft_recursive(player.current_room)
print('traverse', traversal_path)

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
