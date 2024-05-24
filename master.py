import grpc
from concurrent import futures
import kmeans_pb2
import kmeans_pb2_grpc
import random
import shutil
import os
import time
import threading 
import logging


current = [] 
mapper_ports = []  
reducer_ports = [] 
num_centroids=2 
iteration=2

logging.basicConfig(filename='dump.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s')


def read_points_from_file(file_path):
    # Read points from file
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            points.append((x, y))
    return points

def divide_points(points, num_mappers):
    # Divide points equally among the mappers
    chunk_size = len(points) // num_mappers
    divided_points = [points[i:i+chunk_size] for i in range(0, len(points), chunk_size)]
    return divided_points

def select_centroids(points):
    # Randomly select centroids from the points
    global num_centroids 
    return random.sample(points, num_centroids)


# def send_parameters_to_mapper(host, port, request):
#     # Create gRPC channel to connect to mapper
#     channel = grpc.insecure_channel(f"{host}:{port}")
#     stub = kmeans_pb2_grpc.KMeansServiceStub(channel)

#     # Send parameter request to mapper
#     response = stub.SendParameters(request)
#     print(f"Response from mapper on port {port}: {response.status_message}")
#     return response 

# def start_map_reduce(centroids, mapper_ports, divided_points ):
    
#     responses = []
#     for i, port in enumerate(mapper_ports):
#         start_index = i * len(divided_points[i])
#         end_index = (i + 1) * len(divided_points[i]) - 1
#         request = kmeans_pb2.ParametersRequest(
#             start_line_number=start_index,
#             end_line_number=end_index,
#             centroids=[kmeans_pb2.CentroidInfo(centroid_id=j + 1, x=x, y=y) for j, (x, y) in enumerate(centroids)],
#             num_reducers=2
#         ) 
#         response = send_parameters_to_mapper("localhost", port, request)
#         responses.append(response)

#     call_reducers()
# def send_parameters_to_mapper(host, port, request):
#     # Create gRPC channel to connect to mapper
#     channel = grpc.insecure_channel(f"{host}:{port}")
#     stub = kmeans_pb2_grpc.KMeansServiceStub(channel)

#     # Send parameter request to mapper
#     response = stub.SendParameters(request)
#     print(f"Response from mapper on port {port}: {response.status_message}")
#     return response 

def send_parameters_to_mapper(host, port, request, responses, responded_mappers):
    try:
        logging.info(f"Calling mapper on port {port}")

        # Create gRPC channel to connect to mapper
        channel = grpc.insecure_channel(f"{host}:{port}")
        stub = kmeans_pb2_grpc.KMeansServiceStub(channel)

        # Send parameter request to mapper
        response = stub.SendParameters(request)
        print(f"Response from mapper on port {port}: {response.status_message}")
        responses.append(response)
        responded_mappers.append(port)
        logging.info(f"Response from mapper on port {port}: {response.status_message}")

    except grpc.RpcError as e:
        logging.error(f"Error while communicating with mapper on port {port}: {e}")
    except Exception as e:
        logging.error(f"An error occurred while communicating with mapper on port {port}: {e}")
        
    if random.random() < 0.5:
        raise Exception("Error")
        
    
    


# def send_parameters_thread(host, port, request, responses, responded_mappers):
#     response = send_parameters_to_mapper(host, port, request)
#     responses.append(response)
#     responded_mappers.append(port)

