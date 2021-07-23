import requests
import json


class Pinterest:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.image_per_page = 200  # API rate limit

    def get_url(self):
        return 'https://www.pinterest.fr/search/pins/?q='+self.search

    def find_images(self):
        return self.driver.find_elements_by_xpath('//img')

    def load_more_results(self):
        # Click on "Load more results" button
        if self.driver.find_elements_by_xpath('//div[@class="infinite-scroll-load-more"]'):
            self.driver.find_elements_by_xpath('//div[@class="infinite-scroll-load-more"]/button')[0].click()

    def remove_cookies_banner(self):
        if self.driver.find_elements_by_xpath('//div[@data-test-id="full-banner"]'):
            self.driver.execute_script("""
                var el = document.querySelectorAll('[data-test-id="full-banner"]')[0];
                el.parentNode.removeChild(el);
                var el = document.querySelectorAll('[data-test-id="giftWrap"]')[0];
                el.parentNode.removeChild(el);
            """)

    def scraper(self):
        self.driver.get(self.get_url())
        self.remove_cookies_banner()

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.remove_cookies_banner()

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
            bookmarks = ''
            for page in range(1, pages+1):
                response = requests.get('https://nl.pinterest.com/resource/SearchResource/get/?source_url=/&data={"options":{"query":"'+self.search+'","page_size":'+str(self.image_per_page)+', "bookmarks":["'+bookmarks+'"]},"context":{}}')
                content = json.loads(response.content.decode('utf-8'))['resource_response']['data']
                bookmarks = json.loads(response.content.decode('utf-8'))['resource']['options']['bookmarks'][0]

                for doc in content:
                    try:
                        if '474x' in doc['images']:
                            src = doc['images']['474x']['url']
                        elif '736x' in doc['images']:
                            src = doc['images']['736x']['url']
                        elif 'orig' in doc['images']:
                            src = doc['images']['orig']['url']

                        save_res = self.save_images(self.images_dl, self.files_path, src)
                        if not save_res:
                            continue

                        print("Image: %s / %s" % (self.total_images-self.images_remaining, self.total_images), end="\r")
                        self.images_remaining -= 1

                    except Exception as e:
                        print(f'[ERROR] {e}')

                    if self.images_remaining <= 0:
                        return False

                if bookmarks == '-end-':
                    return False
