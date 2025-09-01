# import tempfile
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

# def create_driver():
#     options = Options()
#     options.add_argument("--headless=new")       # run without GUI
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")

#     # ✅ unique user-data-dir for each test run
#     temp_dir = tempfile.mkdtemp()
#     options.add_argument(f"--user-data-dir={temp_dir}")

#     return webdriver.Chrome(options=options)
# def test_homepage_title():
#     driver = create_driver()
#     driver.get("http://localhost:8080")   # adjust if different
#     assert "Jenkins" in driver.title      # ✅ match the real title
#     driver.quit()
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

@pytest.fixture
def driver():
    # Set Edge options
    edge_options = Options()
    # Run headless in Jenkins (no browser window):
    # edge_options.add_argument("--headless")
    # edge_options.add_argument("--disable-gpu")

    # Path to msedgedriver.exe
    service = Service("C:/WebDrivers/msedgedriver.exe")

    # Start Edge browser
    driver = webdriver.Edge(service=service, options=edge_options)
    yield driver
    driver.quit()

def test_homepage_title(driver):
    # Open your local server
    driver.get("http://localhost:8080")

    # Debug: print the page title
    print("Page Title:", driver.title)

    # Assert the title contains expected text
    assert "Simple Product" in driver.title

