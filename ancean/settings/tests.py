import os
import json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

SECRETS_FOLDER = os.path.join(Path(__file__).resolve().parent.parent, 'secrets')

OAUTH_SECRETS = os.path.join(SECRETS_FOLDER, 'oauth-secrets.json')

with open(OAUTH_SECRETS) as f:
    oauth_secrets = json.loads(f.read())
    
    
print(oauth_secrets)