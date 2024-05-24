# import os

# def delete_files_in_directories(directories):
#     for directory in directories:
#         # Get the full path of the directory
#         directory_path = os.path.join(os.getcwd(), directory)
#         # Check if the directory exists
#         if os.path.exists(directory_path):
#             # Iterate over files in the directory
#             for filename in os.listdir(directory_path):
#                 file_path = os.path.join(directory_path, filename)
#                 # Check if it's a file
#                 if os.path.isfile(file_path):
#                     # Delete the file
#                     os.remove(file_path)
#                     print(f"Deleted file: {file_path}")
#         else:
#             print(f"Directory does not exist: {directory_path}")

# # Directories to delete files from
# directories_to_clear = ["mapper_50052", "mapper_50053", "Reducers"] 

# # Call the function to delete files
# delete_files_in_directories(directories_to_clear)
import os
import shutil

def clear_data_folder(data_folder):
    for item in os.listdir(data_folder):
        item_path = os.path.join(data_folder, item)
        if os.path.isdir(item_path) and item != 'Input':
            shutil.rmtree(item_path)
        elif os.path.isfile(item_path) and item != 'Input':
            os.remove(item_path)

# Path to the Data folder
data_folder = 'Data'

# Clear the contents of the Data folder
clear_data_folder(data_folder)

print("Contents of the 'Data' folder except 'Input' folder have been cleared.")
