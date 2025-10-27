# Import libraries
import os
import sys
import glob
import json
import pandas as pd

# Declare variable
CACHE_DIR = "/tmp"
ENV_DURATION="10s"

# Declare function
def retrieved_k6_summary(testcase, duration):
    """Retrieved k6 testcase summary to statistics file."""
    ## Declare variable
    retrieved_file=f'{CACHE_DIR}/stats-{testcase}-{duration}.csv'
    json_objects = []
    ## retrieve all file and statistics data.
    for file_path in sorted(glob.glob(f'{CACHE_DIR}/summary-{testcase}-{duration}*.json'), key=os.path.getmtime):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                metrics = {}
                json_object = {}
                if "metrics" in data:
                    metrics = data["metrics"]
                    json_object["requests"] = metrics["http_reqs"]["values"]["count"]
                    json_object["med"] = metrics["http_req_duration"]["values"]["med"]
                    json_object["max"] = metrics["http_req_duration"]["values"]["max"]
                    json_object["min"] = metrics["http_req_duration"]["values"]["min"]
                    json_object["avg"] = metrics["http_req_duration"]["values"]["avg"]
                    json_object["p(90)"] = metrics["http_req_duration"]["values"]["p(90)"]
                    json_object["p(95)"] = metrics["http_req_duration"]["values"]["p(95)"]
                    json_objects.append(json_object)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{file_path}'.")
        ## Output all statistics data to csv file
        df = pd.DataFrame(json_objects)
        df.to_csv(retrieved_file, index=False, encoding='utf-8')

def retrieved_container_statistics(container_name):
    """Retrieved Docker container resource usage summary to statistics file."""
    ## Declare variable
    watcher_log_file=f'{CACHE_DIR}/watcher.log'
    retrieved_file=f'{CACHE_DIR}/stats-container-{container_name}.csv'
    json_objects = []
    ## retrieve watcher file and statistics data.
    if os.path.isfile(watcher_log_file):
        with open(watcher_log_file, 'r', encoding='utf-8') as f:
            for line in f:
                # Strip whitespace (like newline characters) from the line
                stripped_line = line.strip()
                try:
                    # Convert the JSON string line to a Python dictionary
                    json_object = json.loads(stripped_line)
                    if "Name" in json_object and f'_{container_name}' in json_object["Name"] or "Name" in json_object and f'-{container_name}' in json_object["Name"] :
                        if "ID" in json_object: del json_object["ID"]
                        if "PIDs" in json_object: del json_object["PIDs"]
                        if "Name" in json_object: del json_object["Name"]
                        if "Container" in json_object: del json_object["Container"]
                        if "MemUsage" in json_object:
                            mem = json_object["MemUsage"].replace(" ", "").split("/")
                            del json_object["MemUsage"]
                            json_object["MemUsage"] = mem[0]
                            json_object["MemLimit"] = mem[1]
                        if "BlockIO" in json_object:
                            black = json_object["BlockIO"].replace(" ", "").split("/")
                            del json_object["BlockIO"]
                            json_object["BlockInput"] = black[0]
                            json_object["BlockOutput"] = black[1]
                        if "NetIO" in json_object:
                            net = json_object["NetIO"].replace(" ", "").split("/")
                            del json_object["NetIO"]
                            json_object["NetInput"] = net[0]
                            json_object["NetOutput"] = net[1]
                        json_objects.append(json_object)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line: {stripped_line} - {e}")
        ## Output all statistics data to csv file
        df = pd.DataFrame(json_objects)
        df.to_csv(retrieved_file, index=False, encoding='utf-8')


# Script entrypoint
if __name__ == '__main__':
    if len(sys.argv) > 1:
        print("Arguments provided:")
        for i, arg in enumerate(sys.argv[1:]):
            parmeter = arg.split("=")
            print(f"  Argument {parmeter[0]}: {parmeter[1]}")
            match parmeter[0]:
                case "--duration":
                    ENV_DURATION=parmeter[1]
    else:
        print("No arguments provided.")
    retrieved_k6_summary(testcase="server-status", duration=ENV_DURATION)
    retrieved_k6_summary(testcase="numeric", duration=ENV_DURATION)
    retrieved_k6_summary(testcase="string", duration=ENV_DURATION)
    retrieved_container_statistics("server")
    retrieved_container_statistics("tester")
    retrieved_container_statistics("workers-1")
    retrieved_container_statistics("workers-2")
