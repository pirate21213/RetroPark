import csv
import os.path
from datetime import datetime


def import_occupancy_data(data_dir):
    filepath = get_newest_dataset(data_dir)
    timestamp = os.path.basename(filepath).split('.')[0]
    timestamp = timestamp.replace('_', ':')

    data = list(csv.reader(open(filepath)))
    data.pop(0)
    total_spots = len(data)

    # Calculate total occ and nocc
    vacant_spots = 0
    occupied_spots = 0
    for spot in data:
        # print(spot)
        if spot[1] == 'occ':
            occupied_spots += 1
        else:
            vacant_spots += 1
    occupancy_percent = occupied_spots / total_spots * 100.0

    return total_spots, vacant_spots, occupied_spots, occupancy_percent, timestamp


def get_newest_dataset(search_dir):
    datasets = []
    path = ''
    for (dirpath, dirnames, filename) in os.walk(search_dir):
        datasets.extend(filename)
        path = dirpath
    # convert to timestamp
    for i in range(len(datasets)):
        datasets[i] = datasets[i].replace('.csv', '')

    timestamp = datetime.strptime(datasets[0], '%H_%M_%S')
    for i in range(len(datasets)):
        if datetime.strptime(datasets[i], '%H_%M_%S') > timestamp:
            timestamp = datetime.strptime(datasets[i], '%H_%M_%S')
    # print('{}{}_{}_{}.csv'.format(path, timestamp.hour, timestamp.minute, timestamp.second))
    timestamp = '{}{:02d}_{:02d}_{:02d}.csv'.format(path, timestamp.hour, timestamp.minute, timestamp.second)
    return timestamp


# Test Case
# print(get_newest_dataset('./remote_db/'))
print(import_occupancy_data('./remote_db/'))
