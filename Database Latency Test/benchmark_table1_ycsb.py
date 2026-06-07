import subprocess
import time

# EXPERIMENTAL SETUP: 
# This script automates the YCSB (Yahoo! Cloud Serving Benchmark) execution
# to reproduce Table 1: Database Latency Profiles.

def run_ycsb_workload_a(database_binding, connection_string):
    print(f"--- Starting Benchmark for {database_binding} ---")
    
    # Step 1: Load 1 Million records into the database
    load_cmd = [
        "./bin/ycsb", "load", database_binding, "-s",
        "-P", "workloads/workloada",
        "-p", f"recordcount=1000000",
        "-p", f"{database_binding}.url={connection_string}"
    ]
    print("Loading data phase...")
    subprocess.run(load_cmd, capture_output=True)
    
    # Step 2: Run Workload A to measure p50 and p99 latency
    # Workload A is 50% reads, 50% writes
    run_cmd = [
        "./bin/ycsb", "run", database_binding, "-s",
        "-P", "workloads/workloada",
        "-p", "operationcount=10000000",
        "-p", "threadcount=256",
        "-p", f"{database_binding}.url={connection_string}"
    ]
    
    print("Executing Workload A...")
    result = subprocess.run(run_cmd, capture_output=True, text=True)
    
    # The output contains the p99 latency metrics required for Table 1
    with open(f"results_{database_binding}_table1.txt", "w") as f:
        f.write(result.stdout)
    
    print(f"Results saved to results_{database_binding}_table1.txt\n")

if __name__ == "__main__":
    # Note: Replace with actual live cloud connection strings before running
    dbs = {
        "dynamodb": "dynamodb.us-east-1.amazonaws.com",
        "azurecosmos": "mongodb://user:pwd@mycosmos.documents.azure.com:10255",
        "googlefirestore": "firestore.googleapis.com"
    }
    
    for db, conn in dbs.items():
        run_ycsb_workload_a(db, conn)
        time.sleep(10) # Cooldown between tests