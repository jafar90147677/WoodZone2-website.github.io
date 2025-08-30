from selenium import webdriver

def test_homepage_title():
    driver = webdriver.Chrome()
    driver.get("https://jafar90147677.github.io/WoodZone2-website.github.io/")  # your GitHub Pages URL
    assert "Woodzone" in driver.title
    driver.quit()
