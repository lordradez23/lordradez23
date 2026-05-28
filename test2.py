import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://api.github.com/repos/lordradez23/lordradez23/actions/runs/26598486087/jobs')
req.add_header('User-Agent', 'Mozilla/5.0')
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        for j in data.get('jobs', []):
            print(f"Job: {j['name']} - status: {j['status']}, conclusion: {j['conclusion']}")
            for s in j.get('steps', []):
                print(f"  Step: {s['name']} - status: {s['status']}, conclusion: {s['conclusion']}")
except Exception as e:
    print(f"Error: {e}")
