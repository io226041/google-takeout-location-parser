import os
import csv
import json
import datetime
from pathlib import Path


def process_file(file_path, data_writer):
    print(f"Reading file: {file_path}")  # Debugging line
    try:
        with open(file_path, encoding='utf-8-sig') as file:
            data = json.load(file)
            for obj in data['timelineObjects']:
                if 'placeVisit' in obj and 'location' in obj['placeVisit']:
                    location = obj['placeVisit']['location']
                    address = location.get('address')
                    name = location.get('name', address)
                    lat = location.get('latitudeE7') / 10 ** 7
                    lon = location.get('longitudeE7') / 10 ** 7
                    placeid = location.get('placeId')

                    timestamp = None
                    epoch_time = None
                    if 'duration' in obj['placeVisit']:
                        timestamp = obj['placeVisit']['duration'].get('startTimestamp')
                        # Convert the timestamp to a datetime object
                        if timestamp is not None:
                            try:
                                datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                            except ValueError:
                                datetime_obj = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
                            # Convert the datetime object to Unix epoch time
                            epoch_time = int(datetime_obj.timestamp())

                    # Write the data to the CSV file
                    data_writer.writerow([timestamp, lat, lon, address, placeid, name, epoch_time])
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {file_path}: {e}")  # Debugging line

def main():
    root_dir = Path(".") / "Takeout" / "Location History (Timeline)" / "Semantic Location History"
    output_file = "semantic_location_history.csv"

    if not os.path.exists(root_dir):
        print(f"Root directory does not exist: {root_dir}")
        return

    with open(output_file, 'w', newline='') as outfile:
        data_writer = csv.writer(outfile)
        data_writer.writerow(["timestamp", "latitude", "longitude", "address", "placeid", "name", "epoch_time"])

        for subdir, dirs, files in os.walk(root_dir):
            print(f"Checking directory: {subdir}")  # Debugging line
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(subdir, file)
                    print(f"Processing file: {file_path}")  # Debugging line
                    process_file(file_path, data_writer)
                else:
                    print(f"Skipping file: {file}")  # Debugging line

    print("semantic_location_history.csv created in current directory")

if __name__ == "__main__":
    main()
