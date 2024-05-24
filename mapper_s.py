import grpc
from concurrent import futures
import kmeans_pb2
import kmeans_pb2_grpc
import os 
import time 

class MapperServicer(kmeans_pb2_grpc.KMeansServiceServicer):
    
    def __init__(self, mapper_id):
        self.mapper_id = mapper_id    
        self.partition_dir = "" 
        
    def SendParameters(self, request, context):
        # Print the received parameters
        print("Received parameters from master:")
        print("Start line number:", request.start_line_number)
        print("End line number:", request.end_line_number)
        print("Centroids:")
        centroid_coordinates = []
        
        
        # Extract centroid coordinates and add them to the list
        for centroid_info in request.centroids:
            centroid_coordinates.append([centroid_info.x, centroid_info.y])
            # print(f"Centroid ID: {centroid_info.centroid_id}, X: {centroid_info.x}, Y: {centroid_info.y}")
            # print("Number of reducers:", request.num_reducers)

        print(centroid_coordinates)
        
        print("########################################")
        # time.sleep(5)
        print("sleep time finish")
        print("request.num_reducers", request.num_reducers)
        self.map1(request.start_line_number, request.end_line_number, centroid_coordinates, request.num_reducers)
        # Send a response back to the master
        
        print("successfull printing") 
        return kmeans_pb2.StatusResponse(status_code=kmeans_pb2.StatusResponse.SUCCESS, status_message="Parameters received successfully")

    def GetPartitionFileValues(self, request, context):
        # Read the partition file based on the reducer ID
        partition_file_path = os.path.join(self.partition_dir, f"partition_{request.reducer_id}.txt")
        # partition_file_path = os.path.join("mapper_50052", f"partition{request.reducer_id}.txt")
        
        print(partition_file_path)
        partition_values = self.read_partition_file(partition_file_path)
        
        print("got the correct partition values")
        print(partition_values) 
        # Prepare the response message
        response = kmeans_pb2.PartitionFileResponse(partition_values=partition_values)
        print("sending response") 
        return response
    
    def read_partition_file(self, file_path):
        # Read partition file and extract values
        partition_values = []
        with open(file_path, 'r') as file:
            print("am i reading file path") 
            for line in file:
                
                parts = line.strip().split(',')
                if len(parts) != 3:
                    # Skip lines that don't have three parts
                    continue
                
                try:
                    # Parse centroid_id, x, and y
                    centroid_id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])

                    # Create a PartitionValue instance and append it to partition_values list
                    partition_values.append(kmeans_pb2.PartitionValue(centroid_id=centroid_id, x=x, y=y))
                except ValueError:
                    # Handle parsing errors, e.g., if x or y cannot be converted to float
                    print(f"Error parsing line: {line.strip()}")
        return partition_values


    def run_server(self, port):
        # Start the gRPC server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        kmeans_pb2_grpc.add_KMeansServiceServicer_to_server(self, server)
        server.add_insecure_port("[::]:{}".format(port))
        print("Mapper server started. Listening on port {}...".format(port))
        server.start()
        server.wait_for_termination()
        
    def map1(self, start_idx, end_idx, centroids, num_reducers):
        print("map start")
        input_file = "Data/Input/points2.txt"
        output_data = []

        with open(input_file, "r") as f:
            points = f.readlines()[start_idx:end_idx+1]

        print("Points:", points)
        
        for point in points:
            x, y = map(float, point.strip().split(","))
            nearest_centroid_idx = self.get_nearest_centroid_index(x, y, centroids)
            output_data.append((nearest_centroid_idx, (x, y)))
            print(f"Point ({x}, {y}) assigned to centroid {nearest_centroid_idx}")

        print("Output data:", output_data  )
        self.partition(output_data, num_reducers)

    def get_nearest_centroid_index(self, x, y, centroids):
        print("inside get_nearest_centroid_index")
        min_distance = float('inf')
        nearest_centroid_idx = -1
        for idx, centroid in enumerate(centroids):
            centroid_x, centroid_y = centroid
            distance = (x - centroid_x) ** 2 + (y - centroid_y) ** 2
            if distance < min_distance:
                min_distance = distance
                nearest_centroid_idx = idx
        return nearest_centroid_idx

    def partition(self, output_data, num_reducers):
        print("inside partition")
        for key, value in output_data:
            print("inside for loop")
            print(key)
            # print(num_reducers) 
            reducer_idx = key % num_reducers            
            
            # partition_dir = f"Data/Mappers/M{self.mapper_id}"
            partition_dir = os.path.join("Data", "Mappers", f"M{self.mapper_id}")

            self.partition_dir = partition_dir
            print(partition_dir) 
            if not os.path.exists(partition_dir):
                os.makedirs(partition_dir)
            
            file_name_reducer =f"partition_{reducer_idx}.txt"
            partition_file = os.path.join(partition_dir, file_name_reducer) 
            
            with open(partition_file, "a") as f:
                f.write(f"{key},{value[0]},{value[1]}\n")

                print(f"Writing to partition file {partition_file}: {key}\t{value[0]},{value[1]}")

                    
def main():
    # Take input from the mapper regarding the port on which it wants to run
    mapper_port = int(input("Enter the port number for the mapper server: "))

    # Initialize the mapper servicer
    mapper_servicer = MapperServicer(mapper_port)

    # Start the mapper server
    mapper_servicer.run_server(mapper_port)

if __name__ == "__main__":
    main()
