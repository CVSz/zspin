from __future__ import annotations

import time
from concurrent import futures

import grpc
import zspin.raft.rpc_pb2 as pb2
import zspin.raft.rpc_pb2_grpc as pb2_grpc


class RaftService(pb2_grpc.RaftServicer):
    def __init__(self, node) -> None:
        self.node = node

    def RequestVote(self, request, context):  # noqa: N802
        granted = False
        if request.term >= self.node.term:
            self.node.term = request.term
            granted = True
        return pb2.VoteReply(vote_granted=granted, term=self.node.term)

    def AppendEntries(self, request, context):  # noqa: N802
        self.node.last_heartbeat = time.time()
        self.node.append_entry(request.entry)
        return pb2.AppendReply(success=True)


def serve(node, port: int) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_RaftServicer_to_server(RaftService(node), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()
