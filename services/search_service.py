class SearchService:

    def build_driver_index(self, drivers):
        return {
            driver.driver_id: driver
            for driver in drivers
        }

    def build_trip_index(self, trips):
        return {
            trip.trip_id: trip
            for trip in trips
        }

    def build_zone_index(self, trips):
        zone_index = {}

        for trip in trips:
            zone_key = f"{trip.city}:{trip.pickup_zone}"

            if zone_key not in zone_index:
                zone_index[zone_key] = []

            zone_index[zone_key].append(trip)

        return zone_index

    def find_driver(self, driver_index, driver_id):
        return driver_index.get(driver_id)

    def find_trip(self, trip_index, trip_id):
        return trip_index.get(trip_id)

    def find_zone_trips(self, zone_index, city, zone):
        zone_key = f"{city}:{zone}"

        return zone_index.get(zone_key, [])