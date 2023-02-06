import os
import csv
import json

def process_file(file_path, data_writer):
    with open(file_path, encoding='utf-8-sig') as file:
        data = json.load(file)
        for obj in data['timelineObjects']:
            if 'placeVisit' in obj:
                try:
                    name = obj['placeVisit']['location']['name']
                except KeyError:
                    name = obj['placeVisit']['location']['address']
                lat = obj['placeVisit']['location']['latitudeE7'] / 10**7
                lon = obj['placeVisit']['location']['longitudeE7'] / 10**7
                timestamp = obj['placeVisit']['duration']['startTimestamp']
                address = obj['placeVisit']['location']['address']
                placeid = obj['placeVisit']['location']['placeId']
                data_writer.writerow([timestamp, lat, lon, address, placeid, name])

def main():
    root_dir = "Takeout/Location History/Semantic Location History"
    output_file = "location_history.csv"

    with open(output_file, 'w', newline='') as outfile:
        data_writer = csv.writer(outfile)
        data_writer.writerow(["timestamp", "latitude", "longitude", "address", "placeid", "name"])

        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(subdir, file)
                    process_file(file_path, data_writer)

if __name__ == "__main__":
    main()