RIGHT = 1
LEFT = 2
FASTEST = 3
SLOWEST = 4

class Direction:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @staticmethod
    def FastestRotation(current, final):
        difference = current - final

        if (difference == -1 or difference == 3):
            return LEFT
        
        return RIGHT
    
    @staticmethod
    def ReverseDirection(direction):
        revDirection = direction - 2
        if (revDirection < 0):
            revDirection = revDirection + 4

        return revDirection


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

    def Discover(self, position, direction, hasWall):
        self.map[position.y][position.x].UpdateInfo(direction, hasWall)

        nextPos = position.NextPosition(direction)
        if (self.ExceedsMapBounds(nextPos)):
            return

        self.map[nextPos.y][nextPos.x].UpdateInfo(Direction.ReverseDirection(direction), hasWall)

    def ExceedsMapBounds(self, position):
        return position.x < 0 or position.x >= self.mapWidth or position.y < 0 or position.y >= self.mapHeight
        


class TurtleInfo:
    currentDirection = Direction.NORTH
    position = Position(0, 0)
    goal = Position(0, 0)

    def __init__(self, start, goal):
        self.position = start
        self.goal = goal


startPos = Position(4, 7) #X, Y
endPos = Position(3, 0)
turtle = TurtleInfo(startPos, endPos)


currentRoute = [] #List of positions

def GetNextPosition():
    global currentFastestRoute

    return currentFastestRoute.pop(0)

def NextInstruction(currentPos, endPos):
    global turtle
    
    nextDirection = Direction["NORTH"]

    if (currentPos.x < endPos.x):
        nextDirection = Direction["EAST"]

    elif (currentPos.x > endPos.y):
        nextDirection = Direction["WEST"]

    elif (currentPos.y < endPos.y):
        nextDirection = Direction["SOUTH"]

    rightTurns = nextDirection - turtle.currentDirection

