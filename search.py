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

from game import Directions
import util

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
          state: Search state

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


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    """
    from util import Stack
    stack = Stack()
    visited = set()
    actions = []


    # Init stack and visited set
    stack.push(((problem.getStartState(), problem.getSuccessors(problem.getStartState()))))
    visited.add(problem.getStartState())

    # Start DFS
    while not stack.isEmpty():
        cur_state, neighbor = stack.list[-1]
        # Avoid repeat visitting same node
        valid_neighbor = filter(lambda x: x[0] not in visited, neighbor)
        for nxt in valid_neighbor:
            # Check goal, if next node is goal, do not need to visit it
            if problem.isGoalState(nxt[0]):
                actions.append(nxt[1])
                return actions
            stack.push((nxt[0], problem.getSuccessors(nxt[0])))
            actions.append(nxt[1])
            visited.add((nxt[0]))
            break
        # If no more valid node to be visited, should pop that node from stack
        if len(valid_neighbor) == 0:
            stack.pop()
            actions.pop()
    # If no valid path can be found, return empty path
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    from util import Queue
    queue = Queue()
    visited = set()

    startState = problem.getStartState()

    # Init queue and visited set
    queue.push((startState, []))
    visited.add(startState)

    # Start BFS
    while not queue.isEmpty():
        cur_state, path = queue.pop()
        if problem.isGoalState(cur_state):
            return path
        # Avoid repeat visitting same node
        valid_neighbor = filter(lambda x: x[0] not in visited, problem.getSuccessors(cur_state))
        for nxt in valid_neighbor:
            queue.push((nxt[0], path + [nxt[1]]))
            visited.add(nxt[0])
    # If no valid path can be found, return empty path
    return []


def aStarSearch(problem, heuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    from util import PriorityQueue
    pq = PriorityQueue()
    res = dict()
    visited = set()

    # Init queue and visited set
    pq.push(problem.getStartState(), heuristic(problem.getStartState(), problem))
    res[problem.getStartState()] = []

    # Start A*
    while not pq.isEmpty():
        cur_state = pq.pop()
        path = res[cur_state]
        visited.add(cur_state)
        if problem.isGoalState(cur_state):
            return path

        valid_neighbor = filter(lambda x: x[0] not in visited, problem.getSuccessors(cur_state))
        for nxt in valid_neighbor:
            npath = path + [nxt[1]]
            np = problem.getCostOfActions(npath) + heuristic(nxt[0], problem)
            # Update both path and priority queue
            if nxt[0] not in res or (nxt[0] in res and problem.getCostOfActions(res[nxt[0]]) > np):
                res[nxt[0]] = npath
            pq.update(nxt[0], np)
    # If no valid path can be found, return empty path
    return []



def biDirectionalSearchMM0(problem):
    """
    Bi directional search - MM0.
    Two simple BFS in both direction.
    """
    def __reversedPath(p):
        """
        Given a action list, return the reversed version of it.
        """
        return [Directions.REVERSE[x] for x in p][::-1]

    from util import Queue
    # Init two ques and visited sets.
    que1, que2 = Queue(), Queue()
    visited1, visited2 = dict(), dict()

    que1.push((problem.getStartState(), [], 0))
    que2.push((problem.goal, [], 0))
    visited1[problem.getStartState()] = ''
    visited2[problem.goal] = ''
    expanding_level1, expanding_level2 = 0, 0

    # Two simple BFS in each while round
    while True:
        # First BFS, from start to goal
        # Will expand one level of nodes
        if que1.isEmpty():
            return []
        while (not que1.isEmpty()) and que1.list[0][2] == expanding_level1:
            # Get current state
            cur_state, path, level = que1.pop()

            # Check result
            if problem.isGoalStateBi(cur_state, visited2):
                return path + __reversedPath(visited2[cur_state])

            # Expand valid neighbors
            valid_neighbor = filter(lambda x: x[0] not in visited1, problem.getSuccessors(cur_state))
            for nxt in valid_neighbor:
                que1.push((nxt[0], path+[nxt[1]], level+1))
                visited1[nxt[0]] = path+[nxt[1]]
        expanding_level1 += 1

        # Second BFS, from foal to start
        # Will expand one level of nodes
        if que2.isEmpty():
            return []
        while (not que2.isEmpty()) and que2.list[0][2] == expanding_level2:
            # Get current state
            cur_state, path, level = que2.pop()

            # Check result
            if problem.isGoalStateBi(cur_state, visited1):
                return __reversedPath(visited1[cur_state]) + path

            # Expand valid neighbors
            valid_neighbor = filter(lambda x: x[0] not in visited2, problem.getSuccessors(cur_state))
            for nxt in valid_neighbor:
                que2.push((nxt[0], path+[nxt[1]], level+1))
                visited2[nxt[0]] = path+[nxt[1]]
        expanding_level2 += 1
    return []


def biDirectionalSearchMM(problem, heuristic):
    """
    Bi directional search - MM.
    Two Astar search in two directions.
    """
    def __reversedPath(p):
        """
        Given a action list, return the reversed version of it.
        """
        return [Directions.REVERSE[x] for x in p][::-1]

    from util import PriorityQueue
    # Init two priority queues and visited dicts
    pq1, pq2 = PriorityQueue(), PriorityQueue()
    visited1, visited2 = dict(), dict()

    pq1.push((problem.getStartState(), [], 0), heuristic(problem.getStartState(), problem, 'goal'))
    pq2.push((problem.goal, [], 0), heuristic(problem.goal, problem, 'start'))
    visited1[problem.getStartState()] = []
    visited2[problem.goal] = []

    # Run two Astar search in each while round
    while True:
        # First Astar search, from start to goal
        # Only expand one node
        if pq1.isEmpty():
            return []
        cur_state, path, level = pq1.pop()

        if problem.isGoalStateBi(cur_state, visited2):
            return path + __reversedPath(visited2[cur_state])

        valid_neighbor = filter(lambda x: x[0] not in visited1, problem.getSuccessors(cur_state))
        for nxt in valid_neighbor:
            np = heuristic(nxt[0], problem, 'goal') + problem.getCostOfActions(path+[nxt[1]])
            pq1.push((nxt[0], path+[nxt[1]], level+1), np)
            visited1[nxt[0]] = path+[nxt[1]]

        # Second Astar search, from goal to start
        # Only expand one node
        if pq2.isEmpty():
            return []

        cur_state, path, level = pq2.pop()

        if problem.isGoalStateBi(cur_state, visited1):
            return __reversedPath(visited1[cur_state]) + path

        valid_neighbor = filter(lambda x: x[0] not in visited2, problem.getSuccessors(cur_state))
        for nxt in valid_neighbor:
            np = heuristic(nxt[0], problem, 'start') + problem.getCostOfActions(path+[nxt[1]])
            pq2.push((nxt[0], path+[nxt[1]], level+1), np)
            visited2[nxt[0]] = path+[nxt[1]]

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
bd0 = biDirectionalSearchMM0
bd = biDirectionalSearchMM


