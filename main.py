import os
import sys
import argparse
from config import Config
from scraper_driver import ScraperDriver

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root+'/stocks')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', nargs='+', default='', required=False, help='Search keyword')
    parser.add_argument('--stocks', nargs='+', default='', required=False, help='Stocks to use')
    parser.add_argument('--images', type=int, default=150, required=False, help='Number of images')
    parser.add_argument('--file', type=str, default=False, required=False, help='Configuration file to use')
    parser.add_argument('--browser', type=str, default='chrome', required=False, help='Driver to use')
    parser.add_argument('--dir', type=str, default='./data', required=False, help='Save directory')
    parser.add_argument('--headless', action='store_true', required=False, help='Headless')
    parser.add_argument('--overwrite', action='store_true', required=False, help='Overwrite images')
    parser.add_argument('--api_first', action='store_true', required=False, help='Make API your first choice (recommended)')
    args = parser.parse_args()

    config = Config(args)
    sd = ScraperDriver(config)
    sd.launch_scraping()
