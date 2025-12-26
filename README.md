# GO Transit Fare Zones & Fare By Network Distance Analysis
<a id="readme-top"></a>
An independent, exploratory project using **GO Transit GTFS data** and open-source tools to visualize fare zones and analyze the relationship between **zone-based fares** and **network travel distances**.  
*All views are my own and do not represent official GO Transit fare zones, designs, or policies.*

---

## Table of Contents
- [Overview](#overview)
- [Project Goals](#project-goals)
- [Data Sources](#data-sources)
- [Workflow](#workflow)
- [Key Components](#key-components)
- [Outputs](#outputs)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [License](#license)

---

## Overview
GO Transit uses **zone-based pricing**, but there is limited public visualization of fare zones and little analysis of how fares relate to travel distances through the GO Transit network. This project addresses that gap by:

1. **Visualizing GO Transit fare zones** using Voronoi polygons derived from GTFS stop data.
2. **Computing network-based distances** between zones (not straight-line distances).
3. **Exploring fare vs. distance relationships** to identify patterns.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Project Goals
- Create **interactive maps** of GO Transit fare zones using public GTFS data.
- Build a **network graph** of GO Transit routes and transfers.
- Calculate **average shortest-path network distances** between zones.
- Compare these distances to **existing fare structures** for insights into pricing fairness and efficiency.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Data Sources
- **GO Transit GTFS Feed** (as of 2025-12-10):  
  [GO Transit Developer Resources](https://www.gotransit.com/en/partner-with-us/software-developers)
- **Custom Service Boundary**: `GO_zone.geojson`  
  Defines the spatial extent for clipping Voronoi polygons.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Workflow
1. **Zone Map Generation**  
   - Notebook: `go_transit_zone_map.ipynb`  
   - Process:
     - Load GTFS stops.
     - Generate Voronoi polygons in a projected CRS.
     - Clip to custom service boundary.
     - Dissolve by zone identifier.
     - Reproject to WGS84 for web visualization.
   - Outputs:
     - `01_go_transit_voronoi_fare_zones.html`
     - `02_go_transit_voronoi_fare_zones_treelayer.html` (enhanced UI)

2. **Network Distance Analysis**  
   - Notebook: `go_transit_network_shortest_distance.ipynb`  
   - Process:
     - Build a multimodal graph from GTFS routes and transfers.
     - Compute shortest network path distances between all stop pairs.
     - Aggregate to **average inter-zonal network distance**.
     - Analyze zonal fare pattern sorted by average inter-zonal network distance.
   - Outputs:
     - `03_go_transit_shortest_BM_to_LI.html` (shortest network path example: Bloomington → Old Elm test)
     - `04_go_transit_networkx.html` (graph visualization of network connectivity)
     - `05_go_transit_zone_to_zone_fare_network_distance_explorer.html` (final interactive explorer)
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Key Components
- **Voronoi Zone Map**: Visualizes fare zones derived from GTFS stops.
- **Network Graph**: Represents GO Transit routes and transfer points.
- **Distance Computation**: Calculates realistic travel distances using network paths.
- **Interactive Explorer**: Compares fares vs. network distances for any origin zone.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Outputs
- **Zone Visualization**:  
  `01_go_transit_voronoi_fare_zones.html`  
  `02_go_transit_voronoi_fare_zones_treelayer.html`
- **Distance Analysis**:  
  `03_go_transit_shortest_BM_to_LI.html`  
  `04_go_transit_networkx.html`
- **Final Explorer**:  
  `05_go_transit_zone_to_zone_fare_network_distance_explorer.html`
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started
### Prerequisites
- Python ≥ 3.10
- Recommended packages: `pandas`, `geopandas`, `networkx`, `shapely`, `pyproj`, `jinja2`
- Modern browser for viewing HTML outputs.

### Quick Start
1. Clone the repository.
2. Open any HTML output in your browser to explore results.
3. To reproduce:
   - Download **zipped** GTFS feed and place in `data/GO_GTFS/`.
   - Run notebooks in order:
     - `go_transit_zone_map.ipynb`
     - `go_transit_network_shortest_distance.ipynb`
<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Project Structure
```text
project-root/
├─ data/
│  ├─ GO_GTFS/                # Raw GTFS archives
│  └─ GIS/                    # Raw/Derived GeoJSON
├─ src/
│  ├─ build_voronoi_zones.py  # Voronoi zones + dissolve
│  ├─ gtfs_cleaning.py        # Prepare GTFS data
├─ outputs/
│  ├─ 01_*.html               # 01_go_transit_voronoi_fare_zones
│  └─ 02_*.html               # 02_go_transit_voronoi_fare_zones_treelayer
│  └─ 03_*.html               # 03_go_transit_shortest_BM_to_LI
│  └─ 04_*.html               # 04_go_transit_networkx
│  └─ 05_*.html               # 05_go_transit_zone_to_zone_fare_network_distance_explorer
├─ config.json
├─ .gitignore
├─ requirements.txt
├─ setting.json
├─ README.md
└─ LICENSE
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


---


## License
This project is licensed under the MIT license. See [LICENSE](https://github.com/zhenhuasun/go-zone-network-explorer/?tab=MIT-1-ov-file/) for more information.
<p align="right">(<a href="#readme-top">back to top</a>)</p>