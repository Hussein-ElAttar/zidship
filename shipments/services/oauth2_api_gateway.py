
import json
from datetime import datetime, timedelta
from typing import Dict

import requests
from shipments.models import CourierApiSettings


class OAuth2ApiGateway:
    settings: CourierApiSettings = None

    def __init__(self, settings):
        self.settings = settings

    def get_access_token(self) -> str:
        return self.settings.access_token

    def get_credentials(self) -> Dict[str, str]:
        return {'client_id': self.settings.client_id, 'client_secret': self.settings.client_secret}

    def authenticate(self) -> None:
        token_url = self.settings.api_url + '/' + self.settings.token_path

        data = {'grant_type': 'client_credentials', **self.get_credentials()}

        response = requests.post(url=token_url, data=data).json()

        self.settings.access_token = response['access_token']
        self.settings.token_expiration_date = datetime.now() + timedelta(seconds=response['expires_in'])
        self.settings.save()

    # Optional
    def handle_refresh(self) -> None:
        pass
