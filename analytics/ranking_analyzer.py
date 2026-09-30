import heapq


class RankingAnalyzer:

    def top_k(self, items, key_function, k):

        if k <= 0:
            return []

        heap = []

        for index, item in enumerate(items):

            value = key_function(item)

            # index acts as a tie-breaker
            heap_item = (value, index, item)

            if len(heap) < k:
                heapq.heappush(heap, heap_item)

            elif value > heap[0][0]:
                heapq.heapreplace(
                    heap,
                    heap_item
                )

        heap.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            item
            for value, index, item in heap
        ]

    def top_drivers_by_completed_trips(
        self,
        driver_metrics,
        k
    ):
        return self.top_k(
            driver_metrics,
            lambda driver: driver["completed_trips"],
            k
        )

    def top_drivers_by_revenue(
        self,
        driver_metrics,
        k
    ):
        return self.top_k(
            driver_metrics,
            lambda driver: driver["revenue"],
            k
        )

    def top_zones_by_demand(
        self,
        zone_metrics,
        k
    ):
        return self.top_k(
            zone_metrics,
            lambda zone: zone["total_trips"],
            k
        )

    def top_zones_by_cancellations(
        self,
        zone_metrics,
        k
    ):
        return self.top_k(
            zone_metrics,
            lambda zone: zone["cancelled_trips"],
            k
        )
        
    def top_riders_by_trip_count(self, trips, k):
        rider_counts = {}

        for trip in trips:
            rider_id = trip.rider_id
            rider_counts[rider_id] = rider_counts.get(rider_id, 0) + 1

        rider_metrics = [
            {
                "rider_id": rider_id,
                "trip_count": trip_count
            }
            for rider_id, trip_count in rider_counts.items()
        ]

        return self.top_k(
            rider_metrics,
            lambda rider: rider["trip_count"],
            k
        )
        
    def lowest_cancellation_drivers(self, driver_metrics, k):
        return self.top_k(
            driver_metrics,
            lambda driver: -driver["cancellation_rate"],
            k
        )
    
    
    def highest_utilization_drivers(self, driver_metrics, utilization_metrics, k):
    
        utilization_by_driver = {
            item["driver_id"]: item["utilization"]
            for item in utilization_metrics
        }
    
        drivers_with_utilization = []
    
        for driver in driver_metrics:
            driver_copy = driver.copy()
            driver_copy["utilization"] = utilization_by_driver.get(
                driver["driver_id"], 0
            )
            drivers_with_utilization.append(driver_copy)
    
        return self.top_k(
            drivers_with_utilization,
            lambda driver: driver["utilization"],
            k
        )