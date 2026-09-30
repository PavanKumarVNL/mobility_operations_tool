class AnomalyDetector:

    def __init__(
        self,
        trips,
        drivers,
        driver_metrics,
        utilization_metrics
    ):
        self.trips = trips
        self.drivers = drivers
        self.driver_metrics = driver_metrics
        self.utilization_metrics = utilization_metrics

    def detect_trip_anomalies(self):

        anomalies = []

        driver_ids = {
            driver.driver_id
            for driver in self.drivers
        }

        for trip in self.trips:

            # Negative fare
            if trip.fare < 0:
                anomalies.append({
                    "trip_id": trip.trip_id,
                    "issue": "Negative fare"
                })

            # Zero distance
            if trip.distance_km == 0:
                anomalies.append({
                    "trip_id": trip.trip_id,
                    "issue": "Zero distance"
                })

            # Missing pickup timestamp
            if trip.pickup_time is None:
                anomalies.append({
                    "trip_id": trip.trip_id,
                    "issue": "Missing pickup timestamp"
                })

            # Drop time before pickup time
            if (
                trip.pickup_time is not None
                and trip.drop_time is not None
                and trip.drop_time < trip.pickup_time
            ):
                anomalies.append({
                    "trip_id": trip.trip_id,
                    "issue": "Drop time before pickup time"
                })

            # Unknown driver
            if trip.driver_id not in driver_ids:
                anomalies.append({
                    "trip_id": trip.trip_id,
                    "issue": "Unknown driver"
                })

            # Unusually high fare
            if trip.fare > 2000:
                anomalies.append({
                    "trip_id": trip.trip_id,
                    "issue": "Unusually high fare"
                })

            # Extremely long trip duration
            duration = trip.calculate_duration()

            if duration is not None and duration > 180:
                anomalies.append({
                    "trip_id": trip.trip_id,
                    "issue": "Extremely long trip duration"
                })

        return anomalies

    def detect_driver_anomalies(self):

        anomalies = []

        for metrics in self.driver_metrics:

            driver_id = metrics["driver_id"]

            # High cancellation rate
            total_trips = metrics["total_trips"]
            cancelled_trips = metrics["cancelled_trips"]

            cancellation_rate = (
                cancelled_trips / total_trips * 100
                if total_trips > 0
                else 0
            )

            if cancellation_rate > 30:
                anomalies.append({
                    "driver_id": driver_id,
                    "issue": "High cancellation rate"
                })

            # Unusually high trip count
            if total_trips > 30:
                anomalies.append({
                    "driver_id": driver_id,
                    "issue": "Unusually high trip count"
                })

        for metrics in self.utilization_metrics:

            if metrics["utilization"] < 30:
                anomalies.append({
                    "driver_id": metrics["driver_id"],
                    "issue": "Low utilization"
                })

        for driver in self.drivers:

            if driver.rating < 3:
                anomalies.append({
                    "driver_id": driver.driver_id,
                    "issue": "Low rating"
                })

        return anomalies

    def get_all_anomalies(self):

        return {
            "trip_anomalies": self.detect_trip_anomalies(),
            "driver_anomalies": self.detect_driver_anomalies()
        }