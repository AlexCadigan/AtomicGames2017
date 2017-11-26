# Project: Atomic Games 2017
# Authors: Alex Cadigan and Skyler Norgaard
# Date Last Modified: 11/13/2017
# Description: This file contains code to run a client to play a video game.  The
# client uses a simple AI to play the game.  Currently the AI has workers move in random
# directions.  The workers will not try to move into walls or other blocked objects.

# Imports:
import json
import random
import sys

# Imports the socket server in the method corresponding to which Python version is being used
if (sys.version_info > (3, 0)):

    import socketserver as socketServer

else:

    import SocketServer as socketServer

# This class deals with all network connections
class NetworkHandler(socketServer.StreamRequestHandler):

    # This function controls all subsequent processes of the AI
    def handle(self):

        game = Game()

        # Runs constantly while the game is running
        while True:

            # Reads in json data from server
            data = self.rfile.readline().decode()
            jsonData = json.loads(str(data))

            # Prints the json data
            # print(json.dumps(jsonData, indent = 4, sort_keys = True))

            # Creates commands to send back to the server
            (commands, proceed) = game.getCommands(jsonData)

            # Prints the command that is about to be sent to the server
            # print(json.dumps(json.loads(str(commands)), indent = 4, sort_keys = True))

            # If the command is not empty it will be sent to the server
            if proceed:

                self.wfile.write(commands.encode())

