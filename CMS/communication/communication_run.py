import communication_server
import communication_client
import route
import communication_pb2_grpc
import communication_pb2
import grpc
from concurrent import futures

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service = communication_server.CommunicationServicer()
    communication_pb2_grpc.add_CommunicationServicer_to_server(service, server)
    
    port = 50001
    server.add_insecure_port("[::]:" + str(port))
    server.start()
    server.wait_for_termination()

