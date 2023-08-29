import os
import subprocess

#OPTIONS
input_folder = 'C:/Users/Tim/Documents/Python/Locomotion_Photometry/input_folder'
output_folder = 'C:/Users/Tim/Documents/Python/Locomotion_Photometry/output_folder'
udf_path = 'C:/Users/Tim/Documents/Python/UDFs'

#Main wrapper loop
input_files = os.listdir(input_folder)

for file_name in input_files:
	print('Processing: ' + file_name + '...')
	file_handle = input_folder + '/' + file_name
	save_handle = output_folder + '/' + file_name
	subprocess.call(['python', 'loco_photom_import.py', file_handle, save_handle])
	subprocess.call(['python', 'loco_photom_extract_behavior_trials.py', file_handle, save_handle, udf_path, 'import_data.pkl'])
	subprocess.call(['python', 'loco_photom_extract_photometry_trials.py', file_handle, save_handle, udf_path, 'import_data.pkl', 'behavior_data.pkl'])

print('Done')
