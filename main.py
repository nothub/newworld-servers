import json
import sys

import requests
from bs4 import BeautifulSoup


def scrape_servers(region_id: int):
    servers = list()
    for region_data in soup.findAll(attrs={"data-index": region_id}):
        region_servers = region_data.findAll("div", class_="ags-ServerStatus-content-responses-response-server-name")
        for server in region_servers:
            servers.append(server.text.strip())
    return servers


if __name__ == '__main__':

    response = requests.get("https://www.newworld.com/support/server-status")
    soup = BeautifulSoup(response.content, 'html.parser')

    regions = dict()
    for region in soup.find_all(name="a", attrs={"class": "ags-ServerStatus-content-tabs-tabHeading"}):
        regions[region['data-index']] = region.text.strip()

    if not len(regions):
        print("no regions found, something is fucked!", file=sys.stderr)
        exit(1)

    results = dict()
    for region_id, region_name in regions.items():
        results[region_name] = scrape_servers(region_id)
        count = len(results[region_name])
        if not count:
            print("no servers in region " + region_name + ", something is fucked!", file=sys.stderr)
            exit(1)
        else:
            print(region_name + ": " + str(count) + " servers")

    with open('servers.json', 'w') as output_file:
        output_file.write(json.dumps(results, indent=2))
