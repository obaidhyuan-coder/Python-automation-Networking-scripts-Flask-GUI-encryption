import socket
import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

SERVICE_MAP = {
    20: "FTP-DATA",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-ALT",
    8443: "HTTPS-ALT"
}

def service_name(port):
    return SERVICE_MAP.get(port, "unknown")

def parse_hosts(value):
    if not value:
        return ["127.0.0.1"]

    hosts = []
    for item in value.split(","):
        host = item.strip()
        if host:
            hosts.append(host)
    return hosts

def parse_port_list(value):
    ports = []

    if not value:
        return [80, 443, 22]

    for item in value.split(","):
        item = item.strip()
        if not item:
            continue

        if "-" in item:
            start, end = item.split("-", 1)
            start = int(start.strip())
            end = int(end.strip())
            if start > end:
                start, end = end, start
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(item))

    cleaned = []
    for port in ports:
        if 1 <= port <= 65535:
            cleaned.append(port)

    return cleaned

def scan_port(host, port, timeout):
    if not host:
        return {
            "host": host,
            "port": port,
            "status": "invalid host",
            "service": service_name(port)
        }

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))

            if result == 0:
                return {
                    "host": host,
                    "port": port,
                    "status": "open",
                    "service": service_name(port)
                }
            else:
             return {
                "host": host,
                "port": port,
                "status": "closed",
                "service": service_name(port)
             }

    except Exception as e:
        return {
            "host": host,
            "port": port,
            "status": "error",
            "error": str(e),
            "service": service_name(port)
        }

def scan_host(host, ports, timeout, rate_limit=0.0, max_workers=20):
    results = []
    max_workers = min(max_workers, len(ports)) if ports else 1

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_port, host, port, timeout) for port in ports]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            if rate_limit > 0:
                time.sleep(rate_limit)

    return results

def scan_target(hosts, ports, timeout, rate_limit=0.0, max_workers=20):
    all_results = []

    for host in hosts:
        host_results = scan_host(host, ports, timeout, rate_limit, max_workers)
        all_results.append({
            "host": host,
            "results": host_results
        })

    return all_results

def output_results(results, output_format="console", verbose=0):
    if output_format == "json":
        print(json.dumps(results, indent=2))
        return

    if output_format == "csv":
        print("host,port,status,service")
        for host_entry in results:
            for item in host_entry["results"]:
                print(f"{host_entry['host']},{item['port']},{item['status']},{item['service']}")
        return

    total_ports = 0
    open_count = 0
    closed_count = 0
    error_count = 0

    for host_entry in results:
        for item in host_entry["results"]:
            total_ports += 1

            if item["status"] == "open":
                open_count += 1
            elif item["status"] == "closed":
                closed_count += 1
            elif item["status"] == "error":
                error_count += 1

    if verbose:
        print("=== Scan statistics ===")
        print(f"Total ports scanned: {total_ports}")
        print(f"Open ports: {open_count}")
        print(f"Closed ports: {closed_count}")
        print(f"Errors: {error_count}")
        print()

    for host_entry in results:
        print(f"Host: {host_entry['host']}")

        for item in host_entry["results"]:
            if verbose or item["status"] == "open":
                print(f"  Port {item['port']} ({item['service']}): {item['status']}")

        if verbose:
            print()

def parse_args():
    parser = argparse.ArgumentParser(description="Advanced port scanner")
    parser.add_argument("--host", help="Target host or hosts separated by commas")
    parser.add_argument("--ports", help="Ports or port range, e.g. 22,80,443 or 1-100")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout per port scan")
    parser.add_argument("--format", choices=["console", "json", "csv"], default="console")
    parser.add_argument("--rate-limit", type=float, default=0.0, help="Delay between scans in seconds")
    parser.add_argument("--threads", type=int, default=20, help="Max threads for scanning")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase verbosity")
    return parser.parse_args()

def main():
    args = parse_args()

    hosts = parse_hosts(args.host)
    ports = parse_port_list(args.ports)
    timeout = args.timeout

    results = scan_target(hosts, ports, timeout, rate_limit=args.rate_limit, max_workers=args.threads)
    output_results(results, output_format=args.format, verbose=args.verbose)

if __name__ == "__main__":
    main()








