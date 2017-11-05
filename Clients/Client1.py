# Project: Atomic Games 2017
# Authors: Alex Cadigan and Skyler Norgaard
# Date Last Modified: 11/3/2017
# Description: This file contains code to run a client to play a simple video game.  The
# client uses a simple AI to play the game.  Currently the AI has workers move in random
# directions.  If they stumble upon a resource, they will collect it.  Then they continue 
# to move randomly

# Imports:
import json
import random
import sys

# Imports the socket server in the method corresponding to which Python version is being used
if (sys.version_info > (3, 0)):

    print("Python 3.X detected")
    import socketserver as socketServer

else:

    print("Python 2.X detected")
    import SocketServer as socketServer

# This class deals with all incoming network issues
class NetworkHandler(socketServer.StreamRequestHandler):

	# This class handles the incoming json data from the server
    def handle(self):

        game = Game()

        # Runs constantly while the game is running
        while True:

        	# Reads in data until an "\n" is encountered
            data = self.rfile.readline().decode()
            jsonData = json.loads(str(data))

            # Prints the json data from the server
            print(json.dumps(jsonData, indent = 4, sort_keys = True))

            # Creates and sends a response to the server with unit commands
            gameResponse = game.getRandomMove(jsonData).encode()
            self.wfile.write(gameResponse)

# This class contains functions to control the game and command units
class Game:

	# This method is called when an instance of this class is created
    def __init__(self):

    	# Holds the set of unit IDs
        self.units = set()
        self.directions = ['N', 'S', 'E', 'W']

   	# This method sends a command to move a random unit in a random direction
    def getRandomMove(self, jsonData):

    	# Stores the unit IDs of the units currently in the game
        units = set([unit['id'] for unit in jsonData['unit_updates'] if unit['type'] != 'base'])

        # Unions the two sets together
        self.units |= units

        # Builds the command to move a random unit in a random direction
        unit = random.choice(tuple(self.units))
        direction = random.choice(self.directions)
        command = {"commands": [{"command": "MOVE", "unit": unit, "dir": direction}]}
        response = json.dumps(command, separators=(',',':')) + '\n'
        return response

# Starts the client listening from an incoming connection from the server
if __name__ == "__main__":
	
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 9090
    host = '0.0.0.0'

    server = socketServer.TCPServer((host, port), NetworkHandler)
    print("listening on {}:{}".format(host, port))
    server.serve_forever()
