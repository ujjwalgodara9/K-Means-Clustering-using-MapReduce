# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import kmeans_pb2 as kmeans__pb2


class KMeansServiceStub(object):
    """python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. kmeans.proto

    Service definition for communication between master and mapper
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendParameters = channel.unary_unary(
                '/KMeansService/SendParameters',
                request_serializer=kmeans__pb2.ParametersRequest.SerializeToString,
                response_deserializer=kmeans__pb2.StatusResponse.FromString,
                )
        self.StatusUpdate = channel.unary_unary(
                '/KMeansService/StatusUpdate',
                request_serializer=kmeans__pb2.StatusUpdateRequest.SerializeToString,
                response_deserializer=kmeans__pb2.StatusResponse.FromString,
                )
        self.InvokeReducers = channel.unary_unary(
                '/KMeansService/InvokeReducers',
                request_serializer=kmeans__pb2.ReducerRequest.SerializeToString,
                response_deserializer=kmeans__pb2.PartitionFileResponse.FromString,
                )
        self.GetPartitionFileValues = channel.unary_unary(
                '/KMeansService/GetPartitionFileValues',
                request_serializer=kmeans__pb2.MapperRequest.SerializeToString,
                response_deserializer=kmeans__pb2.PartitionFileResponse.FromString,
                )


class KMeansServiceServicer(object):
    """python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. kmeans.proto

    Service definition for communication between master and mapper
    """

    def SendParameters(self, request, context):
        """RPC method for sending necessary parameters from master to mapper
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StatusUpdate(self, request, context):
        """RPC method for receiving status updates from mapper to master
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def InvokeReducers(self, request, context):
        """RPC method for invoking reducers from master
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPartitionFileValues(self, request, context):
        """RPC method for getting partition file values from mapper to reducer
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_KMeansServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendParameters': grpc.unary_unary_rpc_method_handler(
                    servicer.SendParameters,
                    request_deserializer=kmeans__pb2.ParametersRequest.FromString,
                    response_serializer=kmeans__pb2.StatusResponse.SerializeToString,
            ),
            'StatusUpdate': grpc.unary_unary_rpc_method_handler(
                    servicer.StatusUpdate,
                    request_deserializer=kmeans__pb2.StatusUpdateRequest.FromString,
                    response_serializer=kmeans__pb2.StatusResponse.SerializeToString,
            ),
            'InvokeReducers': grpc.unary_unary_rpc_method_handler(
                    servicer.InvokeReducers,
                    request_deserializer=kmeans__pb2.ReducerRequest.FromString,
                    response_serializer=kmeans__pb2.PartitionFileResponse.SerializeToString,
            ),
            'GetPartitionFileValues': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPartitionFileValues,
                    request_deserializer=kmeans__pb2.MapperRequest.FromString,
                    response_serializer=kmeans__pb2.PartitionFileResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'KMeansService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class KMeansService(object):
    """python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. kmeans.proto

    Service definition for communication between master and mapper
    """

    @staticmethod
    def SendParameters(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KMeansService/SendParameters',
            kmeans__pb2.ParametersRequest.SerializeToString,
            kmeans__pb2.StatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StatusUpdate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KMeansService/StatusUpdate',
            kmeans__pb2.StatusUpdateRequest.SerializeToString,
            kmeans__pb2.StatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def InvokeReducers(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KMeansService/InvokeReducers',
            kmeans__pb2.ReducerRequest.SerializeToString,
            kmeans__pb2.PartitionFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPartitionFileValues(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/KMeansService/GetPartitionFileValues',
            kmeans__pb2.MapperRequest.SerializeToString,
            kmeans__pb2.PartitionFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)