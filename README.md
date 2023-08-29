# Locomotion Photometry
Extracts traces from photometry data and calculates zscores based on timestamps from time locked behavior videos.

Instructions:
1. Create the folders "input_folder" and "output_folder."
2. Change the input and output folder directories in "loco_photom_wrap.py" to match your directories.
3. Change the udf_path directory to folder containing "signal_udfs.py."
4. Copy .csv files of photometry and behavior data to the input_folder.
5. .csv files should be organized thusly: row 1 = column headers, column 1 = locomotor activity timestamps (seconds), column 2 = distance traveled (cm), column 3 = velocity (cm/s), column 4 = photometry timestamps (seconds), column 5 = photometry DF/F0 signal.
6. Run "loco_photom_wrap.py" to execute program.
