# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state (only the coordiantes!)

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem:SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    
    """
    Resources to understand the reconstruction of the path
    https://stackoverflow.com/questions/12864004/tracing-and-returning-a-path-in-depth-first-search
    """
    fringe = util.Stack() #the frontier
    explored = set() #the already explored nodes
    parent = dict() #will remember the parent of every explored node 
    
    
    #init setup
    initState = (problem.getStartState(),(),())
    fringe.push(initState) #the starting state as a tupel
    
    while not fringe.isEmpty():
        # get the first element from the fringe
        stateToExplore=fringe.pop()
        
        # test if the current node is a goal node
        if problem.isGoalState(stateToExplore[0]):
            path = []
            while (stateToExplore != initState):
                #appends the direction of the state
                path.append(stateToExplore[1])
                #find the parent of the current state
                stateToExplore = parent[stateToExplore] 
            path.reverse()
            return path

        #only explore new nodes
        if stateToExplore[0] not in explored:
            #add the state to the explored states
            explored.add(stateToExplore[0])
            
            # explores all the successor nodes
            for successor in problem.getSuccessors(stateToExplore[0]):
                # ignore the explored already coordinates
                if successor[0] in explored: 
                    continue
                #in order to reconstruct the path we need to save the parent of each explored node
                parent[successor] = stateToExplore
                # successor is not only a position but a tupel (coordiantes, direction, cost)
                fringe.push(successor)

    #no path exists
    return []



def breadthFirstSearch(problem:SearchProblem):
    """Search the shallowest nodes in the search tree first."""

    fringe = util.Queue() #the frontier
    explored = set() #the already explored nodes
    parent = dict() #will remember the parent of every explored node
    
    #init setup
    initState = (problem.getStartState(),(),()) #coordinates, direction, cost
    fringe.push(initState) #the starting state as a tupel
    
    while not fringe.isEmpty():
        #get the first node from the fringe
        stateToExplore=fringe.pop()

        #test if the state to explore is a goal state
        if problem.isGoalState(stateToExplore[0]):
            path = []
            while (stateToExplore != initState):
                #append the direction to head
                path.append(stateToExplore[1])
                #go one tier higher
                stateToExplore = parent[stateToExplore] 
            path.reverse()
            return path

        #only explore new nodes
        if stateToExplore[0] not in explored:
            #mark the current node as already explored 
            explored.add(stateToExplore[0])
            
            #explore the current node
            for successor in problem.getSuccessors(stateToExplore[0]):
                #skip already explored coordinates
                if successor[0] in explored: 
                    continue
                #keep track if the parent nodes
                parent[successor] = stateToExplore
                #add the new nodes to the fringe
                fringe.push(successor)

    #no path exists
    return []
    

def uniformCostSearch(problem:SearchProblem):
    """Search the node of least total cost first."""
    #TODO use update or push?
    
    fringe = util.PriorityQueue() #the frontier
    explored = set() #the coordinates of the already expored nodes
    
    #init setup
    initState = (problem.getStartState(),(),list()) #(coordinates, direction, path)
    fringe.push(initState,0) #the starting state (item,cost)

    while not fringe.isEmpty():
        #get the first node from the fringe
        CooridnatesToExplore, *other, path=fringe.pop() #coodinate, ((direction),(cost)), pathArrayOfDirections
        #test if the state to explore is a goal state
        if problem.isGoalState(CooridnatesToExplore):
            return path
        
        #only explore new nodes
        if CooridnatesToExplore not in explored:
            #mark the current node as already explored 
            explored.add(CooridnatesToExplore)
            
            #explore the current node
            for successor in problem.getSuccessors(CooridnatesToExplore):
                #skip already explored coordinates
                if successor[0] in explored: 
                    continue
                #update the path
                newPath = path + [successor[1]]
                #add new nodes to the fringe
                fringe.update(item=(*successor,newPath),priority=problem.getCostOfActions(newPath))

    #no path exists
    return []



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem:SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    #TODO how to treat different heuristics? 
    
    fringe = util.PriorityQueue() #the frontier
    explored = set() #the already explored nodes
    parent = dict() #will remember the parent of every explored node
    
    #init setup
    initState = (problem.getStartState(),(),())
    fringe.push(initState,heuristic(initState[0],problem)) #the starting state as a tupel
    
    while not fringe.isEmpty():
        #get the first node from the fringe
        stateToExplore=fringe.pop()
        
        #test if the state to explore is a goal state
        if problem.isGoalState(stateToExplore[0]):
            path = []
            while (stateToExplore != initState):
                #append the direction to head
                path.append(stateToExplore[1])
                #go one tier higher
                stateToExplore = parent[stateToExplore] 
            path.reverse()
            return path

        #only explore new nodes
        if stateToExplore not in explored:
            #mark the current node as already explored 
            explored.add(stateToExplore)
            
            #explore the current node
            for successor in problem.getSuccessors(stateToExplore[0]):
                #skip already explored coordinates
                if successor[0] in [successor[0] for successor in explored]: 
                    continue
                #keep track if the parent nodes
                parent[successor] = stateToExplore
                #add new nodes to the fringe
                fringe.update(item=successor,priority=heuristic(successor[0],problem))

    #no path exists
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
