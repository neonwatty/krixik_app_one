import docker
import re

# Initialize Docker client
client = docker.from_env()


def print_container_logs(container_name: str) -> None:
    # Fetch the container
    container = client.containers.get(container_name)

    # Retrieve logs from the container
    logs = container.logs(stdout=True, stderr=True, tail=100).decode("utf-8")

    # Define a regex pattern to match lines with timestamps
    timestamp_pattern = re.compile(r"^\d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2},\d{3}", re.MULTILINE)

    # Define patterns to exclude lines containing specific keywords
    exclude_patterns = re.compile(r"(START RequestId|END RequestId|REPORT RequestId)", re.MULTILINE)

    # Filter out lines that start with timestamps or contain specific keywords
    filtered_logs = "\n".join(line for line in logs.splitlines() if not (timestamp_pattern.match(line) or exclude_patterns.search(line)))
    print(filtered_logs)
