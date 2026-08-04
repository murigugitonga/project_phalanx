#ifndef PARSER_HPP
#define PARSER_HPP

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <memory>
#include <stdexcept>

namespace phalanx {
    struct RawTargetFrame {
        std::string system_id;
        uint64_t timestamp;
        double latitude;
        double longitude;
        double altitude_meters;
        float velocity_knots;
        int domain_type;
    };
    
    class EdgeTelemetryParser
    {

    // Memory-safe stack parsing of delimited raw radar text
    public:
        static std::unique_ptr<RawTargetFrame> parseStringFrame(const std::string& raw_frame) noexcept {
            if(raw_frame.empty()) return nullptr;

            std::vector<std::string> tokens;
            std::stringstream ss(raw_frame);
            std::string token;

            while (std::getline(ss, token, '|')){
                tokens.push_back(token);
            }
            // Enforce structural schema match
            if (tokens.size() !=7){
                std::cerr <<"[SECURITY CRITICAL] Dropped malformed network telemetry packet. \n";
                return nullptr;
            }
            try
            {
                auto frame = std::make_unique<RawTargetFrame>();
                frame->system_id = tokens[0];
                frame->timestamp = std::stoull(tokens[1]);
                frame->latitude = std::stod(tokens[2]);
                frame->longitude = std::stod(tokens[3]);
                frame->altitude_meters = std::stod(tokens[4]);
                frame->velocity_knots = std::stof(tokens[5]);
                frame->domain_type = std::stoi(tokens[6]);
                return frame;
            }
            catch(const std::exception& e)
            {
                std::cerr <<"[SYSTEM PARSER ERROR] Data cast failure: " << e.what() << '\n';
                return nullptr;
            }
            
            
        }
    };
    
    
}

#endif