def start_map_reduce(centroids, mapper_ports, divided_points,numberofreducer, timeout=10):
    responses = []
    threads = []
    responded_mappers = []

    for i, port in enumerate(mapper_ports):
        start_index = i * len(divided_points[i])
        end_index = (i + 1) * len(divided_points[i]) - 1
        request = kmeans_pb2.ParametersRequest(
            start_line_number=start_index,
            end_line_number=end_index,
            centroids=[kmeans_pb2.CentroidInfo(centroid_id=j + 1, x=x, y=y) for j, (x, y) in enumerate(centroids)],
            num_reducers=numberofreducer
        ) 
        # Create a thread for sending parameters to each mapper
        thread = threading.Thread(target=send_parameters_to_mapper, args=("localhost", port, request, responses, responded_mappers))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # time.sleep(6)  
    # Wait for all threads to finish or until timeout
    start_time = time.time()
    while time.time() - start_time < timeout and len(responses) < len(mapper_ports):
        time.sleep(3)  # Sleep for a short duration to avoid busy waiting

    # Check if any mapper has not responded
    missing_mappers = [port for port in mapper_ports if port not in responded_mappers]
    print("##########################")
    print("missing mappers, ", missing_mappers) 
    print("responded mapper, ", responded_mappers)
    print("printing responses, ",  responses) 
    
    if missing_mappers:
        print(f"Mappers {missing_mappers} did not respond. Reassigning workload...")
        for i, port in enumerate(missing_mappers):
            # Reassign workload to a mapper that has responded
            new_port = responded_mappers[i % len(responded_mappers)]
            print(f"Reassigning workload of mapper {port} to mapper {new_port}")
            start_index = i * len(divided_points[i])
            end_index = (i + 1) * len(divided_points[i]) - 1
            request = kmeans_pb2.ParametersRequest(
                start_line_number=start_index,
                end_line_number=end_index,
                centroids=[kmeans_pb2.CentroidInfo(centroid_id=j + 1, x=x, y=y) for j, (x, y) in enumerate(centroids)],
                num_reducers=2
            ) 
            # Send parameters to the new mapper
            response = send_parameters_to_mapper("localhost", new_port, request,responses, responded_mappers)
            responses.append(response)

    # Wait for all threads to finish
    responded_mappers_final  = list(set(responded_mappers)) 
    invoke_reducers(responded_mappers_final)
    print("returning all the responses") 
    
    return responses



def are_same(list1, list2):
    print("list1:", list1)
    print("list2:", list2)
    if len(list1) != len(list2):
        print("lengths are different")
        return False  # If the lists have different lengths, return False

    for tuple1, tuple2 in zip(list1, list2):
        x1, y1 = tuple1
        x2, y2 = tuple2
        if abs(x1 - x2) + abs(y1 - y2) >= 0.0001:
            return False  # If the condition is not satisfied for any pair, return False

    print("centroids are same")
    return True  # If the condition is satisfied for all pairs, return True

def clear_data_folder(data_folder):
    for item in os.listdir(data_folder):
        item_path = os.path.join(data_folder, item)
        if os.path.isdir(item_path) and item != 'Input':
            shutil.rmtree(item_path)
        elif os.path.isfile(item_path) and item != 'Input':
            os.remove(item_path)

def main():
    # Set the number of mappers
    

    # Read points from file
    input_file_path = "Data/Input/points2.txt"  # Adjust the path as per your file location
    points = read_points_from_file(input_file_path)

    # Divide points equally among the mappers
    divided_points = divide_points(points, len(mapper_ports))

    
    # Select centroids from the points
    # previous = select_centroids(points)
    global current
    # print(are_same(current, previous)) 
    current = select_centroids(points)
    previous = [] 
    data_folder = 'Data'
    
    
    global iteration 
    print("current values", current)
    print("previous values", previous) 
    while (iteration >0 and (not are_same(current, previous))  ) :
        

        # Clear the contents of the Data folder
        
        # time.sleep(0.5)
        clear_data_folder(data_folder)
        temp_current = [i for i in current]
        print("temp current before", temp_current)
        logging.info("Starting map-reduce process for iteration %d", iteration)

        start_map_reduce(current, mapper_ports, divided_points,len(reducer_ports) )
        logging.info("Completed map-reduce process for iteration %d", iteration)
        logging.info("Centroids for iteration %d: %s", iteration, current)

        print("before starting next iteration ")
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        time.sleep(5)
        iteration = iteration - 1
        
        print("temp current after, ", temp_current) 
        previous = temp_current 


