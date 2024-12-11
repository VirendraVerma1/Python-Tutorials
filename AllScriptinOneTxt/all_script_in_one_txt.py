import os

# Base directory where to start searching for .cs files
base_directory = "D:\\Programs\\Unity\\UnityMARSBodyTracking-master\\Assets\\MARS"

# Path of the file where to save the project information
output_file_path = os.path.join(base_directory, "project.txt")

def find_and_log_cs_files(directory):
    """Recursively finds .cs files, logs their paths, and writes their content to an output file."""
    with open(output_file_path, "w", encoding='utf-8') as output_file:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".cs"):
                    # Create the full path to the file
                    full_path = os.path.join(root, filename)
                    # Write the file path to the output file
                    output_file.write(f"File: {full_path}\n")

                    # Try to open the .cs file and handle possible encoding errors
                    content = read_file_with_fallback_encoding(full_path)
                    output_file.write(content + "\n")
                    output_file.write("\n" + "#" * 80 + "\n\n")  # Divider between files

def read_file_with_fallback_encoding(file_path, encodings=('utf-8', 'cp1252', 'iso-8859-1')):
    """Attempts to read a file with multiple encodings in case of UnicodeDecodeErrors."""
    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue  # Try the next encoding
    return f"ERROR: Failed to decode {file_path}\n"

# Call the function with the base directory
find_and_log_cs_files(base_directory)
