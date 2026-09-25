import requests
import urllib.parse
import dns.resolver
import validators
from bs4 import BeautifulSoup


def url_checker(url):
    if not validators.url(url):
        return {
            "valid": False,
            "scheme": None,
            "domain": None,
            "path": None,
            "hostname": None
        }

    parsed = urllib.parse.urlparse(url)

    return {
        "valid": True,
        "scheme": parsed.scheme,
        "domain": parsed.netloc,
        "path": parsed.path,
        "hostname": parsed.hostname
    }


def dns_checker(domain):
    try:
        records = {
            "A": [str(r) for r in dns.resolver.resolve(domain, "A")],
            "MX": [str(r.exchange) for r in dns.resolver.resolve(domain, "MX")],
            "NS": [str(r) for r in dns.resolver.resolve(domain, "NS")],
            "TXT": [str(r) for r in dns.resolver.resolve(domain, "TXT")]
        }
        return {
            "valid": True,
            "records": records
        }
    except Exception:
        return {
            "valid": False,
            "records": {}
        }


def url_page_checker(url):
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        links = [link.get("href") for link in soup.find_all("a") if link.get("href")]

        return {
            "status_code": response.status_code,
            "final_url": response.url,
            "redirected": len(response.history) > 0,
            "html": html,
            "links": links
        }
    except Exception as e:
        return {
            "status_code": None,
            "final_url": None,
            "redirected": False,
            "html": "",
            "links": [],
            "error": str(e)
        }


def patterns_checker(url, html=""):
    suspicious_keywords = [
        "login", "verify", "account", "update",
        "secure", "bank", "password", "confirm"
    ]

    flags = []
    lower_url = url.lower()
    lower_html = html.lower()

    for keyword in suspicious_keywords:
        if keyword in lower_url or keyword in lower_html:
            flags.append(keyword)

    return {
        "is_suspicious": bool(flags),
        "patterns_found": flags
    }


def main():
    print("URL Reputation Checker")
    url = input("Enter URL to check: ")

    parsed_url = url_checker(url)

    if not parsed_url["valid"]:
        result = {
            "classification": "invalid_url",
            "details": parsed_url
        }
        print(result)
        return

    dns_data = dns_checker(parsed_url["hostname"])
    page_data = url_page_checker(url)
    pattern_data = patterns_checker(url, page_data.get("html", ""))

    classification = "safe"

    if not dns_data["valid"]:
        classification = "suspicious"

    if page_data.get("status_code") is not None and page_data["status_code"] >= 400:
        classification = "suspicious"

    if pattern_data["is_suspicious"]:
        classification = "malicious"

    result = {
        "classification": classification,
        "url": parsed_url,
        "dns": dns_data,
        "page": page_data,
        "patterns": pattern_data
    }

    print(result)


if __name__ == "__main__":
    main()