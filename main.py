import json
import time
import requests
import logging

from bs4 import BeautifulSoup as bs

from db_manager import DataManager
from mailer import Mailer

CATEGORY_BOOKS = "books"
CATEGORY_GAMES = "games"
CATEGORY_SOFTWARE = "software"
CATEGORY = "games"




class Bundle():
    """
    Interesting Data
    ["tile_short_name"]
    ["tile_stamp"]
    ["product_url"]
    ["author"]
    ["detailed_marketing_blurb"]
    ["marketing_blurb"]
    """
    def __init__(self, title, author, description, url, stamp, category):
        self.title = title
        self.author = author
        self.description = description
        self.url = "https://www.humblebundle.com" + url
        self.stamp = stamp
        self.category = category
        
    def __str__(self):
        return self.title

def get_bundle_html(category):
    root_url = "https://www.humblebundle.com/"
    
    # Final URL leading to the category of bundles being requested
    url = root_url + category  
    
    n = 0
    while n < 3:
        try:
            # Attempt to get the bundles
            response = requests.get(url)
            
        except requests.ConnectionError:
            logging.error(f"Could not connect to HumbleBundle for {category}")
            
        except requests.HTTPError:
            logging.error(f"Request to {category} was unsuccessful: Status Code - {response.status_code}")
        
        except requests.Timeout:
            logging.error(f"Request timed out for {category}.")
        
        except:
            logging.error(f"An error occured requesting data for {category}.")
        
        finally:
            # If there is an error and a response isn't generated, 
            # sleep for 10 seconds and try again up to 3 times.
            if response is None or str(response.status_code) != '200':
                time.sleep(10)
                n += 1
            
        return response
    
def get_items_from_bundle_json(bundle_json, category):
    """Take the json data for the bundle and return a list of Bundles for that category

    Args:
        bundle_json (dict): json data representing the bundles scrapped from HumbleBundle
        category (str): a constant delcaring what kind of bundles are being parsed
    """
    try:
        bundles = bundle_json["data"][category]["mosaic"][0]["products"]
    except:
        logging.error(f"Could not parse json data for {category} bundles.")
    
    bundle_list = []
    for bundle in bundles:
        title = bundle['tile_short_name']
        author = bundle['author']
        description = bundle["detailed_marketing_blurb"]
        url = bundle["product_url"]
        stamp = bundle["tile_stamp"]
        
        bundle_list.append(Bundle(title, author, description, url, stamp, category))
        
    return bundle_list



def main():
    books_page = get_bundle_html(CATEGORY)
    book_soup = bs(books_page.text, 'html.parser')
    book_data = book_soup.find(id='landingPage-json-data').text
    book_json = json.loads(book_data)
    
    bundle_pull = get_items_from_bundle_json(book_json, CATEGORY)
    
    database = DataManager()
    database.connect()
    
    previous_bundles = database.get_bundle_list_by_category(CATEGORY)
    previous_bundles_cleaned = [i[0] for i in previous_bundles]
    
    new_bundles = []
    for bundle in bundle_pull:
        if bundle not in previous_bundles_cleaned:
            new_bundles.append(bundle)
    

    
    for bundle in new_bundles:
        database.add_bundle(bundle)
        
    database.close()



if __name__ == "__main__":
    logging.basicConfig(filename='humbleBundle.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s | %(levelname)s : %(message)s')
    main()