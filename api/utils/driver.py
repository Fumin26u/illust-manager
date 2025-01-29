from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setDriver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-default-browser-check")
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    options.add_argument('--user-agent=' + USER_AGENT)
    driver = webdriver.Chrome(options=options)
    
    return driver