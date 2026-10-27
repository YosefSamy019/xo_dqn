import numpy as np
import cv2

_X = 1
_O = 2
_N = 0

_gridShape = (3, 3)

class XO_Env:
    def __init__(self):
        self.reset(randomGrid=False)
    
    def _conjugatePlayer(self, player):
        return [_O, _X][player-1]
    
    def _getCurrentState(self):
        s = []
        
        # Add current player state, one hot encoder
        s.append(self._curPlayer == _X) 
        s.append(self._curPlayer == _O) 

        # Add each cell state, use one hot encoder
        for i in range(_gridShape[0]):
            for j in range(_gridShape[1]):
                s.append(self._grid[i, j] == _X)
                s.append(self._grid[i, j] == _O)
                s.append(self._grid[i, j] == _N)

        return np.array(s).astype(int)
    
    def getStateShape(self):
        return self._getCurrentState().shape
        
    def getActionsCount(self):
        return _gridShape[0] * _gridShape[1]
        
    def getGrid(self):
        return self._grid.copy()
        
    def getCurrentPlayer(self):
        return self._curPlayer
        
    def reset(self, randomGrid = True):
        self._grid = np.ones(_gridShape) * _N
        
        self._curPlayer = np.random.choice([_X, _O])
        
        self._gameDone = False
        
        if randomGrid == False:
            return self._getCurrentState()
        else:
            if np.random.rand() < 0.75:
                for i in range(4):
                    action = np.random.randint(0, _gridShape[0] * _gridShape[1])
                    
                    if self._grid[action // 3, action % 3] == _N:
                        self.step(action)
            return self._getCurrentState()
        
    def render(self):
        dimension = 248
        cmap = {_X: (255,0,0), _O: (0,255,0), _N: (100,100,0)}
        txt = {_X: 'X', _O: 'O', _N: '-'}
        
        image = np.ones((dimension, dimension, 3),dtype=np.uint8) * 255
        
        # Add text to the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1        
        thickness = 2
        
        for i in range(_gridShape[0]):
            for j in range(_gridShape[1]):
                # if self._grid[i,j] != _N:
                    segment = dimension / 4
                    pos_x = int(segment * (i + 0.5) - 10)
                    pos_y = int(segment * (j + 0.5) + 10)
                
                    cv2.putText(image, txt[self._grid[i,j]], (pos_x,pos_y), font, font_scale, cmap[self._grid[i,j]], thickness)
        return image
        
    def step(self, action):
        action_i, action_j = action // 3, action % 3
        s, d, r = None, False, 0
        
        if self._gameDone == True:
            s = self._getCurrentState()
            r = 0
            d = True            
            return s,d,r
            
        if self._grid[action_i, action_j] != _N:
            r += -50  # Cell is not empty
            d = True
            s = self._getCurrentState()
            
            return s, d, r
            
        else:
            self._grid[action_i, action_j] = self._curPlayer
            r -= 2  # Movement cost
            
            # Check cols if equal
            for i in range(_gridShape[0]):
                if self._grid[i, 0] == self._grid[i, 1] == self._grid[i, 2] == self._curPlayer:
                    r += 50  # Winning
                    d = True
                elif self._grid[i, 0] == self._grid[i, 1] == self._grid[i, 2] == self._conjugatePlayer(self._curPlayer):
                    r -= 50  # Lossing
                    d = True
                    
            # Check rows if equal
            for j in range(_gridShape[1]):
                if self._grid[0, j] == self._grid[1, j] == self._grid[2, j] == self._curPlayer:
                    r += 50  # Winning
                    d = True
                elif self._grid[0, j] == self._grid[1, j] == self._grid[2, j] == self._conjugatePlayer(self._curPlayer):
                    r -= 50  # Lossing
                    d = True
                    
            # Check \
            if self._grid[0, 0] == self._grid[1, 1] == self._grid[2, 2] == self._curPlayer:
                r += 50  # Winning
                d = True
                
            elif self._grid[0, 0] == self._grid[1, 1] == self._grid[2, 2] ==  self._conjugatePlayer(self._curPlayer):
                r -= 50  # Lossing
                d = True
                    
            # Check /
            if self._grid[0, 2] == self._grid[1, 1] == self._grid[2, 0] == self._curPlayer:
                r += 50  # Winning
                d = True
            elif self._grid[0, 2] == self._grid[1, 1] == self._grid[2, 0] == self._conjugatePlayer(self._curPlayer):
                r -= 50  # Lossing
                d = True
                
            # Check tie
            if not any(self._grid[i, j] == _N for i in range(_gridShape[0]) for j in range(_gridShape[1])) and not d:
                r += 20  # Tie
                d = True
                    
        # Swap player
        self._curPlayer = self._conjugatePlayer(self._curPlayer)
        
        # Get new state
        s = self._getCurrentState()
        
        #store game state
        self._gameDone = d
        
        return s, d, r
        
        
        

    