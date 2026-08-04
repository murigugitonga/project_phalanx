#include <iostream>
#include <memory>
#include <chrono>
#include <thread>

#include "parser.hpp"

#include <grpcpp/grpcpp.h>
#include "telemetry.pb.h"
#include "telemetry.pb.h"
#include "telemetry.grpc.pb.h"

using grpc::Channel;

using grpc::ClientContext;
using grpc::Status;
using phalanx::TelemetryStream;
using phalanx::TargetPayload;
using phalanx::IngestionResponse;

class PhalanxTransportClient
{
private:
    std::unique_ptr<TelemetryStream::Stub> stub_;

public:
    PhalanxTransportClient(std::shared_ptr<Channel> channel)
     : stub_(TelemetryStream::NewStub(channel)) {}
    
     //~PhalanxTransportClient();
    void ForwardTarget(const phalanx::RawTargetFrame& frame){
        TargetPayload payload;
        payload.set_system_id(frame.system_id);
        payload.set_timestamp(frame.timestamp);
        payload.set_latitude(frame.latitude);
        payload.set_longitude(frame.longitude);
        payload.set_altitude_meters(frame.altitude_meters);
        payload.set_velocity_knots(frame.velocity_knots);
        payload.set_domain(static_cast<phalanx::ThreatDomain>(frame.domain_type));

        IngestionResponse response;
        ClientContext context;

        std::cout << "[IPC LOG] Emitting binary payload package to AI Layer...\n";
        Status status = stub_->StreamTargets(&context, payload, &response);

        if (status.ok()) {
            std::cout << "[IPC SUCCESS] State synchronized. Active targets tracked globally: " 
                      << response.active_target_count() << "\n";
        } else {
            std::cout << "[IPC WARNING] Tactical edge connection degraded: " << status.error_message() << "\n";
            std::cout << " > Initiating temporary local caching sequence...\n";
        }
    }
};

int main() {
    std::cout << "[BOOT] Launching Project PHALANX Edge Engine...\n";

    // Setup transport route targeting the localhost Python gRPC receiver
    PhalanxTransportClient client(grpc::CreateChannel("127.0.0.1:50051", grpc::InsecureChannelCredentials()));

    // Simulated tactical stream data >> "SYSTEM_ID|TIMESTAMP|LAT|LON|ALT|VEL|DOMAIN_ENUM(1=AIR)"
    std::string mock_radar_feed = "RADAR-01|1719792045|-1.2921|36.8219|12450.5|520.4|1";

    // Single-pass processing validation loop
    auto parsed_frame = phalanx::EdgeTelemetryParser::parseStringFrame(mock_radar_feed);
    if (parsed_frame) {
        std::cout << "[PARSE MATCH] Successfully processed " << parsed_frame->system_id << "\n";
        client.ForwardTarget(*parsed_frame);
    }

    return 0;
}
