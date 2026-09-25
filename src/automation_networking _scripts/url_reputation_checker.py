"""URL reputation checker: validate URLs and check for suspicious patterns."""

import re
from urllib.parse import urlparse
import json

# Validate the URL structure using a regex pattern.
def is_valid_url(url):
    url_pattern = re.compile(
        r'^https?://'  # http or https
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

# Look for suspicious words or short URL patterns.
def check_suspicious_patterns(url):
    suspicious_keywords = [
        "phishing", "malware", "trojan", "virus",
        "bit.ly", "tinyurl", "bit", "short",  # shortened URLs
        "login", "confirm", "verify", "update",  # common phishing patterns
    ]
    url_lower = url.lower()
    found_issues = []
    for keyword in suspicious_keywords:
        if keyword in url_lower:
            found_issues.append(f"Contains suspicious keyword: {keyword}")
    return found_issues

# Analyze the URL and collect any reputation issues.
def check_url_reputation(url):
    issues = []
    if not is_valid_url(url):
        issues.append("Invalid URL format")
        return issues
    parsed = urlparse(url)
    issues.extend(check_suspicious_patterns(url))
    if parsed.scheme != "https":
        issues.append("Not using HTTPS (unencrypted)")
    if "localhost" in parsed.netloc or "127.0.0.1" in parsed.netloc:
        issues.append("Points to localhost (local development)")
    if parsed.port and parsed.port not in [80, 443, 8080, 8443]:
        issues.append(f"Using unusual port: {parsed.port}")
    return issues

# Main interactive script for checking a URL.
def main():
    print("URL Reputation Checker")
    url = input("Enter URL to check: ")
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    issues = check_url_reputation(url)
    print(f"\nAnalyzing: {url}")
    if not issues:
        print("✓ URL appears safe (no issues detected)")
    else:
        print(f"⚠ Found {len(issues)} potential issue(s):")
        for issue in issues:
            print(f"  - {issue}")
    log_entry = {
        "url": url,
        "issues_count": len(issues),
        "issues": issues
    }
    with open("url_check_log.json", "a") as f:
        json.dump(log_entry, f)
        f.write("\n")
    print("\nLog saved to url_check_log.json")


if __name__ == "__main__":
    main()
