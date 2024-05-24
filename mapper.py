import grpc
from concurrent import futures
import kmeans_pb2
import kmeans_pb2_grpc

class MapperServicer(kmeans_pb2_grpc.KMeansServiceServicer):
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
            print(f"Centroid ID: {centroid_info.centroid_id}, X: {centroid_info.x}, Y: {centroid_info.y}")
            print("Number of reducers:", request.num_reducers)

        print(centroid_coordinates)
        # Send a response back to the master
        return kmeans_pb2.StatusResponse(status_code=kmeans_pb2.StatusResponse.SUCCESS, status_message="Parameters received successfully")

    def run_server(self, port):
        # Start the gRPC server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        kmeans_pb2_grpc.add_KMeansServiceServicer_to_server(self, server)
        server.add_insecure_port("[::]:{}".format(port))
        print("Mapper server started. Listening on port {}...".format(port))
        server.start()
        server.wait_for_termination()
        
    # def map(self, start_idx, end_idx, centroids):
        

def main():
    # Take input from the mapper regarding the port on which it wants to run
    mapper_port = int(input("Enter the port number for the mapper server: "))

    # Initialize the mapper servicer
    mapper_servicer = MapperServicer()

    # Start the mapper server
    mapper_servicer.run_server(mapper_port)

if __name__ == "__main__":
    main()
