class Vertex:
    def __init__(self,id, player, priority,pointTo):
        self.id = id
        self.player = player
        self.priority = priority
        self.pointTo = pointTo
        self.checkPlayer()
        self.checkPriority()

    
        
    def getId(self):
        return self.id

    def getPlayer(self):
        return self.player
    
    def getPriority(self):
        #winFor = self.priority%2
        return self.priority

    def getPointTo(self):
        return self.pointTo


    def winerFor(self):
        winFor = self.priority%2
        return winFor
    
    def checkEdgeRange(self, graphSize):
        if self.id < graphSize:
            corRange = True
        else:
            return False
            
        for i in self.pointTo:
            if i >= graphSize:
                corRange = False
                break
        
        return corRange

    def checkPlayer(self):
        if self.player not in (0, 1):
            raise ValueError("Player must be 0 or 1.")
    
    def checkPriority(self):
        if self.priority < 0 or not self.priority % 1 == 0 :
            raise ValueError("Priority must be a positive integer.")
    
    def addPath(self, newGoals):
        self.pointTo.append(newGoals)
    
    def changePath(self, newGoals):
        self.pointTo = self.pointTo[1:]
        self.pointTo.append(newGoals)
