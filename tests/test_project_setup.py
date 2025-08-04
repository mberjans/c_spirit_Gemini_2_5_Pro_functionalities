import os
import unittest
from pathlib import Path

class TestProjectSetup(unittest.TestCase):    
    def test_package_structure_exists(self):
        """Test that all required package directories exist."""
        base_dir = Path(__file__).parent.parent
        required_dirs = [
            'aim2',
            'aim2/ontology',
            'aim2/corpus',
            'aim2/extraction',
            'aim2/postprocessing',
            'tests'
        ]
        
        for dir_path in required_dirs:
            full_path = base_dir / dir_path
            self.assertTrue(
                full_path.exists() and full_path.is_dir(),
                f"Directory does not exist: {dir_path}"
            )

if __name__ == '__main__':
    unittest.main()
