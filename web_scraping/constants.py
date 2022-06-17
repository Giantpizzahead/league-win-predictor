from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

champ_cache_folder = 'data/champ_cache'

# Setup the browser
# chromedriver.exe is located in C:\Program Files\LOVE
ser = Service('chromedriver.exe')
op = webdriver.ChromeOptions()
op.add_argument('--window-size=500,400')
des = DesiredCapabilities().CHROME
# des['pageLoadStrategy'] = 'eager'
driver = webdriver.Chrome(service=ser, options=op) # , desired_capabilities=des)
