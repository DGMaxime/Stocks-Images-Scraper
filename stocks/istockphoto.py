import urllib


class Istockphoto:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_url(self, page):
        return 'https://www.istockphoto.com/fr/search/2/image?phrase='+self.search+'&page='+str(page)

    def find_images(self):
        return self.driver.find_elements_by_xpath('//a/figure/img')

    def next_page(self):
        if not self.driver.find_elements_by_css_selector('.PaginationRow-module__button___n_Toa'):
            return False
        return True

    def scraper(self):
        while True:
            page = 1 if 'page' not in locals() else page+1
            self.driver.get(self.get_url(page))
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
                    img_name = 'istockphoto-'+urllib.parse.parse_qs(parsed.query)['m'][0]+'-'+urllib.parse.parse_qs(parsed.query)['s'][0]

                    save_res = self.save_images(self.images_dl, self.files_path, src, img_name)
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
