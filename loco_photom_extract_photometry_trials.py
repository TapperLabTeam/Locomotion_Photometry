import sys
import pandas as pd
import pickle
sys.path.append(sys.argv[3])
from signal_udfs import unpickle
from signal_udfs import plot_average_signals
from signal_udfs import plot_all_signals

#Import file and save handles from wrapper
file_handle = sys.argv[1]
save_handle = sys.argv[2]

#Import pickles
pkl_files = unpickle(sys.argv[4:])
import_data = pkl_files[0]
behavior_data = pkl_files[1]

#Filter behavior data to keep events >= 5s durations
behavior_data_filt = {'Start Time (s)': [], 'Stop Time (s)': [], 'Duration (s)': [], 'Interval (s)': [], '-5s to 0s Mean Distance (cm)': [], '-5s to 0s Mean Velocity (cm/s)': [], '0s to 5s Mean Distance (cm)': [], '0s to 5s Mean Velocity (cm/s)': []}

start_trim = []
stop_trim = []
duration_trim = []
#distance_trim = []
#velocity_trim = []
interval_trim = []

for num_num, num in enumerate(behavior_data['Duration']):
    if num >= 5 and behavior_data['Interval'][num_num] != 'NaN':
        start_trim.append(behavior_data['Start Time'][num_num])
        stop_trim.append(behavior_data['Stop Time'][num_num])
        duration_trim.append(num)
        interval_trim.append(behavior_data['Interval'][num_num])

behavior_data_filt['Start Time (s)'] = start_trim
behavior_data_filt['Stop Time (s)'] = stop_trim
behavior_data_filt['Duration (s)'] = duration_trim
behavior_data_filt['Interval (s)'] = interval_trim

#Calculate mean distance and velocity for -5s to 0s and 0s to 5s.
base_distance = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
base_velocity = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
event_distance = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
event_velocity = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]

for time_num, time in enumerate(behavior_data_filt['Start Time (s)']):
    for num_num, num in enumerate(import_data['Loco Time']):
        if num != 'NaN':
            if num - time >= -5 and num - time < 0:
                base_distance[time_num].append(import_data['Distance'][num_num])
                base_velocity[time_num].append(import_data['Velocity'][num_num])
            if num - time >= 0 and num - time <= 5:
                event_distance[time_num].append(import_data['Distance'][num_num])
                event_velocity[time_num].append(import_data['Velocity'][num_num])

df = pd.DataFrame(base_distance)
behavior_data_filt['-5s to 0s Mean Distance (cm)'] = df.mean(axis = 1, skipna = True).tolist()

df = pd.DataFrame(base_velocity)
behavior_data_filt['-5s to 0s Mean Velocity (cm/s)'] = df.mean(axis = 1, skipna = True).tolist()

df = pd.DataFrame(event_distance)
behavior_data_filt['0s to 5s Mean Distance (cm)'] = df.mean(axis = 1, skipna = True).tolist()

df = pd.DataFrame(event_velocity)
behavior_data_filt['0s to 5s Mean Velocity (cm/s)'] = df.mean(axis = 1, skipna = True).tolist()

#Save behavior_data_filt pickle
pickle.dump(behavior_data_filt, open('behavior_data_filt.pkl','wb'))
df = pd.DataFrame.from_dict(behavior_data_filt)
df.to_csv(save_handle[:-4] + '_behavior_data.csv', index = False)


#Extract photometry traces based on behavior event start times (-5s pre, 5s post)
#Create blank lists for extracting events					
base_time = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
base_trace = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
event_time = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
event_trace = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
full_time = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
full_trace = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]

#Extract evens from raw data dict
for stamp_num, stamp in enumerate(behavior_data_filt['Start Time (s)']):
	for num_num, num in enumerate(import_data['Photo Time']):
		if num >= stamp - 5 and num < stamp:
			base_time[stamp_num].append(num)
			base_trace[stamp_num].append(import_data['DF/F0'][num_num])
			full_time[stamp_num].append(num)
			full_trace[stamp_num].append(import_data['DF/F0'][num_num])
		if num >= stamp and num <= stamp + 5:
			event_time[stamp_num].append(num)
			event_trace[stamp_num].append(import_data['DF/F0'][num_num])
			full_time[stamp_num].append(num)
			full_trace[stamp_num].append(import_data['DF/F0'][num_num])


#Create blank lists for normalizing times			
base_time_norm = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
event_time_norm = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
term_time_norm = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
full_time_norm = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
			
#Normalize times
for time_num, time in enumerate(event_time):
	zero_time = event_time[time_num][0]
	for times in base_time[time_num]:
		base_time_norm[time_num].append(times - zero_time)
		full_time_norm[time_num].append(times - zero_time)
	for times in event_time[time_num]:
		event_time_norm[time_num].append(times - zero_time)
		full_time_norm[time_num].append(times - zero_time)

	
#Calculate baseline mean and STD for calculating Zscores
df = pd.DataFrame(base_trace)
df = df.T
base_means = df.mean(axis = 0, skipna = True)
base_stds = df.std(axis = 0, skipna = True)

#Create blank lists for trace zscores
base_trace_z = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
event_trace_z = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]
full_trace_z = [[] for x in range(len(behavior_data_filt['Start Time (s)']))]

#Calculate Zscores
for num_num, num in enumerate(base_means):
	for point in base_trace[num_num]:
		base_trace_z[num_num].append((point - base_means[num_num])/base_stds[num_num])
	for point in event_trace[num_num]:
		event_trace_z[num_num].append((point - base_means[num_num])/base_stds[num_num])
	for point in full_trace[num_num]:
		full_trace_z[num_num].append((point - base_means[num_num])/base_stds[num_num])
		
#Find longest time for plotting
longest_time = []
prev_len = 0

for x in full_time_norm:
	z = len(x)
	if z > prev_len:
		longest_time = x
	prev_len = z

#Plot signals	
plot_average_signals(longest_time, full_trace_z, 'Time (s)', 'DF/F0 Zscore', save_handle[:-4] + '_avg_signals_1')
plot_all_signals(full_time_norm, full_trace_z, 'Time (s)', 'DF/F0 Zscore', save_handle[:-4] + '_all_signals_1')

#Pickle dict of trace data
event_dict = {}
event_dict['Base Time'] = base_time_norm
event_dict['Base Trace'] = base_trace_z
event_dict['Event Time'] = event_time_norm
event_dict['Event Trace'] = event_trace_z
event_dict['Full Time'] = full_time_norm
event_dict['Full Trace'] = full_trace_z

pickle.dump(event_dict,open('event_dict.pkl','wb'))
