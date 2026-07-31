# Project PHALANX

Platform for Heterogeneous Analysis and Low-latency Networked Data Fusion (PHALANX) is a software-defined tactical command architecture designed to ingest, process, and classify real-time multi-domain sensor telemetry at the tactical edge. 

Built under the structural paradigms of the overarching A.R.M.E.D study framework, Project PHALANX bridges high-throughput, low-latency native hardware processing (C++) with asynchronous multi-agent cognitive reasoning infrastructures (Python, MCP) via high-performance binary transport boundaries.

## Legal & Compliance Eligibility

*   **Export Control Classification:** U.S. Person / ITAR and EAR Compliant Engineering Architecture.
*   **Design Framework:** Engineered exclusively around Dual-Use and ITAR-Free hardware-agnostic patterns, enabling seamless integration across unclassified commercial pipelines and allied defense logistics networks.

## Core Architectural Modules

### 1. Edge Ingestion Engine (C++20)
*   **Objective:** Zero-allocation tokenization and structural sanitization of raw, high-throughput text and binary sensor feeds.
*   **Design Constraints:** Implements static stack allocation profiles and explicit exception handling boundaries to avoid runtime heap fragmentation during continuous tracking operations.
*   **Operational Role:** Sockets directly into hardware radar arrays, tracking systems, and edge telemetry networks.

### 2. High-Speed Transport Layer (gRPC / Protocol Buffers)
*   **Objective:** Cross-language type-safety and minimal latency serialization.
*   **Design Constraints:** Leverages Google Protocol Buffers over persistent HTTP/2 transport connections to strip JSON parsing overhead entirely out of the execution loop.
*   **Operational Role:** Acts as an immutable structural contract ensuring state synchronization between the C++ Ingestion layer and the Python Reasoning layer.

### 3. Cognitive Reasoning Layer (Python 3.11 & Model Context Protocol)
*   **Objective:** Deterministic threat prioritization, multi-agent coordination, and localized rule verification.
*   **Design Constraints:** Implements Model Context Protocol (MCP) server endpoints alongside localized Vector Retrieval-Augmented Generation (RAG) tools to execute within entirely air-gapped environments.
*   **Operational Role:** Parses tactical engagement guidelines and issues threat classification metrics without routing telemetry outside the immediate base station perimeter.

## Repository File Tree Layout

## Setup & Execution inside GitHub Codespaces

This repository contains a pre-configured devcontainer file that automatically instantiates all toolchains, compilers, and library dependencies required for development.

### 1. Initialize the Workspace
Open this repository within GitHub Codespaces. The container build will automatically execute the post-creation commands to compile dependencies.

### 2. Compile the Serialization Schema
Navigate to the repository root and generate the respective C++ and Python communication bindings from the Protocol Buffer contract:
```bash
protoc -I=proto --cpp_out=src/ingestion --grpc_out=src/ingestion --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` proto/telemetry.proto
python3 -m grpc_tools.protoc -Iproto --python_out=src/reasoning --grpc_out=src/reasoning --plugin=protoc-gen-grpc=`which grpc_tools_node_protoc` proto/telemetry.proto
```

### 3. Build the C++ Edge Binary
```bash
cd src/ingestion
mkdir build && cd build
cmake ..
make
./phalanx_ingest
```

### 4. Initialize the Cognitive Engine
```bash
cd src/reasoning
python3 main.py
```

## System Robustness and Edge Paradigms

Project PHALANX is specifically engineered to mitigate standard vulnerabilities found in commercial SaaS platforms migrating to tactical environments:

*   **Graceful Network Degradation:** If the communication line to the Python cognitive network drops, the C++ ingestion engine invokes a localized memory ring buffer, safely caching data coordinates without halting system processes.
*   **Anti-Air Gap Leaks:** By avoiding third-party commercial cloud APIs, all RAG vector stores are indexed inside localized embedded file stores (ChromaDB), blocking metadata exfiltration over public networks.
*   **Memory-Safe Malformed Rejection:** The edge parser treats all incoming strings as untrusted inputs, deploying instant delimiter bounds verification to counter memory manipulation attempts embedded in corrupted sensor telemetry.
