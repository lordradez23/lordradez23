import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://api.github.com/repos/lordradez23/lordradez23/actions/runs?per_page=10')
req.add_header('User-Agent', 'Mozilla/5.0')
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode())
        for r in data.get('workflow_runs', []):
            print(f"Run {r['run_number']}: {r['id']} - status: {r['status']}, conclusion: {r['conclusion']}, title: {r['display_title']}")
except Exception as e:
    print(f"Error: {e}")
