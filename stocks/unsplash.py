import requests
import json


class Unsplash:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.image_per_page = 30  # API rate limit

    def get_url(self):
        return 'https://unsplash.com/s/photos/'+self.search

    def find_images(self):
        return self.driver.find_elements_by_xpath('//div/div/img')

    def scraper(self):
        self.driver.get(self.get_url())
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            res = self.find_images()
            res = res if 'last_position' not in locals() else res[last_position:]
            last_position = len(res)

            for position, v in enumerate(res):
                image = res[position]

                try:
                    src = image.get_attribute("src")
                    if src is None:
                        src = image.get_attribute("srcset")
                        src = src.split(',')[-1].split()[0].strip()

                    save_res = self.save_images(self.images_dl, self.files_path, src)
                    if not save_res:
                        continue

                    print("Image: %s / %s" % (self.total_images-self.images_remaining, self.total_images), end="\r")
                    self.images_remaining -= 1

                except Exception as e:
                    print('[ERROR]', e)

                if self.images_remaining <= 0:
                    return False

    def api(self):
        print('API')
        if self.total_images % self.image_per_page > 1:
            pages = int((self.total_images / self.image_per_page)+1)
        else:
            pages = int(self.total_images / self.image_per_page)

        while True:
            for page in range(1, pages+1):
                response = requests.get('https://api.unsplash.com/search/photos?query='+self.search+'&page='+str(page)+'&per_page='+str(self.image_per_page)+'&client_id='+self.api_key.unsplash)
                content = json.loads(response.content.decode('utf-8'))['results']
                total_pages = json.loads(response.content.decode('utf-8'))['total_pages']

                for doc in content:
                    try:
                        if 'small' in doc['urls']:
                            src = doc['urls']['small']
                        if 'regular' in doc['urls']:
                            src = doc['urls']['regular']
                        elif 'full' in doc['urls']:
                            src = doc['urls']['full']
                        elif 'raw' in doc['urls']:
                            src = doc['urls']['raw']

                        save_res = self.save_images(self.images_dl, self.files_path, src, doc['id'])
                        if not save_res:
                            continue

                        print("Image: %s / %s" % (self.total_images-self.images_remaining, self.total_images), end="\r")
                        self.images_remaining -= 1

                    except Exception as e:
                        print(f'[ERROR] {e}')

                    if self.images_remaining <= 0:
                        return False

                if page == total_pages:
                    return False
