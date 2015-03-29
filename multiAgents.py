# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        print "Current Pos: "
        print gameState.getPacmanPosition()
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        print "BEST"
        print bestScore
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        curFood = currentGameState.getFood()
        "*** YOUR CODE HERE ***"
        
        ''' SHould Add The feature to consider the newScaredTimes
        '''
        #print "This is new position: " 
        #print newPos
        score = 0
        distanceToGhosts = 0
        distanceToFood = []
        control = 1
        for ghost in newGhostStates: #To get more far with the ghosts
        	distanceToGhosts += util.manhattanDistance(newPos,ghost.getPosition())
        
        for food in newFood.asList():
        	distanceToFood.append(util.manhattanDistance(newPos,food))
        if newPos in curFood.asList():
        	print "YES!"
      		score+=200
      		control = 0
        #print "distanceToGhosts: "
        #print distanceToGhosts
        #print "distanceToFood: "
        if currentGameState.getPacmanPosition()==newPos:#punish for stay
        	score = score -20
        if distanceToFood == []:
        	score+=100+5*distanceToGhosts
        else:
        	#print min(distanceToFood)
        	score += 100+5*distanceToGhosts-15*min(distanceToFood)*control
        if distanceToGhosts<=3:#to get away from the ghost
        	score -=400
        #print "current score:"
        print score
        return score
        #return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    
    def maxValue(self,state,depth):
	if state.isWin() or state.isLose():
        # if depth == self.depth:
            #print self.evaluationFunction(state)
	    return self.evaluationFunction(state)
	result = -999999
	for action in state.getLegalActions(0):
	    result = max(result,self.minValue(state.generateSuccessor(0, action),depth,1))
	#print result
	return result

    def minValue(self,state,depth,level):
        if state.isWin() or state.isLose():
        #if depth == self.depth and level==state.getNumAgents()-1:
            #print self.evaluationFunction(state)
            return self.evaluationFunction(state)
        result = 999999
        if level==state.getNumAgents()-1:
	    for action in state.getLegalActions(level):
                if depth ==self.depth:
                    result = min(result,self.evaluationFunction(state.generateSuccessor(level, action)))
		else:
                    result = min(result,self.maxValue(state.generateSuccessor(level, action),depth+1))
        else:
	    for action in state.getLegalActions(level):
		result = min(result,self.minValue(state.generateSuccessor(level, action),depth,level+1))
	#print result
	return result

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        resultAction= []
        resultValue = []
        #print gameState.getNumAgents()
        #print self.depth
        for action in gameState.getLegalActions(0):
	    resultValue.append(self.minValue(gameState.generateSuccessor(0, action),1,1))
	    resultAction.append(action)
        maxIndex = max(resultValue)
        for i in range(len(resultValue)):
            if resultValue[i]==maxIndex:
                break
        
        #print resultValue
        #print i
        return resultAction[i]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def maxValue(self,state,depth,a,b):
	if state.isWin() or state.isLose():
	    return self.evaluationFunction(state)
	result = -999999
	for action in state.getLegalActions(0):
	    result = max(result,self.minValue(state.generateSuccessor(0, action),depth,1,a,b))
	    if result>b:
                #print "YES"
                return result
            a = max(a,result)
            #print (a,b)
	#print result
	return result

    def minValue(self,state,depth,level,a,b):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        result = 999999
        if level==state.getNumAgents()-1:
	    for action in state.getLegalActions(level):
                if depth ==self.depth:
                    result = min(result,self.evaluationFunction(state.generateSuccessor(level, action)))
		else:
                    temp = self.maxValue(state.generateSuccessor(level, action),depth+1,a,b)
                    result = min(result,temp)
                if result<a:
                    return result
                b=min(b,result)
                #print (a,b)
        else:
	    for action in state.getLegalActions(level):
                temp = self.minValue(state.generateSuccessor(level, action),depth,level+1,a,b)
		result = min(result,temp)
		if result<a:
                    return result
                b=min(b,result)
                print (a,b)
	#print result
	return result

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        resultAction= []
        resultValue = []
        #print gameState.getNumAgents()
        print self.depth
        a = -999999
        b = 999999
        
        for action in gameState.getLegalActions(0):
            temp = self.minValue(gameState.generateSuccessor(0, action),1,1,a,b)
            a = max(a,temp)
            #print "ROOT: "
            #print(a,b)
	    resultValue.append(temp)
	    resultAction.append(action)
        maxIndex = max(resultValue)
        for i in range(len(resultValue)):
            if resultValue[i]==maxIndex:
                break
        
        #print resultValue
        #print i
        return resultAction[i]    

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def maxValue(self,state,depth):
	if state.isWin() or state.isLose():
        # if depth == self.depth:
            #print self.evaluationFunction(state)
	    return self.evaluationFunction(state)
	result = -999999
	for action in state.getLegalActions(0):
	    result = max(result,self.minValue(state.generateSuccessor(0, action),depth,1))
	#print result
	return result

    def minValue(self,state,depth,level):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        result = []
        if level==state.getNumAgents()-1:
	    for action in state.getLegalActions(level):
                if depth ==self.depth:
                    result.append(self.evaluationFunction(state.generateSuccessor(level, action)))
		else:
                    result.append(self.maxValue(state.generateSuccessor(level, action),depth+1))
        else:
	    for action in state.getLegalActions(level):
		result.append(self.minValue(state.generateSuccessor(level, action),depth,level+1))
	#print result
	mean = 0
	for i in range(len(result)):
            mean+=(float)(result[i])
        mean = mean/len(result)
	return mean

    def getAction(self, gameState):

        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        resultAction= []
        resultValue = []
        #print gameState.getNumAgents()
        #print self.depth
        for action in gameState.getLegalActions(0):
	    resultValue.append(self.minValue(gameState.generateSuccessor(0, action),1,1))
	    resultAction.append(action)
        maxIndex = max(resultValue)
        for i in range(len(resultValue)):
            if resultValue[i]==maxIndex:
                break
        
        #print resultValue
        #print i
        return resultAction[i]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood().asList()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    NumofFood = currentGameState.getNumFood()
    locationOfCap =  currentGameState.getCapsules()
    GhostPos = currentGameState.getGhostPositions()
    
    curScore = currentGameState.getScore()
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return - float("inf")
    distanceToFood = []
    gradeForFood = 0
    if Pos in Food:
        gradeForFood = 60
    else:
        for food in Food:
            distanceToFood.append(util.manhattanDistance(Pos,food))
        if distanceToFood != []:
            distanceToFood.sort()
            if len(distanceToFood)>=3:
                gradeForFood = gradeForFood - distanceToFood[0]-distanceToFood[1]-distanceToFood[2]
            #else:
                #gradeForFood = gradeForFood - min(distanceToFood)-NumofFood*200
    
    gradeForGhost = 0
    nearestGhostDistance = -999999
    for i in range(len(GhostPos)):
        if ScaredTimes[i] == 0:
            if util.manhattanDistance(Pos,GhostPos[i]) < nearestGhostDistance:
                nearestGhostDistance = util.manhattanDistance(Pos,GhostPos[i])
        elif ScaredTimes[i] > util.manhattanDistance(Pos,GhostPos[i]):
            gradeForGhost += 200 - util.manhattanDistance(Pos,GhostPos[i])

    curScore = curScore - NumofFood*10 +gradeForGhost+gradeForFood
    return curScore
    
# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

