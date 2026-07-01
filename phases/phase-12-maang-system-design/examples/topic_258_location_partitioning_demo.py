def geocell(lat, lon, cell_size_degrees=0.01):
    lat_cell = int(lat / cell_size_degrees)
    lon_cell = int(lon / cell_size_degrees)
    return lat_cell, lon_cell


def neighboring_cells(cell):
    lat_cell, lon_cell = cell
    cells = []

    for lat_delta in (-1, 0, 1):
        for lon_delta in (-1, 0, 1):
            cells.append((lat_cell + lat_delta, lon_cell + lon_delta))

    return cells


def main():
    rider_location = {"lat": 37.7749, "lon": -122.4194}
    drivers = [
        {"driver_id": "d1", "lat": 37.7750, "lon": -122.4195},
        {"driver_id": "d2", "lat": 37.7800, "lon": -122.4200},
        {"driver_id": "d3", "lat": 37.9000, "lon": -122.5000},
    ]

    rider_cell = geocell(rider_location["lat"], rider_location["lon"])
    candidate_cells = set(neighboring_cells(rider_cell))

    print(f"Rider cell: {rider_cell}")
    print("Candidate drivers from rider cell and neighbors:")

    for driver in drivers:
        driver_cell = geocell(driver["lat"], driver["lon"])
        if driver_cell in candidate_cells:
            print(f"  {driver['driver_id']} in cell {driver_cell}")


if __name__ == "__main__":
    main()