# def invoke_reducers(responded_mappers):
#      # Specify the ports where reducers are running
#     num_reducers = len(reducer_ports)
#     # responded_reducers = [] 
#     responded_id = [] 
    
#     for i in range(0, len(reducer_ports)):
#         # Establish gRPC channel to connect to the reducer
        
#         try:
#             channel = grpc.insecure_channel(f"localhost:{reducer_ports[i]}")
#             stub = kmeans_pb2_grpc.KMeansServiceStub(channel)
            
#             # Create a ReducerRequest message
#             reducer_request = kmeans_pb2.ReducerRequest(num_reducers=reducer_ports[i], reducer_id=i, mapper_ports=responded_mappers) 
            
#             # Invoke the reducers by sending the ReducerRequest
#             response = stub.InvokeReducers(reducer_request)
#             # print(f"Response from reducer on port {reducer_ports[i]}: {response.status_message}")
#             responded_id.append(i) 
        
#             # Print the new centroids
#             for centroid in response.partition_values:
#                 # centroid_values[centroid.centroid_id][0] = centroid.x
#                 # centroid_values[centroid.centroid_id][0] = centroid.y
#                 centroid_tupe = (centroid.x, centroid.y)
#                 print(int(centroid.centroid_id)) 
#                 # print(centroid_values) 
#                 global current
#                 # print(centroid_values)
#                 current[int(centroid.centroid_id)] = centroid_tupe
#         except grpc.RpcError as e:
#             print("reducers did not respond") 
#             # print(f"New centroid: centroid_id={centroid.centroid_id}, x={centroid.x}, y={centroid.y}")
#             # print(centroid_values) 

    
#     missing_reducers = [port for port in range(0, len(reducer_ports)) if port not in responded_id]
#     if missing_reducers:
#         print("Missing reducers:", missing_reducers)
#         for missing_reducer_id in missing_reducers:
#             for responded_id in responded_id:
#                 try:
#                     channel = grpc.insecure_channel(f"localhost:{reducer_ports[responded_id]}")
#                     stub = kmeans_pb2_grpc.KMeansServiceStub(channel)
                    
#                     # Resend request to a reducer that has responded
#                     reducer_request = kmeans_pb2.ReducerRequest(num_reducers=reducer_ports[responded_id], reducer_id=missing_reducer_id, mapper_ports=responded_mappers)
#                     response = stub.InvokeReducers(reducer_request)
#                     print(f"Response from reducer on port {reducer_ports[responded_id]} for reducer {missing_reducer_id}") 
#                     for centroid in response.partition_values:
#                     # centroid_values[centroid.centroid_id][0] = centroid.x
#                     # centroid_values[centroid.centroid_id][0] = centroid.y
#                         centroid_tupe = (centroid.x, centroid.y)
#                         print(int(centroid.centroid_id)) 
#                         # print(centroid_values) 
                        
#                         # print(centroid_values)
#                         current[int(centroid.centroid_id)] = centroid_tupe
#                     break  # Exit the inner loop once a response is received
#                 except grpc.RpcError as e:
#                     print(f"Error invoking reducer on port {reducer_ports[responded_id]} for reducer {missing_reducer_id}: {e}")

def invoke_reducer_thread(reducer_id, reducer_port, responded_mappers, responded_id):
    try:
        logging.info(f"Calling reducer on port {reducer_port}")

        channel = grpc.insecure_channel(f"localhost:{reducer_port}")
        stub = kmeans_pb2_grpc.KMeansServiceStub(channel)
        
        # Create a ReducerRequest message
        reducer_request = kmeans_pb2.ReducerRequest(num_reducers=reducer_port, reducer_id=reducer_id, mapper_ports=responded_mappers) 
        
        # Invoke the reducer by sending the ReducerRequest
        response = stub.InvokeReducers(reducer_request)
        responded_id.append(reducer_id) 
        # Print the new centroids
        for centroid in response.partition_values:
            centroid_tuple = (centroid.x, centroid.y)
            print(int(centroid.centroid_id)) 
            global current
            current[int(centroid.centroid_id)] = centroid_tuple
        logging.info(f"Response from reducer on port {reducer_port}")

    except grpc.RpcError as e:
        logging.info(f"Error Response from reducer on port {reducer_port}")
        print(f"Error invoking reducer on port {reducer_port} for reducer {reducer_id}: {e}")
        
    if random.random() < 0.5:
        raise Exception("Error")