# This class contains functions to control the game and command units
class Game:

    # This function initiates some useful variables
    def __init__(self):

        self.directions = ['N', 'S', 'E', 'W']

        # A dictionary is used to hold general information about units
        self.unitInfo = {}

        # These are the blocked coordinates in the game (blocked by walls or resources)
        self.blockedXCoords = []
        self.blockedYCoords = []

        # These are the coordinates of resources
        self.resourceXCoords = []
        self.resourceYCoords = []

    # This function controls the creation of commands
    def getCommands(self, jsonData):

        # Collects general information about the units
        self.collectUnitInfo(jsonData)

        # Collects the coordinates of blocked tiles (blocked by walls or resources)
        self.storeBlockedCoords(jsonData)

        # Collects the coordinates of resources
        self.storeResourceCoords(jsonData)

        # Data structures to hold commands
        masterCommand = {}
        commands = []

        # Builds the commands to move each unit in a random direction
        for unit in self.unitInfo:

            # Makes sure unit is a worker
            if self.unitInfo[unit]['Type'] == "worker":

                # Makes sure unit is not currently moving
                if self.unitInfo[unit]['Status'] != "moving":

                    # Gets a direction for the unit to move in
                    self.directions = ['N', 'S', 'E', 'W']
                    (direction, proceed) = self.getDirection(unit)
                    while (not proceed):

                        (direction, proceed) = self.getDirection(unit)

                    # Generates the commands
                    command = {"command": "MOVE", "unit": unit, "dir": direction}
                    commands.append(command)

                # Makes sure the unit is not currently carrying a resource
                if self.unitInfo[unit]['Resources'] == 0:

                    # Collects any resources near the unit
                    (resourceDirection, proceed2) = self.getResourceDirection(unit)
                    if proceed2:

                        command = {"command": "GATHER", "unit": unit, "dir": resourceDirection}
                        commands.append(command)

                # Identifies the unit (makes a little nametag pop up next to the unit)
                command = {"command": "IDENTIFY", "unit": unit, "name": unit}
                commands.append(command)

        # Returns the finalized commands
        masterCommand = {"commands": commands}
        response = json.dumps(masterCommand, separators=(',',':')) + '\n'
        if len(commands) == 0:

            return (response, False)

        else:

            return (response, True)

    # Stores general information about the units present in the game
    def collectUnitInfo(self, jsonData):

         for unit in jsonData['unit_updates']:

            self.unitInfo[unit['id']] = {'Type': unit['type'], 'X': unit['x'], 'Y': unit['y'], 'Status': unit['status'], 'Resources': unit['resource']}

    # Stores the coordinates of the blocked tiles (blocked by walls or resources)
    def storeBlockedCoords(self, jsonData):

        # Stores the new blocked coordinates from the json data
        blockedXCoords = []
        blockedYCoords = []
        for tile in jsonData['tile_updates']:

            if tile['visible'] and tile['blocked']:

                blockedXCoords.append(tile['x'])
                blockedYCoords.append(tile['y'])

        # Integrates the new blocked coordinates into the older ones
        for index, coord in enumerate(blockedXCoords):

            duplicate = False
            for subIndex, oldCoord in enumerate(self.blockedXCoords):

                if blockedXCoords[index] == self.blockedXCoords[subIndex] and blockedYCoords[index] == self.blockedYCoords[subIndex]:

                    duplicate = True

            if  not duplicate:

                self.blockedXCoords.append(blockedXCoords[index])
                self.blockedYCoords.append(blockedYCoords[index])

    # Stores the coordinates of resources
    def storeResourceCoords(self, jsonData):

        # Stores the new resource coordinates from the json data
        resourceXCoords = []
        resourceYCoords = []
        for tile in jsonData['tile_updates']:

            if tile['visible'] and str(tile['resources']) != "None":

                resourceXCoords.append(tile['x'])
                resourceYCoords.append(tile['y'])

        # Integrates the new resource coordinates into the older ones
        for index, coord in enumerate(resourceXCoords):

            duplicate = False
            for subIndex, oldCoord in enumerate(self.resourceXCoords):

                if resourceXCoords[index] == self.resourceXCoords[subIndex] and resourceYCoords[index] == self.resourceYCoords[subIndex]:

                    duplicate = True

            if not duplicate:

                self.resourceXCoords.append(resourceXCoords[index])
                self.resourceYCoords.append(resourceYCoords[index])

    # Returns a direction for the given unit to move in (that is not blocked)
    def getDirection(self, unit):

        direction = random.choice(self.directions)

        # Makes sure that the selected direction will not move the unit into a blocked object
        for index, coord in enumerate(self.blockedXCoords):

            if direction == 'N' and self.unitInfo[unit]['X'] == self.blockedXCoords[index] and self.unitInfo[unit]['Y'] - 1 == self.blockedYCoords[index]:

                self.directions.remove('N')
                return (direction, False)

            elif direction == 'S' and self.unitInfo[unit]['X'] == self.blockedXCoords[index] and self.unitInfo[unit]['Y'] + 1 == self.blockedYCoords[index]:

                self.directions.remove('S')
                return (direction, False)

            elif direction == 'E' and self.unitInfo[unit]['X'] + 1 == self.blockedXCoords[index] and self.unitInfo[unit]['Y'] == self.blockedYCoords[index]:

                self.directions.remove('E')
                return (direction, False)

            elif direction == 'W' and self.unitInfo[unit]['X'] - 1 == self.blockedXCoords[index] and self.unitInfo[unit]['Y'] == self.blockedYCoords[index]:

                self.directions.remove('W')
                return (direction, False)

        return (direction, True)

    # Returns the direction of a resource relative to a given unit (or null if there are no resources next to the unit)
    def getResourceDirection(self, unit):

        # Checks if any resources are next to the given unit
        for index, coord in enumerate(self.resourceXCoords):

            if self.unitInfo[unit]['X'] == self.resourceXCoords[index] and self.unitInfo[unit]['Y'] - 1 == self.resourceYCoords[index]:

                return ('N', True)

            if self.unitInfo[unit]['X'] == self.resourceXCoords[index] and self.unitInfo[unit]['Y'] + 1 == self.resourceYCoords[index]:

                return ('S', True)

            if self.unitInfo[unit]['X'] + 1 == self.resourceXCoords[index] and self.unitInfo[unit]['Y'] == self.resourceYCoords[index]:

                return ('E', True)

            if self.unitInfo[unit]['X'] - 1 == self.resourceXCoords[index] and self.unitInfo[unit]['Y'] == self.resourceYCoords[index]:

                return ('W', True)

        return ('', False)

# Starts the client listening from an incoming connection from the server
if __name__ == "__main__":

    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 9090
    host = '0.0.0.0'

    server = socketServer.TCPServer((host, port), NetworkHandler)
    print("listening on {}:{}".format(host, port))
    server.serve_forever()
