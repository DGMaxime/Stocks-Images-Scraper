class Stockvault:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_url(self, page):

        return 'https://www.stockvault.net/free-photos/'+self.search+'/?c=120&p='+str(page)

    def find_images(self):
        return self.driver.find_elements_by_xpath('//div/a[@class="preview"]/img')

    def next_page(self):
        if self.driver.find_elements_by_css_selector('.allmargin-lg'):
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

                    src = src.replace('/.', 'https://www.stockvault.net') if not src.startswith('https') and src.startswith('/.') else src
                    img_name = 'stockvault-'+src.split('/')[-2]

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
