import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def fetch(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0')
    with urllib.request.urlopen(req, context=ctx) as response:
        return json.loads(response.read().decode())

try:
    print("Fetching recent runs...")
    runs_data = fetch('https://api.github.com/repos/lordradez23/lordradez23/actions/runs?per_page=1')
    latest_run = runs_data['workflow_runs'][0]
    run_id = latest_run['id']
    print(f"Latest run ID: {run_id}")
    
    jobs_data = fetch(f'https://api.github.com/repos/lordradez23/lordradez23/actions/runs/{run_id}/jobs')
    for j in jobs_data.get('jobs', []):
        print(f"Job: {j['name']} - status: {j['status']}, conclusion: {j['conclusion']}")
        for s in j.get('steps', []):
            if s['conclusion'] == 'failure':
                print(f"  FAILED STEP: {s['name']} - status: {s['status']}, conclusion: {s['conclusion']}")
            else:
                print(f"  Step: {s['name']} - status: {s['status']}, conclusion: {s['conclusion']}")
except Exception as e:
    print(f"Error: {e}")
