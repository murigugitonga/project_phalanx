# Project PHALANX

Project Phalanx (Platform for heterogenous Analysis and Low Latency Networked Data Fusion) consists of two disparate engines exchanging serialized payload transfers and linked by protocol buffers. 

## Project development architecture
Project Phalanx is systematically built from the ground up. The logical progression of this multi-language defence architecture follows this order:
 - Establishing the data contract.
 - Build the communication pipeline.
 - The AI reasoning layer. 
### The protocol buffer layer
The immutable contract that ensures that both Python and C++ read the exact same binary data structures down to the bit.
### The Ingestion Engine
Written in C++, the ingestion engine parses raw string packets without runtime allocation and drops corrupted or malformed data packets.

### The Build Architecture
The automated build configuration file.

### The Edge parser header (parser.hpp)
Enforces static stack-allocated tokenization to handle raw sensor inputs without runtime memory leaks.

### The main ingestion engine (main.cpp)
This entrypoint spins up the pipeline, instantiates a sample gRPC client connection to pass the parsed data feeds over the cross-language transport boundary and mocks a live radar feed.

## The Cross-Language Interface (gRPC Pipeline)
This pipeline:
 - Encaspulates tracking frames into binary frameworks.
 - Controls sychronous data exchange pipelines.

## The Cognitive Reasoning Layer
The Cognitive reasoning layer is explicitly written in Python:

 - Evaluates threat priorities via langGraph.
 - Queries localized vector rules databases.
