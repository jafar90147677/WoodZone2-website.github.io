import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver():
    options = Options()
    options.add_argument("--headless=new")       # run without GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ unique user-data-dir for each test run
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")

    return webdriver.Chrome(options=options)
def test_homepage_title():
    driver = create_driver()
    driver.get("http://localhost:8080")   # adjust if different
    assert "Jenkins" in driver.title      # ✅ match the real title
    driver.quit()
