import requests
import json
import logging
import sys
import os
from bs4 import BeautifulSoup

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger('app')

def get_page(url):
    try:
        page = requests.get(url)
    except Exception as ex:
        logger.exception("failed to get page")
    else:
        if not page.ok:
            raise Exception("Page not OK")
        return page.content

def main():
    items_str = open("items.json").read()
    logger.debug(items_str)
    for item in json.loads(items_str):
        logger.debug(item)
        name = item.get("name")
        content = get_page(item.get("url"))
        logger.debug(content[:100])
        ele = BeautifulSoup(content, 'html.parser')
        focus = item.get("focus")
        for f_item in focus:
            ele = ele.find(f_item.get('ele'), f_item.get('selector'))
            
            if "contains" in f_item:
                if f_item.get("contains").lower() in ele.text.lower():
                    logger.info("check success")
                    os.system(f"telegram-send \"check for {name} passed\"")
                else:
                    logger.info("check failed")


if __name__ == "__main__":
    main()
