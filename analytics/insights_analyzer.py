class InsightsAnalyzer:

    def __init__(
        self,
        zone_metrics,
        hourly_demand,
        cancellation_summary,
        utilization_metrics,
        anomaly_summary
    ):
        self.zone_metrics = zone_metrics
        self.hourly_demand = hourly_demand
        self.cancellation_summary = cancellation_summary
        self.utilization_metrics = utilization_metrics
        self.anomaly_summary = anomaly_summary

    def highest_cancellation_zone(self):

        if not self.zone_metrics:
            return None

        zone = max(
            self.zone_metrics,
            key=lambda item: item["cancellation_rate"]
        )

        return {
            "city": zone["city"],
            "zone": zone["zone"],
            "cancellation_rate": zone["cancellation_rate"]
        }

    def peak_demand_period(self):

        if not self.hourly_demand:
            return None

        peak_hour = max(
            self.hourly_demand,
            key=self.hourly_demand.get
        )

        return {
            "hour": peak_hour,
            "trip_count": self.hourly_demand[peak_hour]
        }

    def low_utilization_count(self):

        return sum(
            1
            for driver in self.utilization_metrics
            if driver["classification"] == "Low"
        )

    def largest_cancellation_category(self):

        by_reason = self.cancellation_summary["by_reason"]

        if not by_reason:
            return None

        reason = max(
            by_reason,
            key=by_reason.get
        )

        return {
            "reason": reason,
            "count": by_reason[reason]
        }

    def total_anomaly_count(self):

        trip_anomalies = self.anomaly_summary["trip_anomalies"]
        driver_anomalies = self.anomaly_summary["driver_anomalies"]

        return len(trip_anomalies) + len(driver_anomalies)

    def generate_insights(self):

        return {
            "highest_cancellation_zone":
            self.highest_cancellation_zone(),

            "peak_demand_period":
            self.peak_demand_period(),

            "low_utilization_count":
            self.low_utilization_count(),

            "largest_cancellation_category":
            self.largest_cancellation_category(),

            "total_anomaly_count":
            self.total_anomaly_count()
        }