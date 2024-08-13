from requests import ConnectTimeout

from flight_search import FlightSearch
from datetime import datetime, timedelta
import pandas as pd


class FlightData:

    def __init__(self):
        self.flight_search = FlightSearch()
        self.search_dates = []
        self.range_search = 30*6
        self.create_search_list()

    def create_search_list(self):
        """
        Initialize search range: default from now to next 6 months, with step of 10 days to reduce API call amount
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(days=self.range_search)
        while start_date <= end_date:
            self.search_dates.append(start_date.strftime('%Y-%m-%d'))
            start_date += timedelta(days=10)

    def get_best_price(self, destination, max_price):
        """
        Parse destination and expected price to search for flight with price lower than that.
        :param destination: Place you want to go to
        :param max_price: use as a filter to get only flight with price less than or equal to this price
        :return: best_offer (dict) including:
            - best_price: price that is lowest in the next 6 months and lower than max_price
            - earliest_flight: earliest flight date in the next 6 months at this price
            - latest_flight: latest flight date in the next 6 months at this price
            - carrier_code: list of carrier code offering this price
        """
        cheap_price = []
        carrier_code = []
        flight_at = []

        for day in self.search_dates:
            try:
                flight_response = self.flight_search.get_flight_offer(destination, max_price, day)
                if len(flight_response) > 0 and flight_response["meta"]['count'] > 0:
                    for data in flight_response['data']:
                        flight_at.append(data['itineraries'][0]['segments'][0]['departure']['at'])
                        carrier_code.append(data['itineraries'][0]['segments'][0]['carrierCode'])
                        price_offer = int(data['price']['total'].split(".")[0])
                        cheap_price.append(price_offer)

            except ConnectTimeout or ConnectionError:
                print("There is some connection error, please try again later.")
                continue

        if len(cheap_price) > 0:
            best_price_df = pd.DataFrame({
                'time_flight': flight_at,
                'carrier_code': carrier_code,
                'offer': cheap_price
            })

            best_price_df = best_price_df[best_price_df['offer'] == best_price_df['offer'].min()]

            best_offer = {
                'destination': destination,
                'best_price': best_price_df['offer'].min(),
                'earliest_flight': best_price_df['time_flight'].min(),
                'latest_flight': best_price_df['time_flight'].max(),
                'carrier_code': best_price_df['carrier_code'].unique()
            }

            return best_offer
        else:
            return None
