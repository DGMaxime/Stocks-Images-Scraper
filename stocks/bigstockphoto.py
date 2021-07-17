
class Bigstockphoto():
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	def get_url(self, start):
		return 'https://www.bigstockphoto.com/fr/search/'+self.search+'/?start='+str(start)

	def find_images(self):
		 return self.driver.find_elements_by_xpath('//a/div/img')

	def next_page(self):
		if not self.driver.find_elements_by_css_selector('.search-pagination-next'):
			return False
		return True

	def scraper(self):
		while True:
			start = 0 if not 'res' in locals() else start+150
			self.driver.get(self.get_url(start))
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			res = self.find_images()

			for position, v in enumerate(res):
				image = res[position]

				try:
					src = image.get_attribute("src")
					if src is None:
						continue

					src = 'https:' + src if not src.startswith('https') and src.startswith('//') else src

					save_res = self.save_images(self.images_dl, self.files_path, src)
					if not save_res:
						continue

					print("Image: %s / %s"%(self.total_images-self.images_remaining, self.total_images), end="\r")
					self.images_remaining -= 1

				except Exception as e:
					print('[ERROR]', e)

				if self.images_remaining<=0:
					return False

			if not self.next_page():
				break
