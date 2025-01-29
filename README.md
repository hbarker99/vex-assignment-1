# Glossary
| Term | Definition |
|-|:-|
|Tile|A square in the map, potentially having a wall to it's north, east, south and west|
|Turtle|The robot in the simulation|

# Video
[Link](https://www.youtube.com/watch?v=v5yWDoqdYR8)

# Assumptions
- The turtle knows the map size (could be varied to use in different sized maps, but the turtle doesn't find it out)
- The turtle knows the start location
- The turtle knows the goal location
- There is only one path

# Fastest Route
- Optimised to get to the goal in the shortest amount of time.
- Uses the A* algorithm to plot from the turtles current position to the goal.
- Assumes that there are no walls until proven otherwise
- Aims to find a route with less turns

# Retun Home
- Uses the A* algorithm to plot a point from it's current location to the start.
- By this point it knows a route for definite, and it must take the guranteed route to avoid wasting time searching.

# Discover the map
- Uses djkstras algorithm, but stops searching as soon as it finds an unavailable tile.
- Moves to the closest tile, but optimised for discovery of information so it will discover all information of each tile.

# Sources
[A* Algorithm](https://www.researchgate.net/profile/Xiao-Cui-12/publication/267809499_A-based_Pathfinding_in_Modern_Computer_Games/links/54fd73740cf270426d125adc/A-based-Pathfinding-in-Modern-Computer-Games.pdf)
[A* Algorithm Justification](https://jewlscholar.mtsu.edu/server/api/core/bitstreams/c8efec32-6148-4699-a86d-1f99362a9f36/content)