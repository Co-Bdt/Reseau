import os
import time

# TODO : make this script run every day at 04:00

# Path to the images folder
images_folder = "./images_folder"

# Get the current time
current_time = time.time()

# Iterate over the files in the images folder
for filename in os.listdir(images_folder):
    file_path = os.path.join(images_folder, filename)

    # Check if the file is a regular file and not a directory
    if os.path.isfile(file_path):
        # Get the creation time of the file
        creation_time = os.path.getctime(file_path)

        # Calculate the time difference in seconds
        time_difference = current_time - creation_time

        # Check if the file has been in the folder
        # for more than 1 day (86400 seconds)
        if time_difference > 86400:
            # Delete the file
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
