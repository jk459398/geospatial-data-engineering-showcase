Geospatial Data Engineering Showcase

This repository contains mini-projects demonstrating my skills in Geospatial Data Engineering, specifically focused on spatial data processing, data quality, and geographic analysis for e-commerce/logistics use cases.

Technologies Used:

    Python: pandas, geopandas, shapely

    Databases: PostgreSQL with PostGIS spatial extension

    Concepts: Data Pipelines, Spatial Data Quality, Geometry transformations, Bounding Boxes, Spatial Indexing (GiST), K-Nearest Neighbors (KNN).

Project 1: Spatial Data Quality & Processing Pipeline (Python)

Location: /python_pipeline/spatial_data_quality.py

Business Context: In a logistics network, raw data regarding parcel locker coordinates can often contain errors (e.g., swapped latitude/longitude, locations outside the target country).

What this script does:

    Extracts raw spatial coordinates.

    Performs Data Quality checks by verifying if the coordinates fall within a valid Bounding Box (e.g., boundaries of Poland).

    Filters out anomalies.

    Reprojects data from a global geographic coordinate system (EPSG:4326) to a local projected metric system (EPSG:2180).

    Creates a 500-meter pedestrian catchment area (buffer) around valid locations.

    Exports the cleaned and processed spatial data to a GeoJSON format ready for visualization.

Project 2: Nearest Locker Spatial Query (SQL / PostGIS)

Location: /sql_postgis/nearest_locker_query.sql

Business Context: When a customer enters their address, the system needs to instantly suggest the closest pickup locations based on actual geographical distance, not just zip codes.

What this script does:

    Defines spatial table structures using the GEOMETRY data type.

    Implements GiST spatial indexes for optimized query performance.

    Uses PostGIS functions to calculate the exact distance in meters between a customer's coordinates and parcel lockers, accounting for Earth's curvature (using GEOGRAPHY casting).

    Utilizes the <-> KNN operator to efficiently retrieve the top 2 closest lockers.

How to run

    Clone this repository.

    Install Python dependencies: pip install -r requirements.txt

    Run the Python pipeline: python python_pipeline/spatial_data_quality.py

    For SQL, execute the script in any PostgreSQL environment with the PostGIS extension enabled.