import csv
import cv2
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


def generate_overview(occupancy_data):
    # Grab total spots from csv
    total_spots, vacant_spots, occupied_spots, occupancy_percent, timestamp = import_occupancy_data(occupancy_data)
    color = (255, 0, 0)  # BGR
    lot_diag = cv2.imread("./Parking_Diagram_Ex.jpg")

    # Load diag csv for display location data
    diag_loc = list(csv.reader(open('./diagram_locations_ex.csv')))
    diag_loc.pop(0)  # throws out header
    print(diag_loc)

    # Load main occupancy data for individual spot data
    filepath = get_newest_dataset(occupancy_data)
    data = list(csv.reader(open(filepath)))
    data.pop(0)

    for index in range(len(data)):
        if data[index][1] == "nocc":
            # This created a color gradient based on confidence, not a fan
            # color = (float(data[index][2])*255.0, 0, 100 - (float(data[index][2])*100.0))     # BGR
            if abs(float(data[index][3])) > 0.6:
                color = (255, 188, 149)
            else:
                color = (255, 205, 175)
            print("nocc", data[index][0], color)

            # Find the correlating spotID and set the status
            for search in diag_loc:
                if search[5] == data[index][0]:
                    lot_diag = cv2.rectangle(lot_diag, (int(search[1]), int(search[2])),
                                             (int(search[3]), int(search[4])), color, -1)
        else:
            # Find the correlating spotID and set the status
            if abs(float(data[index][3])) > 0.6:
                color = (0, 0, 0)
            else:
                color = (61, 61, 61)
            print("occ", data[index][0], color)
            for search in diag_loc:
                if search[5] == data[index][0]:
                    lot_diag = cv2.rectangle(lot_diag, (int(search[1]), int(search[2])),
                                             (int(search[3]), int(search[4])), color, -1)

    # After populating the occ data, fill in which spots are considered inaccessible (spotID = -1)
    for search in diag_loc:
        hazard_color = (14, 208, 208)  # BGR
        if int(search[5]) == -1:
            print("hazard at: ", search[0])
            lot_diag = cv2.rectangle(lot_diag, (int(search[1]), int(search[2])), (int(search[3]), int(search[4])),
                                     hazard_color, -1)
    cv2.imwrite('./.current_diag.jpg', lot_diag)


def generate_full_overview():
    # Grab total spots from csv
    color = (255, 0, 0)  # BGR
    lot_diag = cv2.imread("./Parking_Diagram_Ex.jpg")

    # Load diag csv for display location data
    diag_loc = list(csv.reader(open('./diagram_locations_ex.csv')))
    diag_loc.pop(0)  # throws out header
    print(diag_loc)
    for search in diag_loc:
        lot_diag = cv2.rectangle(lot_diag, (int(search[1]), int(search[2])),
                             (int(search[3]), int(search[4])), color, -1)
    cv2.imwrite('./.current_diag.jpg', lot_diag)


# Test Case
# print(get_newest_dataset('./remote_db/'))
# print(import_occupancy_data('./remote_db/'))
# generate_overview('./remote_db/')
generate_full_overview()
