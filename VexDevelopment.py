#endregion VEXcode Generated Robot Configuration
import random

RIGHT = 1
LEFT = 2

class DiscoveryInstruction:
    FASTEST = 1
    SLOWEST = 2
    CHECKRIGHT = 3
    CHECKLEFT = 4

class DirectionInstruction:
    RotationDirection = LEFT
    Rotations = 0

    def __init__(self, direction, rotations):
        self.RotationDirection = direction
        self.Rotations = rotations

class Direction:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @staticmethod
    def FastestRotation(current, final):
        difference = current - final

        if (difference == 0):
            return DirectionInstruction(RIGHT, 0)

        if (difference == -1 or difference == 3):
            return DirectionInstruction(RIGHT, 1)
        
        if (difference == 2 or difference == -2):
            return DirectionInstruction(RIGHT, 2)
        
        return DirectionInstruction(LEFT, 1)
    
    @staticmethod
    def ReverseDirection(direction):
        revDirection = direction - 2
        if (revDirection < 0):
            revDirection = revDirection + 4

        return revDirection
    
    @staticmethod
    def RequiredDirection(startPos, endPos):
        required = Direction.NORTH

        if (startPos.x < endPos.x):
            required = Direction.EAST

        elif (startPos.x > endPos.x):
            required = Direction.WEST

        elif (startPos.y < endPos.y):
            required = Direction.SOUTH

        return required
    
    def RightFrom(direction):
        return direction + 1 if direction != Direction.WEST else Direction.NORTH
    
    def LeftFrom(direction):
        return direction - 1 if direction != Direction.NORTH else Direction.WEST
        


class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def NextPosition(self, direction):

        vertModifier = 0
        horizModifier = 0

        if (direction == Direction.NORTH):
            vertModifier = -1
            
        elif (direction == Direction.EAST):
            horizModifier = 1
            
        if (direction == Direction.SOUTH):
            vertModifier = 1

        if (direction == Direction.WEST):
            horizModifier = -1

        return Point(self.x + horizModifier, self.y + vertModifier)

class Tile:
    Pos = Point(0, 0)
    AvailableDirections = [True, True, True, True] #North, East, South, West
    CheckedDirections = [False, False, False, False] 

    def __init__(self, x, y):
        self.Pos = Point(x, y)
        self.AvailableDirections = [True, True, True, True] #North, East, South, West
        self.CheckedDirections = [False, False, False, False] 

    def IsDiscovered(self):
        return all(self.CheckedDirections)
    
    def GetDiscoveryInstruction(self, currentDirection, finalDirection):
        #When entering a tile we know whether it has a wall behind it, and if it has a tile in front of it. So can work with that assumption.
        undiscoveredDirections = self.CheckedDirections.count(False)

        if (undiscoveredDirections == 0):
            return DiscoveryInstruction.FASTEST
        
        if (currentDirection == finalDirection):
            #If there is 1 undiscovered and we want to end up facing the same direction, we just want to check that direction and then point back again
            #This is 2 rotations, as opposed to 4 if we just went the slowest way.
            if (undiscoveredDirections == 1):
                rightDirection = Direction.RightFrom(currentDirection)
                return DiscoveryInstruction.CHECKRIGHT if self.CheckedDirections[rightDirection] else DiscoveryInstruction.CHECKLEFT

            #If there are 2 it doesn't matter so may aswell go in the same direction 4 times
            else:
                return DiscoveryInstruction.SLOWEST
        
        #If we have already checked the end direction we know we need to go around backwards as unchecked is opposite
        if (self.CheckedDirections[finalDirection]):
            return DiscoveryInstruction.SLOWEST
        
        else:
            return DiscoveryInstruction.FASTEST if undiscoveredDirections == 1 else DiscoveryInstruction.SLOWEST
    
    def UpdateInfo(self, direction, hasWall):
        self.AvailableDirections[direction] = not hasWall
        self.CheckedDirections[direction] = True
    
class Board:
    Map = []
    MapWidth = 8
    MapHeight = 8

    def __init__(self):
        self.Map = []
        self.MapWidth = 8
        self.MapHeight = 8

        for y in range(self.MapHeight):
            self.Map.append([])
            for x in range(self.MapWidth):
                self.Map[y].append(Tile(x, y))

    def Discover(self, startPos, direction, closestWall):

        horizChange = 0
        vertChange = 0

        if (direction == Direction.NORTH or direction == Direction.SOUTH):
            vertChange = direction - 1

        else:
            horizChange = (- direction) + 2

        for i in range(closestWall + 1):
            self.Map[startPos.y + (vertChange * i)][startPos.x + (horizChange * i)].UpdateInfo(direction, i == closestWall)

        for i in range(closestWall + 1, 0, -1):
            if (self.ExceedsMapBounds(Point(startPos.x + (horizChange * i), startPos.y + (vertChange * i)))):
                continue

            self.Map[startPos.y + (vertChange * i)][startPos.x + (horizChange * i)].UpdateInfo(Direction.ReverseDirection(direction), i == closestWall + 1)


    def ExceedsMapBounds(self, currentPos):
        return currentPos.x < 0 or currentPos.x >= self.MapWidth or currentPos.y < 0 or currentPos.y >= self.MapHeight
    
    def GetTile(self, pos):
        if (self.ExceedsMapBounds(pos)):
            return Tile(0, 0)
        
        return self.Map[pos.y][pos.x]
    
    def GetCharacter(self, currentTile, direction):

        isChecked = currentTile.CheckedDirections[direction]
        isAvailable = currentTile.AvailableDirections[direction]

        if (not isChecked):
            return '?'
        
        return 'O' if isAvailable else '#'


