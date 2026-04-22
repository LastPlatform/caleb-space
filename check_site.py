import requests, urllib3
urllib3.disable_warnings()
r = requests.get("https://LastPlatform.github.io/caleb-space/", verify=False, timeout=15)
print("Status:", r.status_code)
print("URL:", r.url)
print("Content preview:", r.text[:300])
