# Agile Cloud Scalability & Performance Benchmarking Suite

This repository contains the experimental artifact suite for the manuscript: **"Scalability and Performance Paradoxes in Agile Cloud Environments: A Comparative Analytical Evaluation of Hyperscale Platforms."**

This suite automates the provisioning, execution, and metric collection across AWS, Microsoft Azure, and Google Cloud Platform (GCP) to evaluate Agile application suitability. It measures Database Latency, Trans-Atlantic Network Latency, and Elasticity Velocity ($E_v$).

## Repository Structure
```text
.
├── README.md                      # Documentation and methodology mapping
├── config.json                    # Centralized configuration for cloud endpoints
├── requirements.txt               # Python package dependencies
├── Dockerfile                     # Standardized execution environment setup
├── run_benchmarks.sh              # Master shell script to execute all suites
├── benchmark_table1_ycsb.py       # DB Latency (DynamoDB, Cosmos DB, Firestore)
├── benchmark_table2_network.py    # Network Latency & Jitter (iPerf3)
└── benchmark_table3_provisioning.py # Elasticity Velocity (Fargate, Container Apps, Cloud Run)