from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
class ClassSearch:
    def __init__(self,url):
        self.opts = Options()
        self.opts.add_argument("--start-maximized")
        self.opts.add_argument('--log-level=1') # Para que no salga "Created TensorFlow"

        self.opts.add_argument("--headless")  # Ejecutar en modo headless (Segundo plano)
        self.opts.add_argument("--mute-audio")  # Silenciar el audio
        self.opts.add_experimental_option("excludeSwitches", ['enable-logging']) 
        self.opts.add_experimental_option('useAutomationExtension', False)

        self.url =url
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome()
        
        self.driver.get(self.url)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        # Configuración de opciones de Chrome
        
    def closeConexion(self):
        self.driver.quit()
        