class AStar:
    Route = []
    Goal = Point(0, 0)

    class Node:
        def __init__(self, x, y, totalCost, currentCost, node):
            self.x = x
            self.y = y
            self.TotalCost = totalCost
            self.CurrentCost = currentCost
            self.PreviousNode = node

    def __init__(self, goal):
        self.Goal = goal

    def Heuristic(self, point):
        return abs(self.Goal.x - point.x) + abs(self.Goal.y - point.y)
    
    def GetRoute(self, finalNode):
        route = []
        checkingNode = finalNode

        while (checkingNode.PreviousNode != None):
            route.append(Point(checkingNode.x, checkingNode.y))
            checkingNode = checkingNode.PreviousNode

        route.reverse()
        return route

    def CalculateRoute(self, current, theMap):
        self.Current = current
        self.Route = []

        routeFound = False
        checkOrder = [self.Node(current.x, current.y, self.Heuristic(current), 0, None)]

        while (not routeFound):
            currentNode = checkOrder.pop(0)
            nodeRoute = [(x.x, x.y) for x in self.GetRoute(currentNode)]
            availableDirections = theMap.Map[currentNode.y][currentNode.x].AvailableDirections

            for i in range(len(availableDirections)):
                if (not availableDirections[i]):
                    continue

                
                checkingPoint = Point(currentNode.x, currentNode.y).NextPosition(i)
                
                if (currentNode.PreviousNode != None and (checkingPoint.x, checkingPoint.y) in nodeRoute):
                    continue

                stepCost = currentNode.CurrentCost + 1
                totalCost = self.Heuristic(checkingPoint) + stepCost
                finalNode = self.Node(checkingPoint.x, checkingPoint.y, totalCost, stepCost, currentNode)

                if ((finalNode.x, finalNode.y) == (self.Goal.x, self.Goal.y)):
                    routeFound = True
                    self.Route = self.GetRoute(finalNode)
                    break

                if (len(checkOrder) == 0):
                    checkOrder.append(finalNode)

                inserted = False
                removing = False

                removeAt = 0
                insertAt = 0

                for node in range(len(checkOrder)):
                    if (not inserted and finalNode.TotalCost <= checkOrder[node].TotalCost):
                        insertAt = node
                        inserted = True

                    if ((finalNode.x, finalNode.y) == (checkOrder[node].x, checkOrder[node].y)):
                        if (inserted):
                            removing = True
                            removeAt = node
                            break
                        else:
                            break

                if (inserted):
                    checkOrder.insert(insertAt, finalNode)

                if (removing):
                    checkOrder.pop(removeAt)

                elif(not removing and not inserted):
                    checkOrder.append(finalNode)

        if (not routeFound):
            #brain.print("No route to goal was found.")
            pass
        
        return self.Route
                               
        


class TurtleInfo:
    CurrentDirection = Direction.NORTH
    Pos = Point(0, 0)
    Goal = Point(0, 0)


    def __init__(self, direction, start, goal):
        self.Pos = start
        self.Goal = goal
        self.CurrentDirection = direction

    def Turn(self, direction):

        #drivetrain.turn_for(direction, 90, DEGREES)
        if (direction == RIGHT):
            self.CurrentDirection = Direction.RightFrom(self.CurrentDirection)

        else:
            self.CurrentDirection = Direction.LeftFrom(self.CurrentDirection)

    def Forward(self):
        #Drive Forward
        #drivetrain.drive_for(FORWARD, 250, MM)

        self.Pos = self.Pos.NextPosition(self.CurrentDirection)

    def ClosestWall(self):
        distance = 63#front_distance.get_distance(MM)
        tiles = int(round((distance - 62) / 10) / 25)
        return tiles


def NextInstruction(currentPos, nextPos):
    global board, turtle

    nextDirection = Direction.RequiredDirection(currentPos, nextPos)
    currentTile = board.GetTile(currentPos)

    instruction = Direction.FastestRotation(turtle.CurrentDirection, nextDirection)
    discoveryInstruction = currentTile.GetDiscoveryInstruction(turtle.CurrentDirection, nextDirection)


    if (discoveryInstruction != DiscoveryInstruction.FASTEST):
        if (discoveryInstruction == DiscoveryInstruction.CHECKLEFT):
            Turn(LEFT)
            Turn(RIGHT)
        
        elif (discoveryInstruction == DiscoveryInstruction.CHECKRIGHT):
            Turn(RIGHT)
            Turn(LEFT)

        else:
            rotations = 4 - instruction.Rotations
            instruction.Rotations = rotations
            instruction.RotationDirection = RIGHT if instruction.RotationDirection == LEFT else LEFT

    for _ in range(instruction.Rotations):
        Turn(instruction.RotationDirection)

    if (turtle.ClosestWall() == 0):
        return False
    
    Forward()
    return True

def Forward():
    global board, turtle

    turtle.Forward()
    board.Discover(turtle.Pos, turtle.CurrentDirection, turtle.ClosestWall())


def Turn(direction):
    global board, turtle

    turtle.Turn(direction)
    board.Discover(turtle.Pos, turtle.CurrentDirection, turtle.ClosestWall())


startPos = Point(4, 7) #X, Y
endPos = Point(3, 0)
board = Board()

turtle = TurtleInfo(Direction.NORTH, startPos, endPos)


def Main():
    global board, turtle
    calulator = AStar(turtle.Goal)
    route = calulator.CalculateRoute(turtle.Pos, board)

    while ((turtle.Pos.x, turtle.Pos.y) != (turtle.Goal.x, turtle.Goal.y)):
        nextPos = route.pop(0)

        if (not NextInstruction(turtle.Pos, nextPos)):
            route = calulator.CalculateRoute(turtle.Pos, board)
