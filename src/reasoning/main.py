# import concurrent.futures as futures
# import time
# import grpc
# import telemetry_pb2
# import telemetry_pb2_grpc

# class cogntiveReasoningService():
#     def __init__(self):
#         # In-memory target matrix tracking active threats
#         self.active_threat_matrix = {}
#         print("[INIT] Cognitive Reasoning layer initialized ")
    
#     def streamTargets(self, request, context):
#         system_id = request.system_id
#         timestamp = request.timestamp

#         # Track target state footprint
#         target_uid = f"{request_domain}_{system_id}_{timestamp} "

#         # Unpack kinematic payload metrics
#         target_metrics = {
#             "latitude":request.latitude,
#             "longitude":request.longitude,
#             "altitude":request.altitude_meters,
#             "velocity_knots":request.velocity_knots,
#             "domain": telemetry_pb2.ThreatDomain.Name(request_domain)
#         }

#         # Store state locally in the matrix tracker
#         self.active_threat_matrix[target_uid] = target_metrics
#         active_count = len(self.active_threat_matrix)

#         print(f"\n[TARGET INGESTED] Source: {system_id} | Domain: {target_metrics['domain']}")
#         print(f" > Coordinates: [{target_metrics['latitude']}, {target_metrics['longitude']}]")
#         print(f" > Altitude:    {target_metrics['altitude']} meters")
#         print(f" > Kinematics:  {target_metrics['velocity_knots']} knots")
#         print(f" > Global Threat Matrix State Matrix Count: {active_count}")

#         # Construct and return tactical acknowledgement envelope

#         response = telemetry_pb2.IngestionResponse(
#             status_acknowledged=True,
#             active_target_count=active_count
#         )
#         return response

#     def serve_tactical_node():
#         # Instantiate thread pool to process parallel incoming streams concurrently
#         server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
#         telemetry_pb2_grpc.add_TelemetryStreamServicer_to_server(CognitiveReasoningService(), server)
        
#         # Bind to loopback port matched with C++ transport layer configuration
#         server.add_insecure_port('127.0.0.1:50051')
#         server.start()
#         print("[SERVER RUNNING] PHALANX Inter-Process Gateway listening on 127.0.0.1:50051")
        
#         try:
#             while True:
#                 time.sleep(86400) # Keep execution thread alive
#         except KeyboardInterrupt:
#             print("\n[SHUTDOWN] Terminating tactical node operations cleanly...")
#             server.stop(0)

# if __name__ == '__main__':
#     serve_tactical_node()

import concurrent.futures as futures
import time
import grpc
import telemetry_pb2
import telemetry_pb2_grpc
from vector_store import PureTacticalVectorStore

class CognitiveReasoningService(telemetry_pb2_grpc.TelemetryStreamServicer):
    def __init__(self):
        # In-memory target matrix tracking active threats
        self.active_threat_matrix = {}
        
        # Instantiate and seed our zero-dependency local vector store
        self.vector_store = PureTacticalVectorStore()
        self.vector_store.seed_rules_of_engagement()
        
        print("[INIT] Cognitive Reasoning Layer initialized. Awaiting tactical data feeds...")

    def StreamTargets(self, request, context):
        system_id = request.system_id
        timestamp = request.timestamp
        domain_name = telemetry_pb2.ThreatDomain.Name(request.domain)
        
        # Track unique target signature state footprint
        target_uid = f"{domain_name}_{system_id}_{timestamp}"
        
        # 1. Map raw multi-domain kinematics values into a localized normalized vector footprint
        # Mapping parameters: [Domain Weight, Timestamp Delta, Altitude Metric, Kinematic Velocity]
        normalized_vector = [0.0, 0.0, 0.0, 0.0]
        
        if request.domain == telemetry_pb2.AIR:
            normalized_vector = [0.88, 0.10, 0.82, 0.45] # High-altitude, fast tracking profile
        elif request.domain == telemetry_pb2.MARITIME:
            normalized_vector = [0.12, 0.88, 0.18, 0.68] # Subsurface/Surface tracking profile
        else:
            normalized_vector = [0.20, 0.10, 0.10, 0.10] # Baseline standard profile

        # 2. Query our air-gapped vector search matrix engine
        evaluation = self.vector_store.evaluate_threat_vector(normalized_vector)

        # 3. Store the aggregated intelligence matrix state locally
        target_metrics = {
            "latitude": request.latitude,
            "longitude": request.longitude,
            "altitude": request.altitude_meters,
            "velocity_knots": request.velocity_knots,
            "domain": domain_name,
            "matched_rule": evaluation["matched_rule_id"],
            "directive": evaluation["action_directive"],
            "confidence": evaluation["confidence_score"]
        }
        
        self.active_threat_matrix[target_uid] = target_metrics
        active_count = len(self.active_threat_matrix)

        # 4. Print clean tactical state readout to the interface console
        print(f"\n[TARGET INGESTED & FUSED] Source: {system_id} | Domain: {target_metrics['domain']}")
        print(f" > Coordinates:  [{target_metrics['latitude']}, {target_metrics['longitude']}]")
        print(f" > Metrics:      {target_metrics['altitude']}m @ {target_metrics['velocity_knots']} knots")
        print(f" > Vector Match: {target_metrics['matched_rule']} (Confidence: {target_metrics['confidence']*100}%)")
        print(f" > AI Directive: \033[91m{target_metrics['directive']}\033[0m")
        print(f" > Global Threat Matrix State Count: {active_count}")

        # Construct and return tactical acknowledgement envelope back across gRPC channel
        response = telemetry_pb2.IngestionResponse(
            status_acknowledged=True,
            active_target_count=active_count
        )
        return response

def serve_tactical_node():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    telemetry_pb2_grpc.add_TelemetryStreamServicer_to_server(CognitiveReasoningService(), server)
    server.add_insecure_port('127.0.0.1:50051')
    server.start()
    print("[SERVER RUNNING] PHALANX Inter-Process Gateway listening on 127.0.0.1:50051")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Terminating tactical node operations cleanly...")
        server.stop(0)

if __name__ == '__main__':
    serve_tactical_node()



    