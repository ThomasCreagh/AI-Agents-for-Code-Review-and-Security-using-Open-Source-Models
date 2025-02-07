import re
import yaml
import os
import argparse

# load security patterns from YAML file


def load_patterns():
    """load patterns for credential scanning here"""
    with open("security_scanner/config/patterns.yaml", "r") as file:
        data = yaml.safe_load(file)
    return data["credential_patterns"]

# Scan a file for credential patterns


def scan_file(file_path, patterns):
    """scan for patterns"""
    results = []
    with open(file_path, "r", errors="ignore") as file:
        for line_num, line in enumerate(file, start=1):
            for pattern in patterns:
                if re.search(pattern["pattern"], line):
                    results.append({
                        "file": file_path,
                        "line": line_num,
                        "match": pattern["name"],
                        "content": line.strip()
                    })
    return results

# scan whole dir


def scan_directory(directory):
    """scan all files in dir"""
    patterns = load_patterns()
    findings = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".js", ".env", ".json", ".txt")):
                file_path = os.path.join(root, file)
                findings.extend(scan_file(file_path, patterns))

    return findings


if __name__ == "__main__":
    target_directory = "test_files"  # needs to be changed
    results = scan_directory(target_directory)

    if results:
        print("\nDetected Potential Exposed Credentials:\n")
        for res in results:
            print(f"[{res['file']}:{res['line']}] {res['match']} → {res['content']}")
    else:
        print("No credentials found")
