````markdown
# Mobility Operations Intelligence Tool

A Flask-based mobility operations analytics application designed to analyze drivers, trips, zones, cancellations, utilization, and operational anomalies.

## Overview

The Mobility Operations Intelligence Tool processes mobility data and provides operational insights through an interactive Flask dashboard.

The application supports:

- Data ingestion and validation
- Driver analytics
- Trip analytics
- Zone analytics
- Driver utilization analysis
- Cancellation analysis
- Top-K rankings
- Idle-time analysis
- Anomaly detection
- Driver/trip/zone search
- Automated operational insights
- Interactive dashboard visualization

## Key Features

### 1. Data Ingestion & Validation

The application loads mobility data from CSV files and validates the data before processing.

Supported datasets:

- Drivers
- Trips
- Driver activity

The application also supports uploading mobility datasets through the web interface.

### 2. Mobility KPIs

The dashboard provides key operational metrics including:

- Total Drivers
- Active Drivers
- Total Riders
- Total Trips
- Completed Trips
- Cancelled Trips
- Completion Rate
- Cancellation Rate
- Total Revenue
- Average Fare
- Average Trip Distance
- Average Trip Duration

### 3. Driver Analytics

Driver-level analytics include:

- Driver profile
- Total trips
- Completed trips
- Cancelled trips
- Completion rate
- Cancellation rate
- Revenue
- Average fare
- Average distance

The dashboard also provides driver rankings and operational attention indicators.

### 4. Trip Analytics

Trip data is analyzed to identify:

- Completed trips
- Cancelled trips
- Revenue
- Average fare
- Distance
- Duration
- Peak demand periods

Trip-level data is also used for cancellation and anomaly analysis.

### 5. Zone Analytics

The application provides zone-level analysis including:

- Trip demand by zone
- Cancellation patterns
- City and zone comparisons
- Demand distribution by time period

The application maintains a zone-based index to efficiently retrieve trips associated with a city and zone.

### 6. Driver Utilization

Driver activity data is used to calculate:

- Online hours
- Busy hours
- Idle hours
- Utilization percentage

Drivers are classified into:

- High utilization
- Medium utilization
- Low utilization

The utilization thresholds are configurable in the analyzer.

### 7. Cancellation Intelligence

Cancellation analysis identifies patterns across:

- Zones
- Drivers
- Time periods
- Cancellation reasons

The analysis uses grouping, frequency counting, sorting, and filtering to identify operational patterns.

### 8. Idle-Time Analysis

Trips are ordered chronologically for each driver and the gaps between consecutive trips are calculated.

This can be used to identify periods of prolonged driver inactivity.

### 9. Anomaly Detection

The application detects potential trip-level and driver-level anomalies.

#### Trip Anomalies

Examples include:

- Negative fare
- Zero distance
- Invalid timestamps
- Extremely long trip duration
- Unknown driver
- Unusual fare

#### Driver Anomalies

Examples include:

- High cancellation rate
- Low utilization
- Unusually high trip count
- Low driver rating

Anomalies are surfaced separately so they can be investigated without preventing the rest of the dataset from being analyzed.

### 10. Search Engine

The application uses dictionary-based indexes for fast lookups.

Indexes include:

```text
Driver ID → Driver
Trip ID   → Trip
City/Zone → Trips
````

This allows drivers, trips, and zones to be searched without repeatedly scanning the complete dataset.

### 11. Insights Engine

The application generates operational summaries from the analyzed data.

Examples include:

* Highest cancellation zone
* Peak demand period
* Number of low-utilization drivers
* Largest cancellation category
* Total detected anomalies

The insights are generated dynamically from the processed data.

## Project Architecture

```text
mobility_operations_tool/
│
├── python_app.py
├── requirements.txt
├── generate_data.py
│
├── models/
│   ├── __init__.py
│   ├── driver.py
│   ├── trip.py
│   ├── zone.py
│   └── activity.py
│
├── services/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── validation_service.py
│   └── search_service.py
│
├── analytics/
│   ├── __init__.py
│   ├── trip_analyzer.py
│   ├── driver_analyzer.py
│   ├── zone_analyzer.py
│   ├── ranking_analyzer.py
│   ├── activity_analyzer.py
│   ├── utilization_analyzer.py
│   ├── demand_analyzer.py
│   ├── idle_analyzer.py
│   ├── cancellation_analyzer.py
│   ├── anomaly_detector.py
│   └── insights_analyzer.py
│
├── templates/
│   ├── index.html
│   └── search_result.html
│
├── static/
│   └── style.css
│
├── data/
│
└── tests/
    └── __init__.py
