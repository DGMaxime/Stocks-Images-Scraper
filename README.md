# Stocks Images Scraper

Stocks Images Scraper allows you to scrape or use the API of the most popular stock images.

## Stocks Images

| Banque d'images |  Scraping |  API  |
|------|---|---|
|  Adobe Stock    |  Available |   |
|  Bigstock    | Available  |   |
|  Depositphotos   |  Available |   |
|  Flickr   |  Available | Available  |
|  iStockphoto   | Available  |   |
|  Pexels   | Available  | Available  |
|  Pinterest   | Available  |   |
|  Pixabay   |  Available | Available  |
|  Shutterstock   | Available  |   |
|  Stock Photos   | Available  |   |
|  StockSnap   | Available  |   |
|  Stockvault   | Available  |   |
|  Unsplash   | Available  | Available  |

## How to use
Either by launching a command line with the correct arguments.
```
python main.py --search apple "orange juice" strawberry --stocks shutterstock deposit --images 500
```

Or by using a configuration file (see the config_example.yml file in the config_files folder).
```
python main.py --file config_example.yml
```

## Parameters
| Argument |  Type |  Required  |
|------|---|---|
|  --search    |  string | required if --file not filled in  |
|  --stocks    | string  |  required if --file not filled in |
|  --images   |  int |  False |
|  --file   |  string | False  |
|  --browser   | string  |  False |
|  --dir   | string  | False  |
|  --headless   | bool  |  False |
|  --overwrite   |  bool | False  |
|  --api_first   | bool  | False  |
