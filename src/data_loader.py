import csv

def load_airports(filepath):
    airports = {}

    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                airport_id = row[0]
                code = row[4]  # IATA code (IST, LON, etc.)
                lat = float(row[6])
                lon = float(row[7])

                if code:  # skip empty codes
                    airports[code] = (lat, lon)
            except:
                continue

    return airports
    

def load_routes(filepath):
    routes = []

    with open(filepath, encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                source = row[2]
                destination = row[4]

                if source and destination:
                    routes.append((source, destination))
            except:
                continue

    return routes