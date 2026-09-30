from flask import Flask, render_template, request

from services.validation_service import DataValidator
from services.data_loader import DataLoader
from services.search_service import SearchService

from analytics.trip_analyzer import TripAnalyzer
from analytics.driver_analyzer import DriverAnalyzer
from analytics.zone_analyzer import ZoneAnalyzer
from analytics.ranking_analyzer import RankingAnalyzer
from analytics.demand_analyzer import DemandAnalyzer
from analytics.idle_analyzer import IdleAnalyzer
from analytics.cancellation_analyzer import CancellationAnalyzer
from analytics.utilization_analyzer import UtilizationAnalyzer

from analytics.anomaly_detector import AnomalyDetector
from analytics.insights_analyzer import InsightsAnalyzer




app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "GET":
        return render_template(
            "index.html",
            anomaly_summary={
                "trip_anomalies": [],
                "driver_anomalies": []
            }
        )

    drivers_file = request.files.get("drivers")
    trips_file = request.files.get("trips")
    activity_file = request.files.get("activity")

    if not drivers_file or not trips_file or not activity_file:
        return render_template(
            "index.html",
            error="Please upload all three CSV files.",
            anomaly_summary={
                "trip_anomalies": [],
                "driver_anomalies": []
            }
        )

    validator = DataValidator()

    drivers_path = "data/uploaded_drivers.csv"
    trips_path = "data/uploaded_trips.csv"
    activity_path = "data/uploaded_activity.csv"

    drivers_file.save(drivers_path)
    trips_file.save(trips_path)
    activity_file.save(activity_path)

    driver_errors = validator.validate_file(
        drivers_path,
        "drivers"
    )

    trip_errors = validator.validate_file(
        trips_path,
        "trips"
    )

    # trip_errors.extend(
    #     validator.validate_trip_driver_references(
    #         trips_path,
    #         drivers_path
    #     )
    # )

    activity_errors = validator.validate_file(
        activity_path,
        "activity"
    )

    errors = (
        driver_errors
        + trip_errors
        + activity_errors
    )

    if errors:
        return render_template(
            "index.html",
            errors=errors,
            anomaly_summary={
                "trip_anomalies": [],
                "driver_anomalies": []
            }
        )

    # -------------------------
    # LOAD DATA
    # -------------------------

    loader = DataLoader()

    drivers = loader.load_drivers(
        drivers_path
    )

    trips = loader.load_trips(
        trips_path
    )

    activities = loader.load_activity(
        activity_path
    )

    # -------------------------
    # BUILD INDEXES
    # -------------------------
    
    active_driver_count = sum(
        1 for driver in drivers
        if driver.is_active()
    )

    search_service = SearchService()

    driver_index = search_service.build_driver_index(
        drivers
    )

    trip_index = search_service.build_trip_index(
        trips
    )

    zone_index = search_service.build_zone_index(
        trips
    )
    search_result = None

    search_query = request.form.get("search_query")

    if search_query:
        driver = search_service.find_driver(
            driver_index,
            search_query
        )

        if driver:
            search_result = {
                "type": "Driver",
                "data": driver.get_profile()
            }
        else:
            trip = search_service.find_trip(
                trip_index,
                search_query
            )

            if trip:
                search_result = {
                    "type": "Trip",
                    "data": {
                        "trip_id": trip.trip_id,
                        "driver_id": trip.driver_id,
                        "rider_id": trip.rider_id,
                        "city": trip.city,
                        "pickup_zone": trip.pickup_zone,
                        "drop_zone": trip.drop_zone,
                        "status": trip.status,
                        "fare": trip.fare,
                        "distance_km": trip.distance_km
                    }
                }

    # -------------------------
    # BASIC ANALYTICS
    # -------------------------

    trip_analyzer = TripAnalyzer(trips)

    trip_summary = trip_analyzer.get_summary()

    driver_analyzer = DriverAnalyzer(
        drivers,
        trips
    )

    driver_metrics = (
        driver_analyzer.get_all_driver_metrics()
    )

    zone_analyzer = ZoneAnalyzer(trips)

    zone_metrics = (
        zone_analyzer.get_all_zone_metrics()
    )

    # -------------------------
    # DAY 3: TOP-K
    # -------------------------

    ranking_analyzer = RankingAnalyzer()

    top_drivers_by_trips = (
        ranking_analyzer.top_drivers_by_completed_trips(
            driver_metrics,
            10
        )
    )

    top_drivers_by_revenue = (
        ranking_analyzer.top_drivers_by_revenue(
            driver_metrics,
            10
        )
    )

    top_zones_by_demand = (
        ranking_analyzer.top_zones_by_demand(
            zone_metrics,
            10
        )
    )

    top_zones_by_cancellations = (
        ranking_analyzer.top_zones_by_cancellations(
            zone_metrics,
            10
        )
    )

    # -------------------------
    # DAY 3: UTILIZATION
    # -------------------------

    activity_analyzer = UtilizationAnalyzer(
        activities,
        high_threshold=70,
        medium_threshold=40
    )

    utilization_metrics = (
        activity_analyzer.get_all_driver_utilization()
    )

    
    # -------------------------
    # DAY 3: PEAK DEMAND
    # -------------------------

    demand_analyzer = DemandAnalyzer(trips)

    hourly_demand = (
        demand_analyzer.trips_by_hour()
    )

    peak_demand = (
        demand_analyzer.peak_demand_hour()
    )

    # -------------------------
    # DAY 3: IDLE TIME
    # -------------------------

    idle_analyzer = IdleAnalyzer(
        trips,
        threshold_minutes=30
    )

    idle_gaps = (
        idle_analyzer.find_idle_gaps()
    )

    # -------------------------
    # DAY 3: CANCELLATIONS
    # -------------------------

    cancellation_analyzer = (
        CancellationAnalyzer(trips)
    )

    cancellation_summary = (
        cancellation_analyzer.get_summary()
    )
    anomaly_detector = AnomalyDetector(
        trips,
        drivers,
        driver_metrics,
        utilization_metrics
    )
    
    anomaly_summary = anomaly_detector.get_all_anomalies()
    
    insights_analyzer = InsightsAnalyzer(
        zone_metrics,
        hourly_demand,
        cancellation_summary,
        utilization_metrics,
        anomaly_summary
    )

    insights = insights_analyzer.generate_insights()
    # -------------------------
    # RETURN DASHBOARD
    # -------------------------

    top_riders = ranking_analyzer.top_riders_by_trip_count(
        trips,
        10
    )
    
    print("PEAK DEMAND DEBUG:", peak_demand)
    print("PEAK DEMAND TYPE:", type(peak_demand))
    
    return render_template(
        "index.html",

        success=True,

        driver_count=len(drivers),
        trip_count=len(trips),
        activity_count=len(activities),

        driver_index_count=len(driver_index),
        trip_index_count=len(trip_index),
        zone_index_count=len(zone_index),

        trip_summary=trip_summary,

        driver_metrics=driver_metrics,

        zone_metrics=zone_metrics,

        top_drivers_by_trips=top_drivers_by_trips,

        top_drivers_by_revenue=top_drivers_by_revenue,

        top_zones_by_demand=top_zones_by_demand,

        top_zones_by_cancellations=(
            top_zones_by_cancellations
        ),

        utilization_metrics=utilization_metrics,

        hourly_demand=hourly_demand,

        peak_demand=peak_demand,

        idle_gaps=idle_gaps,

        cancellation_summary=(
            cancellation_summary
        ),
        anomaly_summary=anomaly_summary,
        search_result=search_result,
        insights=insights,
        top_riders=top_riders,
        active_driver_count=active_driver_count
    )

