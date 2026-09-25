import socket
import ipaddress
import dns.resolver


def scan_ip(host_or_domain):
    try:
        return socket.gethostbyname(host_or_domain)
    except socket.gaierror:
        return "Invalid host or domain"


def ip_checker(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.version == 4:
            version = "IPv4"
        else:
            version = "IPv6"

        if ip_obj.is_private:
            status = "private"
        else:
            status = "public"

        return version, status
    except ValueError:
        return "Invalid IP"


def dns_checker(domain):
    try:
        a_records = dns.resolver.resolve(domain, "A")
        mx_records = dns.resolver.resolve(domain, "MX")
        ns_records = dns.resolver.resolve(domain, "NS")
        txt_records = dns.resolver.resolve(domain, "TXT")

        return a_records, mx_records, ns_records, txt_records
    except Exception:
        return "No DNS records found"


def main():
    target = input("Enter host or domain: ")
    ip = scan_ip(target)
    print("IP:", ip)
    print("IP status:", ip_checker(ip))
    if "." :
     domain = target
     print("DNS:", dns_checker(domain))


if __name__ == "__main__":
    main()