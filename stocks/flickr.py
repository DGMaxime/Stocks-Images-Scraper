import os
import time
import re
import requests
import json

class Flickr():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.image_width = ['c', 'z', 'w', 'n', 'm', 'q']
        self.image_per_page = 500  # API rate limit

    def get_url(self):
        return 'https://www.flickr.com/search/?text='+self.search
        time.sleep(6)

    def find_images(self):
        return self.driver.find_elements_by_css_selector('.photo-list-photo-view')

    def load_more_results(self):
        # Click on "Load more results" button
        if self.driver.find_elements_by_xpath('//div[@class="infinite-scroll-load-more"]'):
            self.driver.find_elements_by_xpath('//div[@class="infinite-scroll-load-more"]/button')[0].click()

    def remove_cookies_banner(self):
        while True:
            if self.driver.find_elements_by_css_selector('.truste_box_overlay'):
                self.driver.execute_script("""
                    var el = document.getElementsByClassName("truste_box_overlay")[0];
                    el.parentNode.removeChild(el);
                    var el = document.getElementsByClassName("truste_overlay")[0];
                    el.parentNode.removeChild(el);
                """)
                return False
            time.sleep(1)

    def scraper(self):
        print('SCRAPER')
        self.driver.get(self.get_url())
        self.remove_cookies_banner()

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            res = self.find_images()
            res = res if not 'last_position' in locals() else res[last_position:]
            last_position = len(res)

            for position, v in enumerate(res):
                image = res[position]

                try:
                    src = image.get_attribute("style")
                    s = re.search('url\("(.*)"\);', src).group(1)
                    src = 'https:'+s if not s.startswith('https') and s.startswith('//') else src

                    if src is None:
                        continue

                    filename, extension = os.path.splitext(src)
                    for w in self.image_width:
                        src = filename[:-2]+'_'+w+extension
                        save_res = self.save_images(self.images_dl, self.files_path, src)
                        if save_res:
                            break

                    print("Image: %s / %s"%(self.total_images-self.images_remaining, self.total_images), end="\r")
                    self.images_remaining -= 1

                except Exception as e:
                    print('[ERROR]', e)

                if self.images_remaining<=0:
                    return False

            self.load_more_results()

    def api(self):
        print('API')
        if self.total_images%self.image_per_page>1:
            pages = int((self.total_images/self.image_per_page)+1)
        else:
            pages = int(self.total_images/self.image_per_page)

        while True:
            for page in range(1, pages+1):
                response = requests.get(
                    'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key='+self.api_key.flickr+'&format=json&nojsoncallback=1&sort=relevance&text='+self.search+'&extras=url_m&page='+str(page)+'&per_page='+str(
                        self.image_per_page))

                content = json.loads(response.content.decode('utf-8'))['photos']['photo']
                total_pages = json.loads(response.content.decode('utf-8'))['photos']['pages']
                actual_page = json.loads(response.content.decode('utf-8'))['photos']['page']

                for doc in content:

                    try:
                        if 'url_m' in doc:
                            src = doc['url_m']
                            save_res = self.save_images(self.images_dl, self.files_path, src)
                            if not save_res:
                                continue

                            print("Image: %s / %s"%(self.total_images-self.images_remaining, self.total_images), end="\r")
                            self.images_remaining -= 1

                    except Exception as e:
                        print('[ERROR]', e)

                    if self.images_remaining<=0:
                        return False

                if actual_page>total_pages or len(content)==0:
                    return False
