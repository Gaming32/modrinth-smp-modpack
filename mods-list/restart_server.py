"""
Why is this file in this folder?

Science isn't about why! It's about why not! Why is so much of our science dangerous? Why not marry safe science if you
love it so much! In fact, why not invent a special safety door that won't hit your butt on the way out, because you are
fired!
"""
import sys

import requests

if len(sys.argv) <= 4:
    print('Usage: restart_server.py <panel_url> <client_id> <client_secret> <server_id>')
    sys.exit(1)

panel_url = sys.argv[1]
client_id = sys.argv[2]
client_secret = sys.argv[3]
server_id = sys.argv[4]

print('Getting bearer token...')
resp = requests.post(
    f'{panel_url}/oauth2/token',
    data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
)
resp.raise_for_status()
token: str = resp.json()['access_token']
print(f'Token: Bearer {token[:100]}...\n')

print('Stopping server...')
try:
    requests.post(
        f'{panel_url}/daemon/server/{server_id}/stop?wait=true',
        headers={'Authorization': f'Bearer {token}'},
        timeout=300
    )
except requests.Timeout:
    print('Server restart timed out. Killing server.\n')
    requests.post(
        f'{panel_url}/daemon/server/{server_id}/kill',
        headers={'Authorization': f'Bearer {token}'}
    )

print('Starting server...')
requests.post(
    f'{panel_url}/daemon/server/{server_id}/start',
    headers={'Authorization': f'Bearer {token}'}
)
