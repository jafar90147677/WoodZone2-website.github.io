import os
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions


def running_in_ci() -> bool:
    return any(os.getenv(var) for var in ["JENKINS_URL", "BUILD_ID", "CI"])


def create_driver():
    edge_options = EdgeOptions()

    if running_in_ci():
        # Headless for Jenkins/CI
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("--disable-gpu")

    # Unique profile per run
    temp_dir = tempfile.mkdtemp()
    edge_options.add_argument(f"--user-data-dir={temp_dir}")

    # Reduce noisy Chromium logs locally
    edge_options.add_argument("--log-level=3")

    # Works if msedgedriver is on PATH
    return webdriver.Edge(options=edge_options)


def test_homepage_title():
    driver = create_driver()
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    driver.get(base_url)
    assert "WoodZone" in driver.title

    # In CI/Jenkins, exit immediately (headless)
    if running_in_ci():
        try:
            driver.quit()
        except BaseException:
            pass
        return

    # Local behavior: default is to keep the browser open indefinitely
    hold_value = os.getenv("HOLD_OPEN_SECONDS", "-1").strip()
    is_indefinite = hold_value in ("-1", "inf", "infinite", "INFINITE")

    try:
        if is_indefinite:
            # Wait until the user closes the browser window
            while True:
                if len(driver.window_handles) == 0:
                    break
                time.sleep(1)
        else:
            # Timed hold if a positive number is provided
            try:
                hold_seconds = max(0, int(hold_value))
            except ValueError:
                hold_seconds = 0
            if hold_seconds > 0:
                time.sleep(hold_seconds)
    except KeyboardInterrupt:
        # Allow clean cancel without traceback
        pass
    except Exception:
        # Ignore transient WebDriver errors during hold
        pass
    finally:
        # Ensure driver shuts down cleanly, even if interrupted
        try:
            driver.quit()
        except BaseException:
            pass

# import pytest
# from selenium import webdriver
# from selenium.webdriver.edge.options import Options

# @pytest.fixture
# def driver():
#     edge_options = Options()
#     # Run headless in Jenkins if no display available:
#     # edge_options.add_argument("--headless")
#     # edge_options.add_argument("--disable-gpu")

#     # No need for Service() if driver is in PATH
#     driver = webdriver.Edge(options=edge_options)
#     yield driver
#     driver.quit()

# def test_homepage_title(driver):
#     driver.get("http://localhost:8080")
#     print("Page Title:", driver.title)
#     assert "Simple Product" in driver.title







