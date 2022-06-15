This branch is the development version of furaffinity-dl rewritten in python.

# FurAffinity Downloader

**furaffinity-dl** is a python script for batch downloading of galleries (and scraps/favourites) from furaffinity users users or your submissons!
It was written for preservation of culture, to counter the people nuking their galleries every once a while.

Supports all known submission types: images, text, flash and audio.

## Requirements

`pip3 install -r requirements.txt`

**The script currently only works with the "Modern" theme**

furaffinity-dl has only been tested only on Linux, however it should also work on Mac, Windows or any other platform that supports python.

## Usage

When downloading a folder make sure to put everything after **/folder/**, for example 123456/Folder-Name-Here instead of just 123456 (ref [#60](https://github.com/Xerbo/furaffinity-dl/issues/60)).

```help

usage: furaffinity-dl.py [-h] [--output OUTPUT] [--cookies COOKIES] [--ua UA] [--start START] [--stop STOP] [--dont-redownload]
                         [--interval INTERVAL] [--metadir METADIR]
                         [category] [username] [folder]

Downloads the entire gallery/scraps/favorites of a furaffinity user, or your submissions

positional arguments:
  category              the category to download, gallery/scraps/favorites
  username              username of the furaffinity user
  folder                name of the folder (full path, for instance 123456/Folder-Name-Here)

options:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        output directory
  --cookies COOKIES, -c COOKIES
                        path to a NetScape cookies file
  --ua UA, -u UA        Your browser's useragent, may be required, depending on your luck
  --start START, -s START
                        page number to start from
  --stop STOP, -S STOP  Page number to stop on. For favorites pages, specify the full URL after the username (1234567890/next).
  --dont-redownload, -d
                        Don't redownload files that have already been downloaded
  --interval INTERVAL, -i INTERVAL
                        delay between downloading pages
  --metadir METADIR, -m METADIR
                        directory to put meta files in

Examples:
 python3 furaffinity-dl.py gallery koul
 python3 furaffinity-dl.py -o koulsArt gallery koul
 python3 furaffinity-dl.py -o mylasFavs favorites mylafox

You can also log in to FurAffinity in a web browser and load cookies to download Age restricted content or Submissions:
 python3 furaffinity-dl.py -c cookies.txt gallery letodoesart
 python3 furaffinity-dl.py -c cookies.txt msg submissions

DISCLAIMER: It is your own responsibility to check whether batch downloading is allowed by FurAffinity terms of service and to abide by them.

```

You can also log in to download restricted content. To do that, log in to FurAffinity in your web browser, export cookies to a file from your web browser in Netscape format (there are extensions to do that [for Firefox](https://addons.mozilla.org/en-US/firefox/addon/ganbo/) and [for Chrome based browsers](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg)), you can then pass them to the script with the `-c` flag, like this (you may also have to provide your user agent):

`python3 furaffinity-dl.py -c cookies.txt -u 'Mozilla/5.0 ....' gallery letodoesart`

## TODO

- Download user profile information.
- "Classic" theme support
- Login without having to export cookies

## Disclaimer

It is your own responsibility to check whether batch downloading is allowed by FurAffinity's terms of service and to abide by them. For further disclaimers see LICENSE.
