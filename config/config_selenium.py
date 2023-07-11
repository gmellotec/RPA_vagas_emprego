from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager



def config_selenium():
    executable_path = ChromeDriverManager().install()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument(r'user-data-dir=C:\Users\GuilhermeMello\AppData\Local\Google\Chrome\User Data\Profile Selenium')
    driver = webdriver.Chrome(executable_path=executable_path)

    return driver
