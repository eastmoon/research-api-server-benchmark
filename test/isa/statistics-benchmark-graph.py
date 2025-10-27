# Import libraries
import os
import sys
import glob
import json
import pandas as pd
import matplotlib.pyplot as plt

# Declare variable
CACHE_DIR = "/tmp"
ENV_DURATION="10s"

# Declare function
def convert2perc(val_string):
    ## Declare variable
    val_string = val_string.lower()
    val_string = val_string.replace(' ', '')
    val_string = val_string.replace('%', '')
    return float(val_string)

def convert2mb(val_string):
    ## Declare variable
    val_numeric = -1
    val_string = val_string.lower()
    val_string = val_string.replace(' ', '')
    ## String to Numeric
    if isinstance(val_string, str):
        if 'kb' in val_string or 'kib' in val_string:
            # Remove 'kb', 'kib' and convert to float
            val_string = val_string.replace('kb', '')
            val_string = val_string.replace('kib', '')
            val_numeric = float(val_string)
            # Convert KB to MB
            val_numeric = val_numeric / 1024
        if 'mb' in val_string or 'mib' in val_string:
            # Remove 'mb', 'mib' and convert to float
            val_string = val_string.replace('mb', '')
            val_string = val_string.replace('mib', '')
            val_numeric = float(val_string)
        if 'gb' in val_string or 'gib' in val_string:
            # Remove 'gb', 'gib' and convert to float
            val_string = val_string.replace('gb', '')
            val_string = val_string.replace('gib', '')
            val_numeric = float(val_string)
            # Convert KB to MB
            val_numeric = val_numeric * 1024
    ## Return numeric value
    return val_numeric

def draw_k6_summary(testcases, duration, column, title, xlabel, ylabel):
    ## Declare variable
    stats_img=f'{CACHE_DIR}/stats-testcase-{column}.png'
    ##
    df = pd.DataFrame()
    for case in testcases:
        statistics_file=f'{CACHE_DIR}/stats-{case}-{duration}.csv'
        if os.path.isfile(statistics_file):
            ### Read statistics file.
            csv = pd.read_csv(statistics_file)
            ### Copy column
            df[case] = csv[column]
    df.plot(kind='line')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(stats_img, dpi=300, bbox_inches='tight')

def draw_container_statistics(container_name):
    ## Declare variable
    statistics_file=f'{CACHE_DIR}/stats-container-{container_name}.csv'
    stats_cpuperc_img=f'{CACHE_DIR}/stats-container-{container_name}-cpuperc.png'
    stats_memperc_img=f'{CACHE_DIR}/stats-container-{container_name}-memperc.png'
    stats_mem_img=f'{CACHE_DIR}/stats-container-{container_name}-mem.png'
    stats_block_img=f'{CACHE_DIR}/stats-container-{container_name}-block.png'
    stats_net_img=f'{CACHE_DIR}/stats-container-{container_name}-net.png'
    ##
    if os.path.isfile(statistics_file):
        try:
            ### Read statistics file.
            csv = pd.read_csv(statistics_file)
            ### Draw CPUPerc
            df = pd.DataFrame()
            df["CPUPerc"] = csv['CPUPerc'].apply(convert2perc)
            df.plot(kind='line')
            plt.title("CPU percentage")
            plt.savefig(stats_cpuperc_img, dpi=300, bbox_inches='tight')
            ### Draw MemPerc
            df = pd.DataFrame()
            df["MemPerc"] = csv['MemPerc'].apply(convert2perc)
            df.plot(kind='line')
            plt.title("Memory percentage")
            plt.savefig(stats_memperc_img, dpi=300, bbox_inches='tight')
            ### Draw memory usage
            df = pd.DataFrame()
            df["MemUsage"] = csv['MemUsage'].apply(convert2mb)
            df.plot(kind='line')
            plt.title("Memory Usage ( MiB )")
            plt.savefig(stats_mem_img, dpi=300, bbox_inches='tight')
            ### Draw block I/O
            df = pd.DataFrame()
            df["BlockInput"] = csv['BlockInput'].apply(convert2mb)
            df["BlockOutput"] = csv['BlockOutput'].apply(convert2mb)
            df.plot(kind='line')
            plt.title("Block I/O ( MB )")
            plt.savefig(stats_block_img, dpi=300, bbox_inches='tight')
            ### Draw network I/O
            df = pd.DataFrame()
            df["NetInput"] = csv['NetInput'].apply(convert2mb)
            df["NetOutput"] = csv['NetOutput'].apply(convert2mb)
            df.plot(kind='line')
            plt.title("Network I/O ( MB )")
            plt.savefig(stats_net_img, dpi=300, bbox_inches='tight')
        except Exception as e:
            print(f"Error: '{e}'.")

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
    draw_k6_summary(["server-status", "numeric", "string"], ENV_DURATION, "requests", "Total send request.", "vus", "times")
    draw_k6_summary(["server-status", "numeric", "string"], ENV_DURATION, "avg", "Average request duration time.", "vus", "milliseconds")
    draw_container_statistics("server")
    draw_container_statistics("tester")
    draw_container_statistics("workers-1")
    draw_container_statistics("workers-2")