```

## Technology Stack

### Backend

* Python
* Flask
* Object-Oriented Programming

### Data Processing

* Python data structures
* CSV
* Datetime processing
* Dictionaries
* Lists
* Sorting
* Grouping
* Filtering
* Priority queues / Top-K analysis

### Frontend

* HTML
* CSS
* JavaScript
* Jinja templates

## OOP Design

The application separates responsibilities across multiple classes.

### Models

```text
Driver
Trip
Zone
DriverActivity
```

These classes represent the core mobility entities.

### Services

```text
DataLoader
DataValidator
SearchService
```

These classes handle data loading, validation, and indexing/search functionality.

### Analytics

```text
DriverAnalyzer
TripAnalyzer
ZoneAnalyzer
RankingAnalyzer
ActivityAnalyzer
UtilizationAnalyzer
DemandAnalyzer
IdleAnalyzer
CancellationAnalyzer
AnomalyDetector
InsightsAnalyzer
```

Each analyzer is responsible for a specific analytical area.

## Dataset

The project includes generated mobility data for demonstration and testing.

The generated dataset contains:

* 250 drivers
* 4,500 trips
* Driver activity records
* 3 cities
* Multiple operational zones

The data generator also introduces selected invalid and unusual records to test the anomaly detection functionality.

## Running the Application

### 1. Clone the repository

```bash
git clone https://github.com/PavanKumarVNL/mobility_operations_tool.git
cd mobility_operations_tool
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the environment

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Generate sample data

If sample data needs to be regenerated:

```bash
python generate_data.py
```

### 6. Start the Flask application

```bash
python python_app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

## Sample Dashboard Metrics

Using the included sample dataset, the application currently produces metrics such as:

```text
Total Drivers       : 250
Active Drivers      : 197
Total Trips         : 4500
Completed Trips     : 3966
Cancelled Trips     : 534
Completion Rate     : 88.1%
Cancellation Rate   : 11.9%
Total Revenue       : ₹1,277,679
Average Fare        : ₹322
Average Distance    : 13.5 km
Average Duration    : 43.4 min
```

These values are based on the generated sample dataset and will change when different data is uploaded.

## Data Flow

```text
CSV / Uploaded Data
        │
        ▼
Data Loader
        │
        ▼
Data Validation
        │
        ▼
Object Creation
        │
        ▼
Search / Index Creation
        │
        ▼
Analytics Engine
        │
        ├── Driver Analytics
        ├── Trip Analytics
        ├── Zone Analytics
        ├── Utilization
        ├── Cancellation
        ├── Idle Time
        └── Anomaly Detection
        │
        ▼
Insights Engine
        │
        ▼
Flask Dashboard
```

## Project Objective

The primary objective of this project is to demonstrate how a mobility operations dataset can be transformed into actionable operational information using:

* Python
* Object-oriented design
* Data structures and algorithms
* Data validation
* Analytical processing
* Anomaly detection
* Flask-based web development

The project emphasizes modularity and explainable Python logic rather than relying on external analytics platforms.

## Future Improvements

Potential extensions include:

* Interactive charts and visualizations
* Database integration
* Authentication and role-based access
* Advanced anomaly detection models
* Historical trend analysis
* Exportable operational reports
* More advanced search and filtering

## Author

**Pavan Kumar V.**

Mobility Operations Intelligence Tool
Built using Python, Flask, OOP, Data Structures, and Analytics.

```

Available next action: :contentReference[oaicite:0]{index=0}
```
