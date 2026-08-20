# Road Intelligence Platform — Prototype

An AI-powered road-condition monitoring and maintenance-prioritization demo.
**This is a research/demo prototype, not a production system.** See
[Prototype assumptions vs. production requirements](#prototype-assumptions-vs-production-requirements)
below before treating any number here as real.

Full system vision (spec):

```
Vehicle Camera → Defect Detection → GPS + Timestamp → Road Segment Identification
→ Multi-Vehicle Aggregation → Traffic Analysis → Maintenance History
→ Condition Score → Priority Score → Central Ranking → Government Dashboard
```

---

## Build status

| Milestone | Scope | Status |
|---|---|---|
| 1 | Backend + database + synthetic data | ✅ Done |
| 2 | Road segments + GPS observation matching | ⏳ Not started |
| 3 | Aggregation engine | ⏳ Not started |
| 4 | Condition scoring | ⏳ Not started |
| 5 | Priority scoring | ⏳ Not started |
| 6 | Ranking engine | ⏳ Not started |
| 7 | Frontend dashboard | ⏳ Not started |
| 8 | GIS map | ⏳ Not started |
| 9 | Vehicle image detection (CV) | ⏳ Not started |
| 10 | Simulation mode | ⏳ Not started |
| 11 | Testing | ⏳ Not started |
| 12 | Final polish | ⏳ Not started |

This README will be expanded at each milestone. Right now it documents Milestone 1 only.

---

## Milestone 1 — what's implemented

- SQLAlchemy ORM schema: `roads`, `road_segments`, `vehicles`, `vehicle_observations`, `traffic_data`, `maintenance_history`
- `seed_database.py` — deterministic synthetic data generator
- FastAPI app with read endpoints to verify the seeded data (`/roads`, `/roads/{id}`, `/segments`, `/segments/{id}`, `/segments/{id}/observations`, `/segments/{id}/history`)
- Stub endpoints (`/rankings`, `POST /observations`, `POST /recalculate`) that return `501` — present to show the full planned API surface, not yet implemented

## Data model

```
roads                road_id (PK), name, region
road_segments         segment_id (PK), road_id (FK), start/end lat+lon, length_km, sequence_index
vehicles              vehicle_id (PK, anonymous), vehicle_type
vehicle_observations  id (PK), vehicle_id (FK), road_id (FK), segment_id (FK),
                       timestamp, lat, lon, distance_km,
                       pothole_count, crack_count, other_defect_count,
                       average_severity, confidence, image_reference
traffic_data          segment_id (PK/FK), vehicles_per_day, cars, bikes, buses, trucks,
                       peak_hour_volume, weekly_vehicle_count
maintenance_history   segment_id (PK/FK), construction_date, last_repair_date,
                       last_repair_cost, total_historical_cost,
                       number_of_repairs, last_repair_type
```

No PII is collected anywhere in this schema — `vehicle_id` is an opaque anonymous
identifier (e.g. `V0042`). No names, phone numbers, or registration numbers.

## Synthetic dataset (seed_database.py)

Running the seed script with `--seed 42` currently generates:

- 10 roads, ~90 segments (5–11 per road)
- 30 anonymous vehicles
- ~3,700 vehicle observations across a 27-day window (25 May – 20 June 2026)
- traffic and maintenance records for every segment

Each segment is randomly assigned one of 8 **archetypes** that jointly determine
its traffic level, defect trend, and repair history so the generated data stays
internally consistent (e.g. a segment with a rapidly rising defect trend won't
also randomly get a "just repaired last month" maintenance record):

`high_traffic_severe`, `low_traffic_severe`, `high_traffic_moderate`,
`recent_repair_good`, `old_repair_degraded`, `repeated_repair_chronic`,
`rapid_deterioration`, `stable_normal`

The generator is deterministic — the same `--seed` value always produces the
same dataset, which matters for reproducible testing in later milestones.

## Real vs. simulated (this milestone)

| Component | Status |
|---|---|
| Database schema, ORM relationships | Real |
| FastAPI app structure and query endpoints | Real |
| Roads, segments, vehicles, observations, traffic, maintenance data | **Simulated** |
| Road segment geometry | **Simulated** (synthetic straight-line coordinates, not real road curvature) |

## How to run

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Generate the synthetic dataset (creates ./road_intelligence.db)
python seed_database.py --seed 42 --reset

# Start the API
uvicorn app.main:app --reload --port 8000
```

Then visit `http://localhost:8000/docs` for interactive Swagger docs, or try:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/roads
curl http://localhost:8000/roads/SH-01
curl http://localhost:8000/segments?road_id=SH-01
curl http://localhost:8000/segments/SH01-S001
curl http://localhost:8000/segments/SH01-S001/observations
```

## Prototype assumptions vs. production requirements

| Area | Prototype (this repo) | Production would need |
|---|---|---|
| Database | SQLite via SQLAlchemy | PostgreSQL + PostGIS |
| Geometry | Straight-line start/end coordinates | Real road-network polylines (e.g. from OSM) |
| GPS-to-segment matching | Not yet built (Milestone 2) | PostGIS `ST_ClosestPoint` / map-matching algorithm |
| Data source | `seed_database.py` synthetic generator | Real vehicle telemetry ingestion (`POST /observations`, stubbed) |
| Computer vision | Not yet built (Milestone 9) | Trained defect-detection model, validated on real road imagery |
| Scoring weights | Not yet built (Milestones 4–5) | Configurable, but explicitly *not* scientifically validated — will be labeled "prototype weighting / policy parameters" |
| Auth | None | Production authentication & authorization |

## Scaling path (how each simulated piece gets replaced)

- **Database**: change `DATABASE_URL` env var to a Postgres connection string — no application code changes needed elsewhere.
- **Geometry**: swap `start_lat/start_lon/end_lat/end_lon` columns for a PostGIS `Geometry(LINESTRING)` column once real road shapefiles are available.
- **Data ingestion**: `seed_database.py` gets replaced by real traffic hitting `POST /observations` (already reserved in the API surface).
- **CV**: the CV module (Milestone 9) will be built with a clear `Image → Detection Model → Defect Detection API` boundary so a custom-trained YOLO model can be swapped in for the initial pretrained/simulated detector without touching the rest of the pipeline.

---

*Next: Milestone 2 — GPS/segment matching and the observation ingestion endpoint.*
