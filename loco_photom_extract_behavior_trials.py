import sys
import pandas as pd
import pickle
import statistics
sys.path.append(sys.argv[3])
from signal_udfs import unpickle

#Import file and save handles from wrapper
file_handle = sys.argv[1]
save_handle = sys.argv[2]

#Import pickles
pkl_files = unpickle(sys.argv[4:])
import_data = pkl_files[0]

#Set up dict for behavioral data
behavior_data = {'Start Time': [], 'Stop Time': [], 'Duration': [], 'Interval': [], 'Baseline Mean Distance': [], 'Baseline Mean Velocity': [], 'Event Mean Distance': [], 'Event Mean Velocity': []}

temp_time = 0
start_stamp = 0
start_times = []
stop_times = []
duration = []

#Grab start and stop timestamps for distance moved < 1 cm as immobile; calculate mean durations, distances, velocities
for num_num, num in enumerate(import_data['Distance']):
    if num != 'NaN':
        if num < 1 and start_stamp == 0:
            temp_time = import_data['Loco Time'][num_num]
            start_times.append(temp_time)
            start_stamp = 1
        if num >= 1 and start_stamp == 1:
            start_stamp = 0
            stop_times.append(import_data['Loco Time'][num_num])
            duration.append(import_data['Loco Time'][num_num] - temp_time)

behavior_data['Start Time'] = start_times[:len(stop_times)]
behavior_data['Stop Time'] = stop_times
behavior_data['Duration'] = duration

#Calculate Intervals for Events
interval = []
for num_num, num in enumerate(behavior_data['Start Time']):
    if num_num == 0:
        interval.append(num - import_data['Loco Time'][0])
    if num_num > 0:
        interval.append(num - behavior_data['Stop Time'][num_num - 1])

behavior_data['Interval'] = interval

#Dump behavior_data pickle
pickle.dump(behavior_data, open('behavior_data.pkl','wb'))
