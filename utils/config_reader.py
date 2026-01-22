"""
Configuration Reader
Loads settings from config.yaml file
"""
import yaml
import os


class ConfigReader:
    """Read configuration from YAML file"""
    
    def __init__(self, config_file='config/config.yaml'):
        """Initialize and load config file"""
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """Load YAML configuration file"""
        # Get the project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        config_path = os.path.join(project_root, self.config_file)
        
        # Read the YAML file
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    
    def get(self, section, key=None):
        """
        Get configuration value
        
        Examples:
            config.get('application', 'base_url')
            config.get('selenium', 'browser')
        """
        if key:
            return self.config.get(section, {}).get(key)
        return self.config.get(section)
    
    def get_base_url(self):
        """Shortcut to get base URL"""
        return self.get('application', 'base_url')
    
    def get_admin_url(self):
        """Shortcut to get admin URL"""
        return self.get('application', 'admin_url')
    
    def get_browser(self):
        """Shortcut to get browser name"""
        return self.get('selenium', 'browser')
    
    def is_headless(self):
        """Check if tests should run in headless mode"""
        return self.get('selenium', 'headless')
    
    def get_implicit_wait(self):
        """Get implicit wait timeout"""
        return self.get('selenium', 'implicit_wait')
    
    def get_page_load_timeout(self):
        """Get page load timeout"""
        return self.get('selenium', 'page_load_timeout')
    
    def get_credentials(self, user_type='admin'):
        """
        Get credentials for a user type
        
        Args:
            user_type: 'admin' or 'customer'
        
        Returns:
            dict with username/email and password
        """
        if user_type == 'admin':
            return {
                'username': self.get('credentials', 'admin_username'),
                'password': self.get('credentials', 'admin_password')
            }
        elif user_type == 'customer':
            return {
                'email': self.get('credentials', 'customer_email'),
                'password': self.get('credentials', 'customer_password')
            }
    
    def get_window_size(self):
        """Get browser window size"""
        return {
            'width': self.get('selenium', 'window_width'),
            'height': self.get('selenium', 'window_height')
        }
    
    def get_screenshot_folder(self):
        """Get screenshot folder path"""
        return self.get('test_settings', 'screenshot_folder')
    
    def should_screenshot_on_failure(self):
        """Check if screenshots should be taken on test failure"""
        return self.get('test_settings', 'screenshot_on_failure')
    
    def get_parallel_workers(self):
        """Get number of parallel workers for test execution"""
        return self.get('test_settings', 'parallel_workers')


# Create a global config instance
config = ConfigReader()