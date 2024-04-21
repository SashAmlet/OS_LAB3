import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class FileData:
    def __init__(self, full_name, length, creation_time, extension):
        self.full_name = full_name
        self.length = int(length)
        self.creation_time = creation_time
        self.extension = extension

def read_csv_file(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            data.append(FileData(row['FullName'], row['Length'], row['CreationTime'], row['Extension']))
    return data

def calculate_average_size(data):
    average_sizes = {}
    count_files = {}
    
    for file_data in data:
        if file_data.extension not in average_sizes:
            average_sizes[file_data.extension] = 0
            count_files[file_data.extension] = 0
        
        average_sizes[file_data.extension] += file_data.length
        count_files[file_data.extension] += 1

    for extension in average_sizes:
        average_sizes[extension] /= count_files[extension]

    return average_sizes

def plot_average_size_size_by_type(average_sizes):
    extensions = list(average_sizes.keys())
    average_sizes_values = list(average_sizes.values())

    plt.bar(extensions, average_sizes_values)
    plt.xlabel('File Type')
    plt.ylabel('Average Size')
    plt.title('Average File Size by File Type')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def plot_total_size_by_type(data):
    total_sizes = {}
    for file_data in data:
        if file_data.extension not in total_sizes:
            total_sizes[file_data.extension] = 0
        total_sizes[file_data.extension] += file_data.length
    
    extensions = list(total_sizes.keys())
    total_sizes_values = list(total_sizes.values())

    plt.bar(extensions, total_sizes_values)
    plt.xlabel('File Type')
    plt.ylabel('Total Size')
    plt.title('Total File Size by File Type')
    plt.xticks(rotation=45, ha='right')
    plt.show()

def print_top_10_types(average_sizes, data):
    sorted_types = sorted(average_sizes.items(), key=lambda x: x[1], reverse=True)
    top_10_types = sorted_types[:10]

    print("Top 10 File Types by Average Size:")
    print("Type\t\tFile Count\tAverage Size\tTotal Size")
    print("------------------------------------------------------------")
    for file_type, average_size in top_10_types:
        files_of_type = [file_data for file_data in data if file_data.extension == file_type]
        count_files = len(files_of_type)

        print(f"{file_type}\t{count_files}\t\t{average_size:.2f} bytes")

def print_top_10_types_by_total_size(data):
    total_sizes = {}
    for file_data in data:
        if file_data.extension not in total_sizes:
            total_sizes[file_data.extension] = 0
        total_sizes[file_data.extension] += file_data.length
    
    sorted_types = sorted(total_sizes.items(), key=lambda x: x[1], reverse=True)
    top_10_types = sorted_types[:10]

    print("\n\n\n\nTop 10 File Types by Total Size:")
    print("Type\t\tFile Count\tTotal Size")
    print("--------------------------------------------")
    for file_type, total_size in top_10_types:
        count_files = sum(1 for file_data in data if file_data.extension == file_type)
        print(f"{file_type}\t{count_files}\t\t{total_size:,} bytes")

def plot_file_count_by_size(data):
    file_counts = {
        '(0; 1e1] bytes': 0,
        '[1e1; 1e2) bytes': 0,
        '[1e2; 1e3) bytes': 0,
        '[1e3; 1e4) bytes': 0,
        '[1e4; 1e5) bytes': 0,
        '[1e5; 1e6) bytes': 0,
        '[1e6; inf) bytes': 0
    }

    full_num = 0
    for file_data in data:
        size = file_data.length
        full_num += 1
        if size < 10:
            file_counts['(0; 1e1] bytes'] += 1
        elif size >= 10 and size < 100:
            file_counts['[1e1; 1e2) bytes'] += 1
        elif size >= 100 and size < 1000:
            file_counts['[1e2; 1e3) bytes'] += 1
        elif size >= 1e3 and size < 1e4:
            file_counts['[1e3; 1e4) bytes'] += 1
        elif size >= 1e4 and size < 1e5:
            file_counts['[1e4; 1e5) bytes'] += 1
        elif size >= 1e5 and size < 1e6:
            file_counts['[1e5; 1e6) bytes'] += 1
        elif size >= 1e6:
            file_counts['[1e6; inf) bytes'] += 1
    
    #print into console
    
    print("\n\n\n\nFile Count by Size Ranges:")
    for size_range, count in file_counts.items():
        print(f"{size_range}:\t{count} files")

    print(f"The size of {round((file_counts['[1e2; 1e3) bytes'] + file_counts['[1e3; 1e4) bytes'])/full_num*100, 1)}% of the files belongs to the range [100; 10000) bytes")
    #...
    labels = list(file_counts.keys())
    values = list(file_counts.values())

    plt.bar(labels, values)
    plt.xlabel('File Size Ranges')
    plt.ylabel('File Count')
    plt.title('File Count by Size Ranges')
    plt.xticks(rotation=45, ha='right')
    plt.show()


if __name__ == "__main__":
    csv_file = 'file_info_d.csv'
    data = read_csv_file(csv_file)
    average_sizes = calculate_average_size(data)
    print_top_10_types(average_sizes, data)
    print_top_10_types_by_total_size(data)

    plot_average_size_size_by_type(average_sizes)
    plot_total_size_by_type(data)
    plot_file_count_by_size(data)
