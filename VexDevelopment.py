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

        elif (startPos.x > endPos.y):
            required = Direction.WEST

        elif (startPos.y < endPos.y):
            required = Direction.SOUTH

        return required
    
    def RightFrom(direction):
        return direction + 1 if direction != Direction.WEST else Direction.NORTH
    
    def LeftFrom(direction):
        return direction - 1 if direction != Direction.NORTH else Direction.WEST
        


class Position:
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

        return Position(self.x + horizModifier, self.y + vertModifier)

class Tile:
    Pos = Position(0, 0)
    AvailableDirections = [True, True, True, True] #North, East, South, West
    CheckedDirections = [False, False, False, False] 

    def __init__(self, x, y):
        self.Pos = Position(x, y)
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

    def Discover(self, position, direction, closestWall):

        horizChange = 0
        vertChange = 0

        if (direction == Direction.NORTH or direction == Direction.SOUTH):
            vertChange = direction - 1

        else:
            horizChange = (- direction) + 2

        for i in range(closestWall + 1):
            self.Map[position.y + (vertChange * i)][position.x + (horizChange * i)].UpdateInfo(direction, i == closestWall)

        for i in range(closestWall + 1, 0, -1):
            if (self.ExceedsMapBounds(Position(position.x + (horizChange * i), position.y + (vertChange * i)))):
                continue

            self.Map[position.y + (vertChange * i)][position.x + (horizChange * i)].UpdateInfo(Direction.ReverseDirection(direction), i == closestWall + 1)


    def ExceedsMapBounds(self, position):
        return position.x < 0 or position.x >= self.MapWidth or position.y < 0 or position.y >= self.MapHeight
    
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

    
    def PrintKnownBoard(self, turtle):
        for y in range(self.MapHeight * 3):
            print()
            for x in range(self.MapWidth * 3):
                xPoint = int(x / 3)
                yPoint = int(y / 3)

                currentTile = self.Map[yPoint][xPoint]

                yRem = y % 3
                xRem = x % 3

                character = ''

                if (yRem != 1 and xRem != 1):
                    character = '#'

                elif (yRem == 1 and xRem == 1):
                    if (turtle.Pos.x == xPoint and turtle.Pos.y == yPoint):
                        character = 'T'
                    elif (turtle.Goal.x == xPoint and turtle.Goal.y == yPoint):
                        character = 'G'
                    else:
                        character = 'O'

                elif (yRem == 0 and xRem == 1):
                    character = self.GetCharacter(currentTile, Direction.NORTH)

                elif (yRem == 1 and xRem == 0):
                    character = self.GetCharacter(currentTile, Direction.WEST)

                elif (yRem == 1 and xRem == 2):
                    character = self.GetCharacter(currentTile, Direction.EAST)

                elif (yRem == 2 and xRem == 1):
                    character = self.GetCharacter(currentTile, Direction.SOUTH)

                print(character, end='')

class AStar:
    Map = []
    Route = []
    Goal = Position(0, 0)
    Current = Position(0, 0)

    class Node:
        def __init__(self, x, y, distance, currentCost, node):
            self.x = x
            self.y = y
            self.Distance = distance
            self.CurrentCost = currentCost
            self.PreviousNode = node

    def __init__(self, map, current, goal):
        self.Map = map
        self.Current = current
        self.Goal = goal

    def Heuristic(self, point):
        return abs(self.Goal.x - point.x) + abs(self.Goal.y - point.y)

    def CalculateRoute(self, current, theMap):
        self.Current = current
        self.Route = []
        self.Map = theMap

        routeFound = False
        checkOrder = [self.Node(current.x, current.y, self.Heuristic(current), 0, None)]

        while (not routeFound):
            currentNode = checkOrder.pop(0)
            availableDirections = self.Map[currentNode.y][currentNode.x].AvailableDirections

            for i in range(len(availableDirections)):
                if (not availableDirections[i]):
                    continue

                checkingPoint = Position(currentNode.x, currentNode.y).NextPosition(i)
                stepCost = currentNode.CurrentCost + 1
                distance = self.Heuristic(checkingPoint) + stepCost
                finalNode = self.Node(checkingPoint.x, checkingPoint.y, distance, stepCost, currentNode)

                if (len(checkOrder) == 0):
                    checkOrder.append(finalNode)

                for node in range(len(checkOrder)):
                    if (finalNode.Distance < checkOrder[node].Distance):
                        checkOrder.insert(node, finalNode)








class TurtleInfo:
    CurrentDirection = Direction.NORTH
    Pos = Position(0, 0)
    Goal = Position(0, 0)
    ActualMap = Board()


    def __init__(self, direction, start, goal, actualMap):
        self.Pos = start
        self.Goal = goal
        self.CurrentDirection = direction
        self.ActualMap = actualMap

    def Turn(self, direction):
        if (direction == RIGHT):
            self.CurrentDirection = Direction.RightFrom(self.CurrentDirection)

        else:
            self.CurrentDirection = Direction.LeftFrom(self.CurrentDirection)

    def Forward(self):
        #Drive Forward

        self.Pos = self.Pos.NextPosition(self.CurrentDirection)

    def GetDistance(self):
        distance = 62
        position = Position(self.Pos.x, self.Pos.y)

        while (self.ActualMap.GetTile(position).AvailableDirections[self.CurrentDirection]):
            distance = distance + 250
            position = position.NextPosition(self.CurrentDirection)

        return distance

    def ClosestWall(self):
        distance = self.GetDistance()
        tiles = int(round((distance - 62) / 10) / 25)
        return tiles


