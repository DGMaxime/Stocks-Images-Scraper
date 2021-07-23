import urllib
import time
import requests
import json


class Pixabay:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.image_per_page = 200  # API rate limit

    def get_url(self, page):
        return 'https://pixabay.com/fr/images/search/'+self.search+'/?pagi='+str(page)

    def find_images(self):
        return self.driver.find_elements_by_xpath('//div/a/img')

    def next_page(self):
        if not self.driver.find_elements_by_xpath('//a[@class="button--1X-kp"]'):
            return False
        return True

    def scraper(self):
        while True:
            page = 1 if 'page' not in locals() else page+1
            self.driver.get(self.get_url(page))
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            res = self.find_images()

            for position, v in enumerate(res):
                image = res[position]

                try:
                    src = image.get_attribute("src")
                    if src is None:
                        continue

                    src = 'https:'+src if not src.startswith('https') and src.startswith('//') else src

                    parsed = urllib.parse.urlparse(src)
                    if urllib.parse.parse_qs(parsed.query):
                        continue

                    save_res = self.save_images(self.images_dl, self.files_path, src)
                    if not save_res:
                        continue

                    print("Image: %s / %s" % (self.total_images-self.images_remaining, self.total_images), end="\r")
                    self.images_remaining -= 1

                except Exception as e:
                    print('[ERROR]', e)

                if self.images_remaining <= 0:
                    return False

            if not self.next_page():
                break

    def api(self):
        print('API')
        if self.total_images % self.image_per_page > 1:
            pages = int((self.total_images / self.image_per_page)+1)
        else:
            pages = int(self.total_images / self.image_per_page)

        while True:
            for page in range(1, pages+1):
                response = requests.get('https://pixabay.com/api/?key='+self.api_key.pixabay+'&q='+self.search+'&page='+str(page)+'&per_page='+str(self.image_per_page)+'&image_type=photo&order=popular')
                content = json.loads(response.content.decode('utf-8'))['hits']
                total_hits = json.loads(response.content.decode('utf-8'))['totalHits']

                for doc in content:
                    try:
                        if 'webformatURL' in doc:
                            src = doc['webformatURL']
                        elif 'largeImageURL' in doc:
                            src = doc['largeImageURL']

                        save_res = self.save_images(self.images_dl, self.files_path, src)
                        if not save_res:
                            continue

                        print("Image: %s / %s" % (self.total_images-self.images_remaining, self.total_images), end="\r")
                        self.images_remaining -= 1

                    except Exception as e:
                        print(f'[ERROR] {e}')

                    if self.images_remaining <= 0:
                        return False

                if page == int(total_hits / self.image_per_page)+1:
                    return False
