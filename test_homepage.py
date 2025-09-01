# import os
# import time
# import tempfile
# import uuid
# from selenium import webdriver
# from selenium.webdriver.edge.options import Options as EdgeOptions
# from selenium.webdriver.chrome.options import Options as ChromeOptions


# def running_in_ci() -> bool:
#     return any(os.getenv(var) for var in ["JENKINS_URL", "BUILD_ID", "CI"])


# def create_driver():
#     # Use Chrome in CI/Jenkins (chromium + chromium-driver available)
#     # Use Edge locally (built into Windows)
#     use_chrome = running_in_ci()
    
#     if use_chrome:
#         options = ChromeOptions()
#         options.add_argument("--headless=new")
#         options.add_argument("--disable-gpu")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#     else:
#         options = EdgeOptions()

#     # Highly unique profile directory to avoid collisions
#     unique_suffix = f"{os.getpid()}_{int(time.time())}_{uuid.uuid4().hex[:8]}"
#     temp_dir = tempfile.mkdtemp(prefix=f"selenium_profile_{unique_suffix}_")
#     options.add_argument(f"--user-data-dir={temp_dir}")

#     # Reduce noisy Chromium logs
#     options.add_argument("--log-level=3")

#     return webdriver.Chrome(options=options) if use_chrome else webdriver.Edge(options=options)


# def test_homepage_title():
#     driver = create_driver()
#     base_url = os.getenv("BASE_URL", "http://localhost:8000")
#     driver.get(base_url)
#     assert "WoodZone" in driver.title

#     # In CI/Jenkins, exit immediately (headless)
#     if running_in_ci():
#         try:
#             driver.quit()
#         except BaseException:
#             pass
#         return

#     # Local behavior: default is to keep the browser open indefinitely
#     hold_value = os.getenv("HOLD_OPEN_SECONDS", "-1").strip()
#     is_indefinite = hold_value in ("-1", "inf", "infinite", "INFINITE")

#     try:
#         if is_indefinite:
#             # Wait until the user closes the browser window
#             while True:
#                 if len(driver.window_handles) == 0:
#                     break
#                 time.sleep(1)
#         else:
#             # Timed hold if a positive number is provided
#             try:
#                 hold_seconds = max(0, int(hold_value))
#             except ValueError:
#                 hold_seconds = 0
#             if hold_seconds > 0:
#                 time.sleep(hold_seconds)
#     except KeyboardInterrupt:
#         # Allow clean cancel without traceback
#         pass
#     except Exception:
#         # Ignore transient WebDriver errors during hold
#         pass
#     finally:
#         # Ensure driver shuts down cleanly, even if interrupted
#         try:
#             driver.quit()
#         except BaseException:
#             pass

# # import pytest
# # from selenium import webdriver
# # from selenium.webdriver.edge.options import Options

# # @pytest.fixture
# # def driver():
# #     edge_options = Options()
# #     # Run headless in Jenkins if no display available:
# #     # edge_options.add_argument("--headless")
# #     # edge_options.add_argument("--disable-gpu")

# #     # No need for Service() if driver is in PATH
# #     driver = webdriver.Edge(options=edge_options)
# #     yield driver
# #     driver.quit()

# # def test_homepage_title(driver):
# #     driver.get("http://localhost:8080")
# #     print("Page Title:", driver.title)
# #     assert "Simple Product" in driver.title



import os
import time
import tempfile
import uuid
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService


def running_in_ci() -> bool:
    """Detect if running inside Jenkins/CI."""
    return any(os.getenv(var) for var in ["JENKINS_URL", "BUILD_ID", "CI"])


def create_driver():
    # Use Chrome inside CI/Jenkins (with system-installed chromedriver)
    # Use Edge locally on Windows
    use_chrome = running_in_ci()

    if use_chrome:
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--log-level=3")

        # Explicitly point to the chromedriver installed in Dockerfile.jenkins
        service = ChromeService(executable_path="/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

    else:
        options = EdgeOptions()
        unique_suffix = f"{os.getpid()}_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        temp_dir = tempfile.mkdtemp(prefix=f"selenium_profile_{unique_suffix}_")
        options.add_argument(f"--user-data-dir={temp_dir}")
        options.add_argument("--log-level=3")

        service = EdgeService()  # Edge driver must be in PATH on Windows
        driver = webdriver.Edge(service=service, options=options)

    return driver


def test_homepage_title():
    driver = create_driver()
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    driver.get(base_url)
    assert "WoodZone" in driver.title

    if running_in_ci():
        try:
            driver.quit()
        except BaseException:
            pass
        return

    hold_value = os.getenv("HOLD_OPEN_SECONDS", "-1").strip()
    is_indefinite = hold_value in ("-1", "inf", "infinite", "INFINITE")

    try:
        if is_indefinite:
            while driver.window_handles:
                time.sleep(1)
        else:
            try:
                hold_seconds = max(0, int(hold_value))
            except ValueError:
                hold_seconds = 0
            if hold_seconds > 0:
                time.sleep(hold_seconds)
    except (KeyboardInterrupt, Exception):
        pass
    finally:
        try:
            driver.quit()
        except BaseException:
            pass



