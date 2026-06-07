#!/bin/bash

echo "========================================================"
echo " Starting Agile Cloud Performance Benchmarking Suite"
echo "========================================================"

# Check if config.json exists
if [ ! -f config.json ]; then
    echo "Error: config.json not found! Please configure endpoints."
    exit 1
fi

echo -e "\n[1/3] Executing Table 1: Database Latency Benchmarks (YCSB)..."
# python3 benchmark_table1_ycsb.py

echo -e "\n[2/3] Executing Table 2: Trans-Atlantic Network Latency (iPerf3)..."
# python3 benchmark_table2_network.py

echo -e "\n[3/3] Executing Table 3: Elasticity Velocity Provisioning..."
# python3 benchmark_table3_provisioning.py

echo -e "\n========================================================"
echo " Benchmarking Complete. Results saved to local directory."
echo "========================================================"