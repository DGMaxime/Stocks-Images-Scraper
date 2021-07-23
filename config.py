import os
import yaml
import platform
import sys


class Dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Config:
    DRIVERS_FOLDER = './drivers'
    DRIVERS = {'chrome': 'chrome', 'mozilla': 'gecko', 'opera': 'opera'}
    CONFIG_FILES_PATH = './config_files'

    def __init__(self, args):
        if args.file:
            with open(os.path.join(self.CONFIG_FILES_PATH, args.file), "r") as f:
                c = Dotdict(yaml.safe_load(f))
                self.config = c.config
                self.config['stocks'] = [stock for stock, v in c.stocks.items() if v == True]
        else:
            if not args.search and not args.stocks:
                sys.exit('[ERROR] --search and --stocks arguments or --file argument are required')

            self.config = vars(args)

        self.driver_location = self.drivers_selection(self.config['browser'])
        self.api_key = Dotdict({
            'flickr': 'API_KEY',
            'pexels': 'API_KEY',
            'pixabay': 'API_KEY',
            'unsplash': 'API_KEY',
        })
        self.check_api_key()

    def check_api_key(self):
        for stock in self.config['stocks']:
            if self.config['api_first'] and stock in self.api_key and self.api_key[stock] == 'API_KEY':
                sys.exit('[ERROR] Please enter your API key for '+stock)

    def drivers_selection(self, browser):
        if platform.system() == 'Linux':
            driver_location = os.path.join(self.DRIVERS_FOLDER, self.DRIVERS[browser]+'driver_linux')
        elif platform.system() == 'Darwin':
            if platform.processor() != 'arm':
                driver_location = os.path.join(self.DRIVERS_FOLDER, self.DRIVERS[browser]+'driver_mac64')
            elif browser == 'chrome' or browser == 'gecko':
                driver_location = os.path.join(self.DRIVERS_FOLDER, self.DRIVERS[browser]+'driver_mac64_arm')
        elif platform.system() == 'Windows':
            driver_location = os.path.join(self.DRIVERS_FOLDER, self.DRIVERS[browser]+'driver.exe')
        else:
            sys.exit('[ERROR] Platform or driver not found')

        return driver_location
