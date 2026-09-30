from collections import defaultdict


class IdleAnalyzer:

    def __init__(self, trips, threshold_minutes=30):
        self.trips = trips
        self.threshold_minutes = threshold_minutes

    def find_idle_gaps(self):

        trips_by_driver = defaultdict(list)

        # Group completed trips by driver
        for trip in self.trips:
            if trip.is_completed():
                trips_by_driver[trip.driver_id].append(trip)

        results = []

        for driver_id, driver_trips in trips_by_driver.items():

            # Sort chronologically by pickup time
            driver_trips = [
                trip for trip in driver_trips
                if trip.pickup_time is not None
            ]
            
            driver_trips.sort(
                key=lambda trip: trip.pickup_time
            )

            for i in range(len(driver_trips) - 1):

                previous_trip = driver_trips[i]
                next_trip = driver_trips[i + 1]

                # Skip trips with missing timestamps
                if (
                    previous_trip.drop_time is None
                    or next_trip.pickup_time is None
                ):
                    continue

                idle_minutes = (
                    next_trip.pickup_time -
                    previous_trip.drop_time
                ).total_seconds() / 60

                # Ignore overlapping trips
                if idle_minutes <= 0:
                    continue

                if idle_minutes >= self.threshold_minutes:

                    results.append({
                        "driver_id": driver_id,
                        "previous_trip": previous_trip.trip_id,
                        "next_trip": next_trip.trip_id,
                        "idle_minutes": idle_minutes
                    })

        # Largest idle gaps first
        results.sort(
            key=lambda item: item["idle_minutes"],
            reverse=True
        )

        return results