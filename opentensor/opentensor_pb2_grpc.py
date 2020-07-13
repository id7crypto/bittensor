# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from opentensor import opentensor_pb2 as opentensor_dot_opentensor__pb2


class OpentensorStub(object):
    """Runtime protocol definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Fwd = channel.unary_unary(
                '/Opentensor/Fwd',
                request_serializer=opentensor_dot_opentensor__pb2.TensorMessage.SerializeToString,
                response_deserializer=opentensor_dot_opentensor__pb2.TensorMessage.FromString,
                )
        self.Bwd = channel.unary_unary(
                '/Opentensor/Bwd',
                request_serializer=opentensor_dot_opentensor__pb2.TensorMessage.SerializeToString,
                response_deserializer=opentensor_dot_opentensor__pb2.TensorMessage.FromString,
                )


class OpentensorServicer(object):
    """Runtime protocol definition.
    """

    def Fwd(self, request, context):
        """Forward tensor request. 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Bwd(self, request, context):
        """Reverse tensor (gradient) request.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OpentensorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Fwd': grpc.unary_unary_rpc_method_handler(
                    servicer.Fwd,
                    request_deserializer=opentensor_dot_opentensor__pb2.TensorMessage.FromString,
                    response_serializer=opentensor_dot_opentensor__pb2.TensorMessage.SerializeToString,
            ),
            'Bwd': grpc.unary_unary_rpc_method_handler(
                    servicer.Bwd,
                    request_deserializer=opentensor_dot_opentensor__pb2.TensorMessage.FromString,
                    response_serializer=opentensor_dot_opentensor__pb2.TensorMessage.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Opentensor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Opentensor(object):
    """Runtime protocol definition.
    """

    @staticmethod
    def Fwd(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Opentensor/Fwd',
            opentensor_dot_opentensor__pb2.TensorMessage.SerializeToString,
            opentensor_dot_opentensor__pb2.TensorMessage.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Bwd(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Opentensor/Bwd',
            opentensor_dot_opentensor__pb2.TensorMessage.SerializeToString,
            opentensor_dot_opentensor__pb2.TensorMessage.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)


class MetagraphStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Gossip = channel.unary_unary(
                '/Metagraph/Gossip',
                request_serializer=opentensor_dot_opentensor__pb2.AxonBatch.SerializeToString,
                response_deserializer=opentensor_dot_opentensor__pb2.AxonBatch.FromString,
                )


class MetagraphServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Gossip(self, request, context):
        """Shared POW cache.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MetagraphServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Gossip': grpc.unary_unary_rpc_method_handler(
                    servicer.Gossip,
                    request_deserializer=opentensor_dot_opentensor__pb2.AxonBatch.FromString,
                    response_serializer=opentensor_dot_opentensor__pb2.AxonBatch.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Metagraph', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Metagraph(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Gossip(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Metagraph/Gossip',
            opentensor_dot_opentensor__pb2.AxonBatch.SerializeToString,
            opentensor_dot_opentensor__pb2.AxonBatch.FromString,
            options, channel_credentials,
            call_credentials, compression, wait_for_ready, timeout, metadata)
