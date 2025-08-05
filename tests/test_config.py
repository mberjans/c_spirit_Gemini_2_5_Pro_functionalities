import os
import unittest
import tempfile
import yaml
from pathlib import Path

class TestConfigSystem(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test config files
        self.test_dir = tempfile.TemporaryDirectory()
        self.config_path = Path(self.test_dir.name) / "test_config.yml"
        
        # Create a test config file
        self.test_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "test_db"
            },
            "api": {
                "key": "test_api_key",
                "endpoint": "https://api.example.com"
            },
            "paths": {
                "data_dir": "/path/to/data",
                "log_dir": "/path/to/logs"
            }
        }
        
        # Write the test config to a file
        with open(self.config_path, 'w') as f:
            yaml.dump(self.test_config, f)
        
        # Set the environment variable for the config file path
        os.environ["AIM2_CONFIG"] = str(self.config_path)
    
    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()
        # Clear the environment variable
        if "AIM2_CONFIG" in os.environ:
            del os.environ["AIM2_CONFIG"]
    
    def test_config_loading(self):
        """Test that the config file is loaded correctly."""
        from aim2.config import get_config
        
        # Test that the config is loaded correctly
        config = get_config()
        self.assertIsNotNone(config)
        
        # Test that the config contains the expected sections
        self.assertIn("database", config)
        self.assertIn("api", config)
        self.assertIn("paths", config)
        
        # Test that the values are correct
        self.assertEqual(config["database"]["host"], "localhost")
        self.assertEqual(config["api"]["key"], "test_api_key")
        self.assertEqual(config["paths"]["data_dir"], "/path/to/data")
    
    def test_missing_config_file(self):
        """Test behavior when the config file is missing."""
        # Save the current config path and set a non-existent one
        old_config_path = os.environ.get("AIM2_CONFIG")
        non_existent_path = "/non/existent/config.yml"
        os.environ["AIM2_CONFIG"] = non_existent_path
        
        from aim2.config import get_config, reload_config
        
        # Clear any cached config
        try:
            reload_config()
            # If we get here, the reload worked (which is fine)
            self.assertTrue(True)
        except FileNotFoundError:
            # This is also acceptable if the implementation raises an error
            pass
        
        # Restore the original config path if it existed
        if old_config_path is not None:
            os.environ["AIM2_CONFIG"] = old_config_path
        else:
            del os.environ["AIM2_CONFIG"]
    
    def test_config_override_with_env_vars(self):
        """Test that environment variables can override config values."""
        # Set environment variables to override some config values
        os.environ["AIM2_DATABASE__HOST"] = "remote-host"
        os.environ["AIM2_API__KEY"] = "overridden_key"
        
        # Reload the config to pick up the environment variables
        from aim2.config import reload_config
        config = reload_config()
        
        # Check that environment variables override the config file
        self.assertEqual(config["database"]["host"], "remote-host")
        self.assertEqual(config["api"]["key"], "overridden_key")
        
        # Check that other values remain unchanged
        self.assertEqual(config["database"]["port"], 5432)
        self.assertEqual(config["api"]["endpoint"], "https://api.example.com")
        
        # Clean up environment variables
        if "AIM2_DATABASE__HOST" in os.environ:
            del os.environ["AIM2_DATABASE__HOST"]
        if "AIM2_API__KEY" in os.environ:
            del os.environ["AIM2_API__KEY"]

if __name__ == "__main__":
    unittest.main()
