_X = 1
_O = 2
_N = 0

class RuleBasedAgent:
    def __init__(self):
        pass
    
    def _conjugatePlayer(self, player):
        if player == _X:
            return _O
        else:
            return _X
    
    def act(self, grid, currentRole):
        enemy = self._conjugatePlayer(currentRole)
        
        #check to target win
        for i in range(3):
            for j in range(3):
                if grid[i][j] == _N:
                    copyGrid = grid.copy()
                    copyGrid[i][j] = currentRole
                    
                    role = self._getWinner(copyGrid)
                    if role == currentRole:
                        return i*3 + j        
        
        #check to ignore loss
        for i in range(3):
            for j in range(3):
                if grid[i][j] == _N:
                    copyGrid = grid.copy()
                    copyGrid[i][j] = currentRole
                    
                    role = self._getWinner(copyGrid)
                    if role == enemy:
                        return i*3 + j
                        
        # #return default
        # for i in range(3):
        #     for j in range(3):
        #         if grid[i][j] == _N:
        #             return i*3 + j
        
        return -1
        
    def _getWinner(self, grid):
        #check rows
        for i in range(3):
            if grid[i][0] == grid[i][1] == grid[i][2] and grid[i][0] != _N:
                return grid[i][0]
        
        #check cols
        for j in range(3):
            if grid[0][j] == grid[1][j] == grid[2][j] and grid[0][j] != _N:
                return grid[0][j]
                
        #check \
        if grid[0][0] == grid[1][1] == grid[2][2] and grid[0][0] != _N:
            return grid[0][0]
            
        #check /
        if grid[0][2] == grid[1][1] == grid[2][0] and grid[0][2] != _N:
            return grid[0][2]
            
        return 0