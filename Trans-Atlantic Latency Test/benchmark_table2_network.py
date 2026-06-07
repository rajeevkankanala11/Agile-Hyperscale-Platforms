import subprocess
import json

# EXPERIMENTAL SETUP:
# This script automates iPerf3 to measure Trans-Atlantic Network Latency (Table 2).
# It requires an iPerf3 server running in EU-West (iperf3 -s).

def measure_network_latency(provider_name, target_eu_ip):
    print(f"--- Testing Trans-Atlantic Latency for {provider_name} ---")
    
    # Run a UDP test (-u) to measure jitter and packet loss
    # Output is formatted in JSON (-J) for easy parsing
    cmd = [
        "iperf3", "-c", target_eu_ip, 
        "-u", "-b", "200M", "-t", "30", "-J"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        
        # Extracting metrics for Table 2
        jitter_ms = data['end']['sum']['jitter_ms']
        lost_percent = data['end']['sum']['lost_percent']
        
        print(f"Provider: {provider_name}")
        print(f"Jitter: {jitter_ms:.2f} ms")
        print(f"Packet Loss: {lost_percent:.3f} %")
        
        # Save raw data as the "Dataset" artifact
        with open(f"network_results_{provider_name}.json", "w") as f:
            json.dump(data, f, indent=4)
    else:
        print(f"Error connecting to {provider_name} EU-West server.")

if __name__ == "__main__":
    # IPs represent the EU-West VMs for each provider
    providers = {
        "AWS": "3.120.x.x",   
        "Azure": "51.140.x.x",
        "GCP": "34.107.x.x"   
    }
    
    for provider, ip in providers.items():
        measure_network_latency(provider, ip)