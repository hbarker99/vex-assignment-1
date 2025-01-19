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
            return Direction(RIGHT, 0)

        if (difference == -1 or difference == 3):
            return DirectionInstruction(LEFT, 1)
        
        if (difference == 2 or difference == -2):
            return DirectionInstruction(RIGHT, 2)
        
        return DirectionInstruction(RIGHT, 1)
    
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

        match (direction):
            case Direction.NORTH:
                vertModifier = -1
            
            case Direction.EAST:
                horizModifier = 1
            
            case Direction.SOUTH:
                vertModifier = 1

            case Direction.WEST:
                horizModifier = -1

        return Position(self.x + vertModifier, self.y + horizModifier)

class Tile:
    Pos = Position()
    AvailableDirections = (True, True, True, True) #North, East, South, West
    CheckedDirections = (False, False, False, False) 

    def __init__(self, x, y):
        self.Pos = Position(x, y)

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
        self.AvailableDirections[direction] = hasWall
        self.CheckedDirections[direction] = True
    
class Board:
    map = []
    mapWidth = 8
    mapHeight = 8

    def __init__(self):
        for y in range(self.mapHeight):
            self.map.append([])
            for x in range(self.mapWidth):
                self.map[y].append(Tile(x, y))

    def Discover(self, position, direction, closestWall):

        horizChange = 0
        vertChange = 0

        if (direction == Direction.NORTH or direction == Direction.SOUTH):
            vertChange = direction - 1

        else:
            horizChange = (- direction) + 2

        for i in range(closestWall + 1):
            self.map[position.y + vertChange * i][position.x + horizChange * i].UpdateInfo(direction, i == closestWall)

        for i in range(closestWall + 1, 0, -1):
            if (self.ExceedsMapBounds(Position(position.x + horizChange, position.y + vertChange))):
                continue

            self.map[position.y + vertChange * i][position.x + horizChange * i].UpdateInfo(Direction.ReverseDirection(direction), i == closestWall + 1)


    def ExceedsMapBounds(self, position):
        return position.x < 0 or position.x >= self.mapWidth or position.y < 0 or position.y >= self.mapHeight
    
    def GetTile(self, pos):
        return self.map[pos.y][pos.x]
        


class TurtleInfo:
    CurrentDirection = Direction.NORTH
    Pos = Position(0, 0)
    Goal = Position(0, 0)

    def __init__(self, direction, start, goal):
        self.Pos = start
        self.Goal = goal
        self.CurrentDirection = direction

    def Turn(self, direction):
        #Turn 90 degrees in direction

        if (direction == RIGHT):
            self.CurrentDirection = Direction.RightFrom(self.CurrentDirection)

        else:
            self.CurrentDirection = Direction.LeftFrom(self.CurrentDirection)

    def Forward(self):
        #Drive Forward

        self.Pos = self.Pos.NextPosition(self.CurrentDirection)

    def ClosestWall(self):
        distance = 62
        tiles = round((62 - distance) / 10) / 25
        return tiles


def NextInstruction(currentPos, nextPos):
    global board, turtle

    nextDirection = Direction.RequiredDirection(currentPos, nextPos)
    currentTile = board.GetTile(currentPos)

    instruction = Direction.FastestRotation(turtle.CurrentDirection, nextDirection)
    discoveryInstruction = currentTile.GetDiscoveryInstruction(turtle.CurrentDirection, nextDirection)
    
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


def CalculateRoute():
    pass


startPos = Position(4, 7) #X, Y
endPos = Position(3, 0)
turtle = TurtleInfo(Direction.NORTH, startPos, endPos)
board = Board()


def Main():
    global board, turtle
    
    currentRoute = CalculateRoute()
    while (turtle.Pos != turtle.Goal):

        movingTo = currentRoute.pop(0)
        
        if (not NextInstruction(turtle.Pos, movingTo)):
            currentRoute = CalculateRoute()
