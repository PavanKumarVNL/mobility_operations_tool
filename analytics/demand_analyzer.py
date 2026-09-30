from collections import defaultdict


class DemandAnalyzer:

    def __init__(self, trips):
        self.trips = trips

    def trips_by_hour(self):

        hourly_demand = defaultdict(int)

        for trip in self.trips:
            hour = trip.request_time.hour
            hourly_demand[hour] += 1

        return dict(sorted(hourly_demand.items()))

    def peak_demand_hour(self):

        hourly_demand = self.trips_by_hour()

        if not hourly_demand:
            return None

        peak_hour = max(
            hourly_demand,
            key=hourly_demand.get
        )

        return {
            "hour": peak_hour,
            "trip_count": hourly_demand[peak_hour]
        }
        
    def zone_demand_by_time_slot(self, city, zone):

        time_slots = {
            "06-09": 0,
            "09-12": 0,
            "12-15": 0,
            "15-18": 0,
            "18-21": 0,
            "21-00": 0
        }
    
        for trip in self.trips:
        
            if trip.city != city or trip.pickup_zone != zone:
                continue
            
            hour = trip.request_time.hour
    
            if 6 <= hour < 9:
                time_slots["06-09"] += 1
            elif 9 <= hour < 12:
                time_slots["09-12"] += 1
            elif 12 <= hour < 15:
                time_slots["12-15"] += 1
            elif 15 <= hour < 18:
                time_slots["15-18"] += 1
            elif 18 <= hour < 21:
                time_slots["18-21"] += 1
            elif 21 <= hour < 24:
                time_slots["21-00"] += 1
    
        return time_slots