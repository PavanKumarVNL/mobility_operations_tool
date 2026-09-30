class Zone:
    def __init__(self, city, zone_name):
        self.city = city
        self.zone_name = zone_name
        self.trips = []

    def add_trip(self, trip):
        self.trips.append(trip)

    def get_trip_count(self):
        return len(self.trips)