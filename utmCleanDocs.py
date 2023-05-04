import os
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET

if len(sys.argv) != 2:
    filename = os.path.splitext(os.path.basename(__file__))[0]
    print(f"Usage: python {filename}.py <computername>")
    sys.exit(1)

# Get the computer name parameter
computername = sys.argv[1]

# Construct the URL
url = f"http://{computername}:8080/opt/out"

# Read the XML data from the URL
try:
    with urllib.request.urlopen(url) as f:
        xml_data = f.read().decode('utf-8')
except urllib.error.URLError as e:
    print(f"Error: Failed to download XML data from the URL:\n{e.reason}")
    sys.exit(1)

# Parse the XML response
try:
    root = ET.fromstring(xml_data)
except:
    print("Got Bad XML")
    exit()

# Find all the 'url' tags and extract the text
urls = [url.text.strip() for url in root.findall(".//url")]

# Print the list of URLs
print(urls)

# Call curl -X DELETE on each URL
for url in urls:
    # Build the curl command
    curl_command = ["curl", "-X", "DELETE", url]

    # Call the curl command using subprocess and merge it's output to standard
    # output
    print("Deleting " + url)
    subprocess.run(curl_command, stdout=subprocess.PIPE)