def NextInstruction(currentPos, nextPos):
    global board, turtle

    nextDirection = Direction.RequiredDirection(currentPos, nextPos)
    currentTile = board.GetTile(currentPos)

    instruction = Direction.FastestRotation(turtle.CurrentDirection, nextDirection)
    discoveryInstruction = currentTile.GetDiscoveryInstruction(turtle.CurrentDirection, nextDirection)

    print("Next Direction: " + str(nextDirection))
    print("Current Direction: " + str(turtle.CurrentDirection))
    print("Instruction Direction is Right: " + str(instruction.RotationDirection == RIGHT))
    print("Instruction Rotations: " + str(instruction.Rotations))

    if (discoveryInstruction != DiscoveryInstruction.FASTEST):
        #Can be optimised - doesn't need to turn 90 degrees
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

    #If we're facing the suggested direction and there's a wall we need a new route
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


def CalculateRoute(turtle):
    start = turtle.Pos
    goal = turtle.Goal

    checkNext = []




def RandomiseMap(turtle):
    global actualMap

    def IsOnGuranteedPath(path, pos):
        for pathPos in path:
            if pos.x == pathPos.x and pos.y == pathPos.y:
                return True

    guranteedPath = [
        Position(4, 7),
        Position(5, 7),
        Position(6, 7),
        Position(6, 6),
        Position(6, 5),
        Position(5, 5),
        Position(5, 4),
        Position(5, 3),
        Position(6, 3),
        Position(7, 3),
        Position(7, 2),
        Position(7, 1),
        Position(6, 1),
        Position(5, 1),
        Position(4, 1),
        Position(3, 1),
        Position(3, 0)
    ]
    
    for y in range(actualMap.MapHeight):
        for x in range(actualMap.MapWidth):            
            actualMap.Map[y][x].CheckedDirections = [True, True, True, True]

    for y in range(actualMap.MapHeight):
        for x in range(actualMap.MapWidth):
            if ((x + y) % 2 == 0):
                continue

            pos = Position(x, y)



            isNorth = random.choice([True, False])
            isEast = random.choice([True, False])
            isSouth = random.choice([True, False])
            isWest = random.choice([True, False])

            if (x == turtle.Pos.x and y == turtle.Pos.y or IsOnGuranteedPath(guranteedPath, Position(x, y))):
                isNorth = True
                isEast = True
                isSouth = True
                isWest = True

            n = pos.NextPosition(Direction.NORTH)
            e = pos.NextPosition(Direction.EAST)
            s = pos.NextPosition(Direction.SOUTH)
            w = pos.NextPosition(Direction.WEST)

            if (n.y >= 0):
                northTile = actualMap.Map[n.y][n.x]
                northTile.AvailableDirections[Direction.ReverseDirection(Direction.NORTH)] = isNorth

            if (e.x < actualMap.MapWidth):
                eastTile = actualMap.Map[e.y][e.x]
                eastTile.AvailableDirections[Direction.ReverseDirection(Direction.EAST)] = isEast

            if (s.y < actualMap.MapHeight):
                southTile = actualMap.Map[s.y][s.x]
                southTile.AvailableDirections[Direction.ReverseDirection(Direction.SOUTH)] = isSouth


            if (w.x >= 0):
                westTile = actualMap.Map[w.y][w.x]
                westTile.AvailableDirections[Direction.ReverseDirection(Direction.WEST)] = isWest




            currentTile = actualMap.Map[pos.y][pos.x]

            currentTile.AvailableDirections[Direction.NORTH] = isNorth
            currentTile.AvailableDirections[Direction.EAST] = isEast
            currentTile.AvailableDirections[Direction.SOUTH] = isSouth
            currentTile.AvailableDirections[Direction.WEST] = isWest

    for i in range(actualMap.MapWidth):
        actualMap.Map[0][i].AvailableDirections[Direction.NORTH] = False
        actualMap.Map[actualMap.MapHeight - 1][i].AvailableDirections[Direction.SOUTH] = False
        actualMap.Map[i][0].AvailableDirections[Direction.WEST] = False
        actualMap.Map[i][actualMap.MapWidth - 1].AvailableDirections[Direction.EAST] = False


startPos = Position(4, 7) #X, Y
endPos = Position(3, 0)
board = Board()

actualMap = Board()
turtle = TurtleInfo(Direction.NORTH, startPos, endPos, actualMap)
RandomiseMap(turtle)



actualMap.PrintKnownBoard(turtle)
print()
board.PrintKnownBoard(turtle)
print("\n")

def Quick(pos):
    NextInstruction(turtle.Pos, pos)
    board.PrintKnownBoard(turtle)
    print()


def Main():
    global board, turtle
    
    Quick(Position(5, 7))
    Quick(Position(6, 7))
    Quick(Position(6, 6))
    Quick(Position(6, 5))
    Quick(Position(5, 5))
    print("Fin")


Main()
