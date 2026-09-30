class DriverAnalyzer:

    def __init__(self, drivers, trips):
        self.drivers = drivers
        self.trips = trips

    def get_driver_metrics(self, driver_id):

        driver_trips = [
            trip for trip in self.trips
            if trip.driver_id == driver_id
        ]

        completed_trips = [
            trip for trip in driver_trips
            if trip.is_completed()
        ]

        cancelled_trips = [
            trip for trip in driver_trips
            if trip.is_cancelled()
        ]

        revenue = sum(
            trip.fare for trip in completed_trips
        )

        average_fare = (
            revenue / len(completed_trips)
            if completed_trips else 0
        )

        average_distance = (
            sum(trip.distance_km for trip in completed_trips)
            / len(completed_trips)
            if completed_trips else 0
        )

        total_distance = sum(
            trip.distance_km for trip in completed_trips
        )

        average_fare_per_km = (
            revenue / total_distance
            if total_distance > 0 else 0
        )

        total_trips = len(driver_trips)

        completion_rate = (
            len(completed_trips) / total_trips * 100
            if total_trips > 0 else 0
        )

        cancellation_rate = (
            len(cancelled_trips) / total_trips * 100
            if total_trips > 0 else 0
        )

        return {
            "driver_id": driver_id,
            "total_trips": total_trips,
            "completed_trips": len(completed_trips),
            "cancelled_trips": len(cancelled_trips),
            "completion_rate": completion_rate,
            "cancellation_rate": cancellation_rate,
            "revenue": revenue,
            "average_fare": average_fare,
            "average_distance": average_distance,
            "average_fare_per_km": average_fare_per_km
        }

    def get_all_driver_metrics(self):

        driver_metrics = []

        for driver in self.drivers:

            metrics = self.get_driver_metrics(
                driver.driver_id
            )

            metrics["driver_name"] = driver.driver_name
            metrics["city"] = driver.city

            driver_metrics.append(metrics)

        return driver_metrics
    def get_operational_attention_drivers(
        self,
        utilization_metrics,
        cancellation_threshold=30,
        utilization_threshold=30
    ):

        utilization_by_driver = {
            item["driver_id"]: item["utilization"]
            for item in utilization_metrics
        }

        attention_drivers = []

        for driver in self.drivers:

            metrics = self.get_driver_metrics(driver.driver_id)

            reasons = []

            if metrics["cancellation_rate"] > cancellation_threshold:
                reasons.append("High cancellation rate")

            utilization = utilization_by_driver.get(
                driver.driver_id,
                0
            )

            if utilization < utilization_threshold:
                reasons.append("Low utilization")

            if driver.rating < 3:
                reasons.append("Low rating")

            if reasons:
                attention_drivers.append({
                    "driver_id": driver.driver_id,
                    "driver_name": driver.driver_name,
                    "city": driver.city,
                    "reasons": reasons
                })

        return attention_drivers
    
    def peak_demand_hour(self):
        hourly_demand = self.trips_by_hour()
    
        if not hourly_demand:
            return (0, 0)
    
        peak_hour = max(hourly_demand, key=hourly_demand.get)
    
        return (peak_hour, hourly_demand[peak_hour])