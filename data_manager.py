import requests
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()
SHEETY_ACCOUNT = os.getenv('SHEETY_ACCOUNT')
SHEETY_AUTHENTICATION = os.getenv('SHEETY_AUTHENTICATION')


class DataManager:

    def __init__(self):
        self.headers = {
            "Authorization": SHEETY_AUTHENTICATION
        }
        self.main_url = f"https://api.sheety.co/{SHEETY_ACCOUNT}/flightPriceTracking/price"

    def get_location_info(self):
        """
        Use Sheety API to extract list of cities in Google Sheet to search for lowest price offer
        """
        response = requests.get(url=self.main_url, headers=self.headers)
        return pd.DataFrame(response.json()['price'])

    def update_lowest_price(self, object_id, lowest_price, search_price, earliest_day, latest_day, carrier_code):
        """
        After calling API, updating the sheet so next time the code run,
        only alert if the price is lower than the current lowest price
        :param object_id: id to update
        :param lowest_price: the lowest price got from API
        :param search_price: the lowest price - VND 10,000
        :param earliest_day: earliest flight date at the lowest_price
        :param latest_day: latest flight date at the lowest_price
        :param carrier_code: carrier code offering the lowest price
        :return: Update the Google Sheet
        """
        url = f"{self.main_url}/{object_id}"
        body = {
            "price": {
                "searchPrice": search_price,
                "lowestPrice": lowest_price,
                "from": earliest_day,
                "to": latest_day,
                "carrierCode": carrier_code
            }
        }
        response = requests.put(url=url, headers=self.headers, json=body)

        return response
