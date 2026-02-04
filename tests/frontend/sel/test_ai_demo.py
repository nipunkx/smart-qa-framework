"""Demo test for AI failure analysis"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.browser("chrome")
def test_demo_ai_analysis(driver, base_url):
    """Demo test that fails to show AI analysis"""
    driver.get(base_url)
    
    # This will fail - element doesn't exist
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "#nonexistent-element"))
    )