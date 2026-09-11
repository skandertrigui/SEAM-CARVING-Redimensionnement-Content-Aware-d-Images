import numpy as np
from PIL import Image
from typing import List

class ImageManipulator:
    """Utilities for image loading, saving and seam carving operations."""
    
    @staticmethod
    def load_image(path: str) -> np.ndarray:
        """Load image as RGB numpy array."""
        img = Image.open(path).convert('RGB')
        return np.array(img)
    
    @staticmethod
    def save_image(image: np.ndarray, path: str):
        """Save numpy array as image."""
        Image.fromarray(image.astype(np.uint8)).save(path)
        
    @staticmethod
    def remove_vertical_seam(image: np.ndarray, seam: List[int]) -> np.ndarray:
        """Remove a vertical seam from the image."""
        H, W, C = image.shape
        new_image = np.zeros((H, W - 1, C), dtype=image.dtype)
        for i in range(H):
            j = seam[i]
            new_image[i, :j] = image[i, :j]
            new_image[i, j:] = image[i, j+1:]
        return new_image
        
    @staticmethod
    def remove_horizontal_seam(image: np.ndarray, seam: List[int]) -> np.ndarray:
        """Remove a horizontal seam from the image."""
        temp = np.transpose(image, (1, 0, 2))
        temp = ImageManipulator.remove_vertical_seam(temp, seam)
        return np.transpose(temp, (1, 0, 2))