def invoke_reducers(responded_mappers):
    # Specify the ports where reducers are running
    # reducer_ports = [50054, 50055]  # Example reducer ports
    num_reducers = len(reducer_ports)
    responded_id = [] 
    
    threads = []
    for i, port in enumerate(reducer_ports):
        thread = threading.Thread(target=invoke_reducer_thread, args=(i, port, responded_mappers, responded_id))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    missing_reducers = [port for port in range(0, len(reducer_ports)) if port not in responded_id]
    if missing_reducers:
        print("Missing reducers:", missing_reducers)
        for missing_reducer_id in missing_reducers:
            for responded_id in responded_id:
                try:
                    channel = grpc.insecure_channel(f"localhost:{reducer_ports[responded_id]}")
                    stub = kmeans_pb2_grpc.KMeansServiceStub(channel)
                    
                    # Resend request to a reducer that has responded
                    reducer_request = kmeans_pb2.ReducerRequest(num_reducers=reducer_ports[responded_id], reducer_id=missing_reducer_id, mapper_ports=responded_mappers)
                    response = stub.InvokeReducers(reducer_request)
                    print(f"Response from reducer on port {reducer_ports[responded_id]} for reducer {missing_reducer_id}") 
                    for centroid in response.partition_values:
                        centroid_tuple = (centroid.x, centroid.y)
                        print(int(centroid.centroid_id)) 
                        global current
                        current[int(centroid.centroid_id)] = centroid_tuple
                    logging.info(f"Response from reducer on port {reducer_ports[responded_id]}")
                    break  # Exit the inner loop once a response is received
                except grpc.RpcError as e:
                    logging.info(f"Error Response from reducer on port {reducer_ports[responded_id]}")
                    print(f"Error invoking reducer on port {reducer_ports[responded_id]} for reducer {missing_reducer_id}: {e}")
                    
                
    

    
        # Print the response from the reducer
        # print(f"Response from reducer on port {reducer_ports[i]}: {response.status_message}")


# def call_reducers():
#     reducer_ports = [50054, 50055]  # Specify the ports where reducers are running
#     num_reducers = len(reducer_ports)  # Specify the number of reducers

#     invoke_reducers(reducer_ports, num_reducers)

    # Logic to invoke reducers goes here
    # pass  # Placeholder for reducer invocation logic


if __name__ == "__main__":
        # Ask user for the number of mapper ports
    num_mapper_ports = int(input("Enter the number of mapper ports: "))
    # Ask user to input mapper ports
    mapper_ports = []
    for i in range(num_mapper_ports):
        port = int(input(f"Enter mapper port {i + 1}: "))
        mapper_ports.append(port)

    # Ask user for the number of reducer ports
    num_reducer_ports = int(input("Enter the number of reducer ports: "))
    # Ask user to input reducer ports
    reducer_ports = []
    for i in range(num_reducer_ports):
        port = int(input(f"Enter reducer port {i + 1}: "))
        reducer_ports.append(port)

    # Ask user for the number of centroids
    num_centroids = int(input("Enter the number of centroids: "))
    iteration = int(input("Enter number of iterations to calculate centroids: "))
    # Now you can use these values as needed
    print("Mapper ports:", mapper_ports)
    print("Reducer ports:", reducer_ports)
    print("Number of centroids:", num_centroids)

    main() 
