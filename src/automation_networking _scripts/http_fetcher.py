import urllib.request
import urllib.error
import argparse

# Parse the command-line URL argument for the fetcher.
def parse_args():
    parser = argparse.ArgumentParser(description="Fetch a URL and display the response.")
    parser.add_argument("url", help="The URL to fetch.")
    return parser.parse_args()

# Open the URL and print response status, headers, and content.
# Handle common URL and HTTP errors gracefully.
def fetch_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read()
            print("Response status:", response.status)
            print("Response headers:", response.getheaders())
            print("Response content:", content.decode('utf-8', errors='replace'))
    except urllib.error.HTTPError as e:
        print(f"HTTP error occurred: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL error occurred: {e.reason}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Main entry point for the HTTP fetcher.
def main():
    args = parse_args()
    fetch_url(args.url)
    print("Finished fetching URL:", args.url)
 
if __name__ == "__main__":
    main()