@app.route("/search", methods=["POST"])
def search():

    search_query = request.form.get("search_query")

    if not search_query:
        return render_template(
            "search_result.html",
            search_result=None,
            error="Please enter a search value."
        )

    loader = DataLoader()

    drivers = loader.load_drivers(
        "data/uploaded_drivers.csv"
    )

    trips = loader.load_trips(
        "data/uploaded_trips.csv"
    )

    search_service = SearchService()

    driver_index = search_service.build_driver_index(drivers)
    trip_index = search_service.build_trip_index(trips)
    zone_index = search_service.build_zone_index(trips)

    # Search Driver
    driver = search_service.find_driver(driver_index, search_query)

    if driver:
        driver_analyzer = DriverAnalyzer(drivers, trips)

        profile = driver.get_profile()
        metrics = driver_analyzer.get_driver_metrics(search_query)

        search_result = {
            "type": "Driver",
            "profile": profile,
            "metrics": metrics
        }

    else:

        # Search Trip
        trip = search_service.find_trip(
            trip_index,
            search_query
        )

        if trip:

            search_result = {
                "type": "Trip",
                "data": {
                    "trip_id": trip.trip_id,
                    "driver_id": trip.driver_id,
                    "rider_id": trip.rider_id,
                    "city": trip.city,
                    "pickup_zone": trip.pickup_zone,
                    "drop_zone": trip.drop_zone,
                    "status": trip.status,
                    "fare": trip.fare,
                    "distance_km": trip.distance_km
                }
            }

        else:
            zone_parts = search_query.split(":", 1)
        
            if len(zone_parts) == 2:
                city, zone = zone_parts
        
                zone_trips = search_service.find_zone_trips(
                    zone_index,
                    city,
                    zone
                )
        
                if zone_trips:
                    search_result = {
                        "type": "Zone",
                        "data": {
                            "city": city,
                            "zone": zone,
                            "total_trips": len(zone_trips)
                        }
                    }
                else:
                    search_result = {
                        "type": "Not Found",
                        "data": {}
                    }
        
            else:
                search_result = {
                    "type": "Not Found",
                    "data": {}
                }

    return render_template(
        "search_result.html",
        search_result=search_result
    )

if __name__ == "__main__":
    app.run(debug=True)