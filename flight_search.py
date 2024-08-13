import requests
import os
from dotenv import load_dotenv


load_dotenv()
AMADEUS_API_KEY = os.getenv('AMADEUS_API_KEY')
AMADEUS_API_SECRET = os.getenv('AMADEUS_API_SECRET')


class FlightSearch:

    def __init__(self):
        self.site_url = "https://test.api.amadeus.com/v1"
        self.authorization = None
        self.get_access_token(AMADEUS_API_KEY, AMADEUS_API_SECRET)
        self.origin_location = 'SGN'

    def get_access_token(self, AMADEUS_API_KEY, AMADEUS_API_SECRET):
        url = f"{self.site_url}/security/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {
            "grant_type": "client_credentials",
            "client_id": AMADEUS_API_KEY,
            "client_secret": AMADEUS_API_SECRET
        }
        response = requests.post(url=url, data=params, headers=headers)
        token = response.json()['access_token']
        self.authorization = f"Bearer {token}"

    def get_city_code(self, city_name):
        url = f"{self.site_url}/reference-data/locations/cities"
        params = {
            "keyword": city_name
        }
        headers = {
            "Authorization": self.authorization
        }
        response = requests.get(url=url, params=params, headers=headers)
        return response.json()

    def get_flight_offer(self, destination, max_price, search_date, non_stop="true"):
        url = f"https://test.api.amadeus.com/v2/shopping/flight-offers"
        headers = {
            "accept": "application/vnd.amadeus+json",
            "Authorization": self.authorization
        }
        params = {
            "originLocationCode": self.origin_location,
            "destinationLocationCode": destination,
            "departureDate": search_date,
            "adults": 1,
            "nonStop": non_stop,
            "currencyCode": "VND",
            "maxPrice": int(max_price),
            "max": 10
        }
        response = requests.get(url=url, params=params, headers=headers)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print("There was a problem with the flight search.\n"
                  "For details on status codes, check the API documentation:\n"
                  "https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api"
                  "-reference")
            print("Response body:", response.text)

        return response.json()

