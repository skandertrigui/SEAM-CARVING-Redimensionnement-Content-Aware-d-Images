import numpy as np
from typing import Tuple

class ForwardEnergyComputer:
    """Computes improved and smoothed forward energy for content-aware resizing."""
    
    def __init__(self, image: np.ndarray):
        """Initialize with an image."""
        self.image = image.astype(np.float64)
        self.height, self.width = image.shape[:2]
        
    def _smooth_map(self, arr: np.ndarray) -> np.ndarray:
        """Simple 3x3 box blur using numpy for smoother seams."""
        # Check if W > 2 and H > 2 to avoid roll artifacts
        if arr.shape[0] < 3 or arr.shape[1] < 3:
            return arr
            
        smoothed = (arr + 
                   np.roll(arr, 1, axis=0) + np.roll(arr, -1, axis=0) +
                   np.roll(arr, 1, axis=1) + np.roll(arr, -1, axis=1)) / 5.0
        return smoothed
        
    def compute_forward_energy_map(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute forward energy cost maps with smoothing.
        """
        L = np.roll(self.image, 1, axis=1)
        R = np.roll(self.image, -1, axis=1)
        U = np.roll(self.image, 1, axis=0)
        
        cv = np.sum(np.abs(R - L), axis=2)
        cl = cv + np.sum(np.abs(U - L), axis=2)
        cr = cv + np.sum(np.abs(U - R), axis=2)
        
        # Apply smoothing to reduce jagged artifacts
        cv = self._smooth_map(cv)
        cl = self._smooth_map(cl)
        cr = self._smooth_map(cr)
        
        # Penalty for edges (boundary handling)
        edge_penalty = np.max(cv) * 10
        cv[:, [0, -1]] = edge_penalty
        cl[:, [0, -1]] = edge_penalty
        cr[:, [0, -1]] = edge_penalty
        
        # Initial row penalty on edges
        cv[0, [0, -1]] = edge_penalty
        cl[0, [0, -1]] = edge_penalty
        cr[0, [0, -1]] = edge_penalty
        
        return cl, cv, cr
