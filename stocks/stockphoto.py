import re


class Stockphoto:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_url(self):
        return 'https://stockphoto.com/search.php?q='+self.search

    def find_images(self):
        return self.driver.find_elements_by_xpath('//*[@class="results-item"]')

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
                    img_name = re.search('/photo/([^/]+)(.*)/', image.get_attribute("data-ng-href")).group(1)

                    src = image.find_element_by_xpath('.//img').get_attribute("src")
                    if src is None:
                        src = image.get_attribute("data-ng-src")

                    save_res = self.save_images(self.images_dl, self.files_path, src, img_name)
                    if not save_res:
                        continue

                    print("Image: %s / %s" % (self.total_images-self.images_remaining, self.total_images), end="\r")
                    self.images_remaining -= 1

                except Exception as e:
                    print('[ERROR]', e)

                if self.images_remaining <= 0:
                    return False
