import requests
import json


class Pexels:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.image_per_page = 80  # API rate limit

    def get_url(self):
        return 'https://www.pexels.com/search/'+self.search+'/'

    def find_images(self):
        return self.driver.find_elements_by_xpath('//article/a/img')

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
                        src = image.get_attribute("data-large-src")
                        if src is None:
                            src = image.get_attribute("srcset")
                            if src is None:
                                continue

                    src = 'https:'+src if not src.startswith('https') and src.startswith('//') else src

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
                response = requests.get('https://api.pexels.com/v1/search?query='+self.search+'&page='+str(page)+'&per_page='+str(self.image_per_page), headers={'Authorization': self.api_key.pexels, 'User-Agent': 'Mozilla/5.0'})
                content = json.loads(response.content.decode('utf-8'))['photos']
                total_results = json.loads(response.content.decode('utf-8'))['total_results']

                for doc in content:
                    try:
                        if 'medium' in doc['src']:
                            src = doc['src']['medium']
                        elif 'large' in doc['src']:
                            src = doc['src']['large']
                        elif 'original' in doc['src']:
                            src = doc['src']['original']

                        save_res = self.save_images(self.images_dl, self.files_path, src)
                        if not save_res:
                            continue

                        print("Image: %s / %s" % (self.total_images-self.images_remaining, self.total_images), end="\r")
                        self.images_remaining -= 1

                    except Exception as e:
                        print(f'[ERROR] {e}')

                    if self.images_remaining <= 0:
                        return False

                if self.image_per_page * page < total_results or len(content) == 0:
                    return False
