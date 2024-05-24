import grpc
from concurrent import futures
import kmeans_pb2
import kmeans_pb2_grpc
import os

mapper_ports = [50052, 50053]

class ReducerServicer(kmeans_pb2_grpc.KMeansServiceServicer):
    
    def __init__(self, ):
        self.reducer_id = None 

    def InvokeReducers(self, request, context):
        print("Received request to invoke reducers:", request)
        
        # Placeholder for reducer logic
        self.reducer_id= request.reducer_id 
        
        partitions_all = []

        for mapper in mapper_ports:
            partition = self.call_mapper(mapper) 
            partitions_all.extend(partition)

        print("Received partition values from mapper:", partitions_all)

        
        # Return a success response
        return kmeans_pb2.StatusResponse(
            status_code=kmeans_pb2.StatusResponse.SUCCESS,
            status_message="Reducers invoked successfully."
        )

    def call_mapper(self, mapper_port):
        # Connect to the mapper using gRPC
        channel = grpc.insecure_channel(f"localhost:{mapper_port}")  # Adjust the address/port
        
        # Create a stub for the mapper service
        stub = kmeans_pb2_grpc.KMeansServiceStub(channel)
        
        # Send a request to the mapper
        request = kmeans_pb2.MapperRequest(reducer_id=self.reducer_id)
        response = stub.GetPartitionFileValues(request)
        
        # Extract partition values from the response
        partition = []
        for partition_value in response.partition_values:
            centroid_id = partition_value.centroid_id
            x = partition_value.x
            y = partition_value.y
            partition.append([centroid_id, [x, y]])
        
        return partition


    def run_server(self, port):
        # Start the gRPC server for reducers
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        kmeans_pb2_grpc.add_KMeansServiceServicer_to_server(self, server)
        server.add_insecure_port("[::]:{}".format(port))
        print("Reducer server started. Listening on port {}...".format(port))
        server.start()
        server.wait_for_termination()
        
    def shuffle_sort(self, int_pairs):
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
    
    def reduce(self, key, values):
        # reducer_id = 0
        # Calculate the updated centroid
        centroid = self.calculate_centroid(values)
        print(f"Reducer {self.reducer_id} - Key: {key}, Centroid: {centroid}")
        # Write the key and centroid to the reducer's directory
        output_dir = f"Reducers"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Reducer {self.reducer_id} - Creating directory: {output_dir}")
        output_file = os.path.join(output_dir, f"R{self.reducer_id}.txt")
        print(f"Reducer {self.reducer_id} - Writing to file: {output_file}")
        with open(output_file, "a") as f:
            f.write(f"{key},{centroid[0]},{centroid[1]}\n")
            print(f"Reducer {self.reducer_id} - Writing to file: {key}\t{centroid[0]},{centroid[1]}")

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
        

def main():
    # Take input from the reducer regarding the port on which it wants to run
    reducer_port = int(input("Enter the port number for the reducer server: "))

    # Initialize the reducer servicer
    reducer_servicer = ReducerServicer()

    # Start the reducer server
    reducer_servicer.run_server(reducer_port)

if __name__ == "__main__":
    main()
