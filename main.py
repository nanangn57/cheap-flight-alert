from data_manager import DataManager
from flight_data import FlightData
from notification_manager import NotificationManager

if __name__ == "__main__":

    data_manager = DataManager()
    flight_data = FlightData()
    email_notify = NotificationManager()

    offer_avail = False

    city_search = data_manager.get_location_info()
    content = f"Low price alert! In the next 6 months, there are some good flight deals:\n\n"

    for index, row in city_search.iterrows():
        best_offer = flight_data.get_best_price(row['iataCode'], row['searchPrice'])
        if best_offer:
            earliest_day = best_offer['earliest_flight'][:10]
            latest_day = best_offer['latest_flight'][:10]
            formatted_price = "{:,}".format(best_offer['best_price'])
            content += f"Flight from Saigon to {row['city']} only at VND {formatted_price} " \
                       f"starting from {earliest_day} to {latest_day}.\n\n"
            offer_avail = True
            print(f"Finish getting best offer to {row['city']}: {best_offer}")
            data_manager.update_lowest_price(object_id=row['id'],
                                             search_price=str(best_offer['best_price'] - 10000),
                                             lowest_price=formatted_price,
                                             earliest_day=earliest_day, latest_day=latest_day,
                                             carrier_code=','.join(best_offer['carrier_code']))
        else:
            print(f"No best offer to {row['city']}")

    if offer_avail:
        content += "For more detail, visit this file: https://shorturl.at/aG4Ui"
        email_notify.send_email(content)
    else:
        print("There is no good offer in the next 6 months")
