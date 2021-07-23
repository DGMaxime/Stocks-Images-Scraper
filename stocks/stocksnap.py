import requests
import json


class Stocksnap:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_url(self):
        return 'https://stocksnap.io/search/'+self.search+'/'

    def find_images(self):
        return self.driver.find_elements_by_xpath('//div[@class="photo-grid-item"]/a/img')

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

                    save_res = self.save_images(self.images_dl, self.files_path, src)
                    if not save_res:
                        continue

                    print("Image: %s / %s" % (self.total_images-self.images_remaining, self.total_images), end="\r")
                    self.images_remaining -= 1

                except Exception as e:
                    print('[ERROR]', e)

                if self.images_remaining <= 0:
                    return False
