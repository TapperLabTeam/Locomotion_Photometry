import sys
import pandas as pd
import pickle

file_handle = sys.argv[1]
save_handle = sys.argv[2]

#Import data from .csv input file
import_data = {'Loco Time': [], 'Distance': [], 'Velocity': [], 'Photo Time': [], 'DF/F0': []}

loco_time = []
distance = []
velocity = []
photo_time = []
df_f0 = []

for line_num, line in enumerate(open(file_handle)):
    line = line.strip().split(',')
    if line_num > 0:
        for point_num, point in enumerate(line):
            if point_num == 0 and point != '':
                loco_time.append(float(point))
            if point_num == 0 and point == '':
                loco_time.append('NaN')
            if point_num == 1 and point != '':
                distance.append(float(point))
            if point_num == 1 and point == '':
                distance.append('NaN')
            if point_num == 2 and point != '':
                velocity.append(float(point))
            if point_num == 2 and point == '':
                velocity.append('NaN')
            if point_num == 3 and point != '':
                photo_time.append(float(point))
            if point_num == 3 and point == '':
                photo_time.append('NaN')
            if point_num == 4 and point != '':
                df_f0.append(float(point))
            if point_num == 4 and point == '':
                df_f0.append('NaN')

import_data['Loco Time'] = loco_time
import_data['Distance'] = distance
import_data['Velocity'] = velocity
import_data['Photo Time'] = photo_time
import_data['DF/F0'] = df_f0

pickle.dump(import_data, open('import_data.pkl','wb'))
