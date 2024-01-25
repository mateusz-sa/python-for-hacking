import requests
import sys


def urls(out_file):
    url2 = sys.stdin.read().splitlines()

    good_urls = []
    bad_urls = []

    for url in url2:
        try:
            response = requests.head(url)
            if response.status_code == 200:
                good_urls.append(url)

        except requests.exceptions.MissingSchema:
            bad_urls.append(url)
            continue
        except requests.exceptions.ConnectionError:
            bad_urls.append(url)
            continue
    with open(out_file, 'w') as file:
        file.write('\n'.join(good_urls))


    print("\nScript for probing websites based on target lists (URLs)\n")
    #print(f"Incorrect URLs:\n {bad_urls} \n")
    for bad_url in bad_urls:
        print(f"[-] {bad_url}")

    print("\n")
    #print(f"Correct URLs:\n {good_urls}\n")
    for good_url in good_urls:
        print(f"[+] {good_url}")

    print(f"\nSaved URLS {out_file}\n")



out_file = 'filtered_urls.txt'
urls(out_file)

# usage 
# cat urls.txt |  python .\url-probe.py