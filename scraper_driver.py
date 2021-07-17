import base64
import itertools
import os
import requests
from urllib import parse
from io import BytesIO
from PIL import Image
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from config import Config, Dotdict
import string
import re
import hashlib
import stocks

class ScraperDriver(Config, Dotdict):
    def __init__(self, c):
        self.config = Dotdict(c.config)
        self.driver_location = c.driver_location
        self.api_key = c.api_key

    def check_b64(self, source):
        header = source.split(',')[0]
        if header.startswith('data') and header.endswith(';base64'):
            image_type = re.search('data:image/(.*);base64', header)
            return image_type
        return False

    def save_images(self, images_dl, files_path, src, img_name=''):
        is_b64 = self.check_b64(src)
        write = True
        # Base64
        if is_b64:
            extension = is_b64
            content = base64.b64decode(src.split(';base64')[1])
            filename = 'base64-' + str(hashlib.md5(content).hexdigest())
            if not self.config.overwrite and filename + '.' + extension in images_dl:
                write = False

        # URL
        else:
            try:
                if img_name != '':
                    filename = img_name
                else:
                    filename, _ = os.path.splitext(src.split('/')[-1])
                resp = requests.get(src, stream=True, headers={'User-Agent': 'Mozilla/5.0'})

                if len(resp.content)>0:
                    image = Image.open(BytesIO(resp.content))
                    extension = image.format.lower()
                    content = resp.content
                    if not self.config.overwrite and filename+'.'+extension in images_dl:
                        write = False
                else:
                    write = False

            except Exception as e:
                print('[ERROR]', e)
                return False

        if write:
            with open(os.path.join(files_path, filename+'.'+extension), 'wb') as f:
                f.write(content)

        return True

    def start_driver(self):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4183.102 Safari/537.36'
        options = Options()
        if self.config.headless:
            options.add_argument("--headless")
            options.add_argument("--window-size=6000x2000")

        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--allow-cross-origin-auth-prompt")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')

        driver = webdriver.Chrome(executable_path=self.driver_location, options=options)
        driver.maximize_window()

        return driver

    def launch_scraping(self):
        driver = self.start_driver()

        for keyword, stock in itertools.product(self.config.search, self.config.stocks):
            print('[KEYWORD - STOCK]', keyword+' - '+stock)
            keyword = keyword.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
            search = parse.quote(keyword)

            files_path = os.path.join(self.config.dir, search.replace(" ", "_"), stock)
            os.makedirs(files_path, exist_ok=True)
            dl = [i for i in os.listdir(files_path)]

            kwargs = {
                'driver':driver,
                'search':search,
                'total_images':self.config.images,
                'images_remaining':self.config.images,
                'images_dl':dl,
                'files_path':files_path,
                'save_images':self.save_images,
                'api_key':self.api_key
            }
            c = getattr(stocks, stock.capitalize())(**kwargs)
            c.api() if self.config.api_first and 'api' in dir(c) else c.scraper()
            print(end="\n")