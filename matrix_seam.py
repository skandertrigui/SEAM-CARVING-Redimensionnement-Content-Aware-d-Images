import numpy as np
from typing import List, Tuple

class MatrixSeamCalculator:
    """Optimized matrix operations for finding seams (Forward Energy)."""
    
    def find_vertical_seam(self, cost_L: np.ndarray,
                          cost_M: np.ndarray,
                          cost_R: np.ndarray) -> Tuple[List[int], float]:
        """
        Find optimal vertical seam using vectorized cumulative minimum energy.
        """
        H, W = cost_M.shape
        M = np.full((H, W), np.inf)
        M[0, :] = cost_M[0, :]
        
        # backtrack stores the offset (-1, 0, 1) to the previous row's column
        backtrack = np.zeros((H, W), dtype=int)
        
        for i in range(1, H):
            m_left = np.roll(M[i-1], 1)
            m_left[0] = np.inf
            m_mid = M[i-1]
            m_right = np.roll(M[i-1], -1)
            m_right[-1] = np.inf
            
            # Stack possible costs: [left, middle, right]
            stacked = np.stack([
                m_left + cost_L[i],
                m_mid + cost_M[i], 
                m_right + cost_R[i]
            ])
            
            M[i] = np.min(stacked, axis=0)
            backtrack[i] = np.argmin(stacked, axis=0) - 1
        
        # Backtrack from the bottom
        j = np.argmin(M[H-1, :])
        total_cost = M[H-1, j]
        
        seam = np.zeros(H, dtype=int)
        seam[H-1] = j
        for i in range(H-1, 0, -1):
            j = j + backtrack[i, j]
            seam[i-1] = j
            
        return seam.tolist(), float(total_cost)

    def find_horizontal_seam(self, cost_L: np.ndarray,
                             cost_M: np.ndarray,
                             cost_R: np.ndarray) -> Tuple[List[int], float]:
        """Find horizontal seam by transposing."""
        return self.find_vertical_seam(cost_L.T, cost_M.T, cost_R.T)
