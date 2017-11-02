#!/usr/bin/python

import sys
import json
import random
import numpy as np

if (sys.version_info > (3, 0)):
    print("Python 3.X detected")
    import socketserver as ss
else:
    print("Python 2.X detected")
    import SocketServer as ss


class NetworkHandler(ss.StreamRequestHandler):
    def handle(self):
        game = Game()

        start = True
        while True:
            data = self.rfile.readline().decode() # reads until '\n' encountered
            json_data = json.loads(str(data))
            grid = game.get_grid()

            #print(json.dumps(json_data, indent=4, sort_keys=True))
            #print(game.find_barriers(json_data))

            #get initial locations, or anythig else we'd want to get at beginning
            if start == True:
                locations = game.get_initial_location(json_data)
                all_units = units = set([unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base'])
                response = game.move_all_randomly(json_data, all_units).encode()
                self.wfile.write(response)
                start = False

            else:
                locations = game.update_location(json_data, locations) #get new locations after each move
                response = game.move_all_randomly(json_data, all_units).encode()
                print(locations)
                self.wfile.write(response)





            # uncomment the following line to see pretty-printed data
            #print(json.dumps(json_data, indent=4, sort_keys=True))

            #response = game.get_random_move(json_data).encode()
            #self.wfile.write(response)




class Game:
    def __init__(self):
        self.units = set() # set of unique unit ids
        self.directions = ['N', 'S', 'E', 'W']
        self.informed_grid = np.zeros((100,100))
        self.informed_grid[49,49] = 1
        #self.base_loc = [unit['id'] for unit in json_data['unit_updates'] if unit['type'] == 'base']

    def get_grid(self):
        return self.informed_grid.astype(int)

    #want this to initialize a dictionary in form ID:position
    def get_initial_location(self, json_data):
        units = [unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base']
        x_locs = [unit['x']+49 for unit in json_data['unit_updates'] if unit['type'] != 'base']
        y_locs = [unit['y']+49 for unit in json_data['unit_updates'] if unit['type'] != 'base']
        locations = list(zip(x_locs, y_locs))
        location_dict = dict(zip(units, locations))
        return location_dict

    #updates location using most recent data from the server
    def update_location(self, json_data, location_dict):
        #after the first move, this will not necessarily return all units, only ones that were
        #actually updated
        updated_units = [unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base']
        x_locs = [unit['x']+49 for unit in json_data['unit_updates'] if unit['type'] != 'base']
        y_locs = [unit['y']+49 for unit in json_data['unit_updates'] if unit['type'] != 'base']
        updated_locations = list(zip(x_locs, y_locs))
        updated_location_dict = dict(zip(updated_units, updated_locations))

        #want to change the value in the dictionary for any bots that were updated in previous round
        for ID in updated_units:
            location_dict[ID] = updated_location_dict[ID]

        return location_dict

    '''
    #function to find barriers and add them to our grid
    def find_barriers(self, json_data):
        tiles = json_data["tile_updates"] #returns list of dictionaries containing tile information
        x_locs = []
        y_locs = []
        for i in range(len(tiles)):
            one_tile = tiles[i] #save information for one tile as a variable, this will be a dictionary
            if one_tile["blocked"]==True:
                x_loc_relative = one_tile["x"] + 49
                y_loc_relative = one_tile["y"] + 49
                #add elements to list of x and y coords
                x_locs.append(x_loc_relative)
                y_locs.append(y_loc_relative)
                #update our informed grid accordingly
                self.informed_grid[x_loc_relative, y_loc_relative] = 1
        barriers = zip(x_locs, y_locs)
        return(barriers)
    '''

    def move_all_randomly(self, json_data, units):
        #units = set([unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base'])
        self.units |= units # add any additional ids we encounter

        commands = {}
        command_list = []

        for unit in units:
            move_command = {"command": "MOVE", "unit": unit, "dir": random.choice(self.directions)}
            gather_command = {"command": "GATHER", "unit": unit, "dir": random.choice(self.directions)}
            command_list.append(move_command)
            command_list.append(gather_command)

        commands = {"commands": command_list}

        #print(response)
        response = json.dumps(commands, separators=(',',':')) + '\n'
        return response




    def get_random_move(self, json_data):
        units = set([unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base'])
        self.units |= units # add any additional ids we encounter
        unit = random.choice(tuple(self.units)) #choose a random unit to move

        direction = random.choice(self.directions) #choose a random direction to move it in
        move = 'MOVE'
        command = {"commands": [{"command": move, "unit": unit, "dir": direction}]} #move the random unit in the random direction
        response = json.dumps(command, separators=(',',':')) + '\n'
        return response

    #THIS WOULD BE USED ONCE BOTS START HITTING BARRIERS BUT THE RESOURCES OR OTHER BASE ARE UNKNOWN
    #AT THIS POINT, I THINK IT STILL MAKES SENSE FOR THE BOTS TO MOVE RANDOMLY
    def get_informed_move_no_goal_yet(self, json_data, informed_grid):
        units = set([unit['id'] for unit in json_data['unit_updates'] if unit['type'] != 'base'])
        self.units |= units # add any additional ids we encounter
        unit = random.choice(tuple(self.units)) #choose a random unit to move

        #WE WANT TO CHECK WHERE WE CAN MOVE:



    '''
    #I WANT TO MAKE A FUNCTION THAT NOTIFIES THE OTHER BOTS OF A LOCATION FOR RESOURCES
    def notify_of_resources(self, )
    #HEURISTIC FOR THE PATH FINDING ALGORITHM
    def heuristic(self, start, goal):
        (x1, y1) = start
        (x2, y2) = goal
        return abs(x1 - x2) + abs(y1 - y2)
    #
    def a_star_search(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
    '''

if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 9090
    host = '0.0.0.0'

    server = ss.TCPServer((host, port), NetworkHandler)
    print("listening on {}:{}".format(host, port))
    server.serve_forever()