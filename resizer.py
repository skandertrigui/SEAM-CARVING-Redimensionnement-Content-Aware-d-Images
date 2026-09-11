import numpy as np
from typing import List, Tuple
import time
from forward_energy import ForwardEnergyComputer
from matrix_seam import MatrixSeamCalculator
from image_utils import ImageManipulator

class ContentAwareResizer:
    """Main class for content-aware image resizing."""
    
    def __init__(self, image_path: str = None, image_array: np.ndarray = None):
        """Initialize resizer."""
        if image_path:
            self.original = ImageManipulator.load_image(image_path)
        elif image_array is not None:
            self.original = image_array
        else:
            raise ValueError("Provide either image_path or image_array")
        
        self.current = self.original.copy()
        self.operation_log = []
        
    def carve_vertical_seam(self, verbose: bool = False) -> Tuple[np.ndarray, List[int], float]:
        """Remove one vertical seam."""
        start_time = time.time()
        energy_computer = ForwardEnergyComputer(self.current)
        cost_L, cost_M, cost_R = energy_computer.compute_forward_energy_map()
        
        calculator = MatrixSeamCalculator()
        seam, cost = calculator.find_vertical_seam(cost_L, cost_M, cost_R)
        
        new_image = ImageManipulator.remove_vertical_seam(self.current, seam)
        self.current = new_image
        
        elapsed = time.time() - start_time
        self.operation_log.append({'cost': cost, 'time': elapsed})
        
        if verbose:
            print(f"Carved seam: cost={cost:.2f}, time={elapsed*1000:.1f}ms")
        
        return new_image, seam, cost
    
    def carve_horizontal_seam(self) -> Tuple[np.ndarray, List[int], float]:
        """Remove one horizontal seam."""
        start_time = time.time()
        energy_computer = ForwardEnergyComputer(self.current)
        cost_L, cost_M, cost_R = energy_computer.compute_forward_energy_map()
        
        calculator = MatrixSeamCalculator()
        seam, cost = calculator.find_horizontal_seam(cost_L, cost_M, cost_R)
        
        new_image = ImageManipulator.remove_horizontal_seam(self.current, seam)
        self.current = new_image
        
        elapsed = time.time() - start_time
        self.operation_log.append({'cost': cost, 'time': elapsed})
        
        return new_image, seam, cost
    
    def resize(self, target_width: int = None, target_height: int = None,
              verbose: bool = True) -> np.ndarray:
        """Resize to target dimensions."""
        if target_width is not None:
            delta = self.current.shape[1] - target_width
            for i in range(delta):
                self.carve_vertical_seam()
                if verbose and (i + 1) % 10 == 0:
                    print(f"  Width progress: {i+1}/{delta}")
        
        if target_height is not None:
            delta = self.current.shape[0] - target_height
            for i in range(delta):
                self.carve_horizontal_seam()
                if verbose and (i + 1) % 10 == 0:
                    print(f"  Height progress: {i+1}/{delta}")
        
        return self.current
    
    def save_result(self, filepath: str):
        """Save current image."""
        ImageManipulator.save_image(self.current, filepath)
    
    def get_statistics(self) -> dict:
        """Get statistics."""
        if not self.operation_log:
            return {'total_time': 0, 'average_time_per_seam': 0}
        total_time = sum(op['time'] for op in self.operation_log)
        return {
            'total_time': total_time,
            'average_time_per_seam': total_time / len(self.operation_log)
        }
