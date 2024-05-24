import os

def shuffle_sort(int_pairs):
    # Sort the list by key
    int_pairs.sort(key=lambda x: x[0])
    print("Sorted int_pairs:", int_pairs)
    # Group the values that belong to the same key
    final_pairs = []
    current_key = None
    current_values = []
    for key, value in int_pairs:
        if key != current_key:
            if current_key is not None:
                final_pairs.append((current_key, current_values))
                print("Appending to final_pairs:", current_key, current_values)
            current_key = key
            current_values = [value]
        else:
            current_values.append(value)
    if current_key is not None:
        final_pairs.append((current_key, current_values))
        print("Appending to final_pairs end:", current_key, current_values)

    return final_pairs

def reduce(key, values):
    reducer_id = 0
    # Calculate the updated centroid
    centroid = calculate_centroid(values)
    print(f"Reducer {reducer_id} - Key: {key}, Centroid: {centroid}")
    # Write the key and centroid to the reducer's directory
    output_dir = f"Reducers"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Reducer {reducer_id} - Creating directory: {output_dir}")
    output_file = os.path.join(output_dir, f"R{reducer_id}.txt")
    print(f"Reducer {reducer_id} - Writing to file: {output_file}")
    with open(output_file, "a") as f:
        f.write(f"{key},{centroid[0]},{centroid[1]}\n")
        print(f"Reducer {reducer_id} - Writing to file: {key}\t{centroid[0]},{centroid[1]}")

def calculate_centroid(values):
    # Calculate the centroid by averaging the coordinates of all data points
    if not values:
        return None
    sum_x = sum(y[0] for y in values)
    sum_y = sum(y[1] for y in values)
    count = len(values)
    print("count:", count)
    centroid_x = sum_x / count
    centroid_y = sum_y / count
    print("centroid_x:", centroid_x)
    print("centroid_y:", centroid_y)
    return (centroid_x, centroid_y)

# Get the current directory of the file
current_dir = os.path.dirname(os.path.abspath(__file__))

print("Current directory:", current_dir)

int_pairs = [(0, (81.15927937347692,57.750360036814705)),
             (2, (81.430136979439,50.33034624768575)),
             (0, (22.918984884832927,86.29388886815464)),
             (1, (81.430136979439,50.33034624768575)),
             (0, (37.59627649460666,83.10255966867024)),
             (0, (41.94706427555632,76.82403075144262)),
             (1, (2.4253966361924117,14.200140998826638)),            
            (1,	(85.32433236307622,38.85085293948647)),
            (1,	(31.557122052707076,36.90041258086754)),
            (1,	(46.66353476332117,42.536829675995506)),
            (2, (85.32433236307622,38.85085293948647)),
            (1, (65.92469227195072,51.192695664924834)),
            (1,	(88.28421977908025,12.067049557489574)),
            (1,	(2.552573964893323,17.536987084919097))            
            ]

sorted_list = shuffle_sort(int_pairs)
for key, values in sorted_list:
    reduce(key, values)