import os
import json
import requests
import time



class Auth:
    access_token = ""
    token_type = ""
    expires_in = ""
    scope = ""
    client_id = ""
    client_secret = ""
    scope = ""
    grant_type = "client_credentials"
    token_boleto_write = ""
    token_boleto_read = ""

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def generate_token_boleto_write(self, scope, cert):
        request_body = (
            "client_id={0}&client_secret={1}&scope={2}&grant_type={3}".format(
                self.client_id, self.client_secret, scope, self.grant_type
            )
        )
        if os.environ.get('INTER_TOKEN_BOLETO_WRITE_LAST_UPDATE') is None:
            os.environ['INTER_TOKEN_BOLETO_WRITE_LAST_UPDATE'] = str(0)
        if float(os.environ.get('INTER_TOKEN_BOLETO_WRITE_LAST_UPDATE')) + 3600 < time.time():
            response = requests.post(
                "https://cdpj.partners.bancointer.com.br/oauth/v2/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=request_body,
                cert=cert,
            )

            if response.status_code != 200:
                print("Server didn't return an 'OK' response.  Content was: {!r}".format(response.content))
                raise Exception(
                    ["Server didn't return an 'OK' response.  Content was: {!r}".format(response.content),
                    str(response.text), response.status_code]
                    )
                self.token_boleto_write = json.loads(response.text)
            else:
               os.environ['INTER_TOKEN_BOLETO_WRITE'] = response.json().get("access_token")
               os.environ['INTER_TOKEN_BOLETO_WRITE_LAST_UPDATE'] = str(time.time())
        self.token_boleto_write = os.environ.get('INTER_TOKEN_BOLETO_WRITE')

    def generate_token_boleto_read(self, scope, cert):
        request_body = (
            "client_id={0}&client_secret={1}&scope={2}&grant_type={3}".format(
                self.client_id, self.client_secret, scope, self.grant_type
            )
        )
        if os.environ.get('INTER_TOKEN_BOLETO_READ_LAST_UPDATE') is None:
            os.environ['INTER_TOKEN_BOLETO_READ_LAST_UPDATE'] = str(0)
        if float(os.environ.get('INTER_TOKEN_BOLETO_READ_LAST_UPDATE')) + 3600 < time.time():
            response = requests.post(
                "https://cdpj.partners.bancointer.com.br/oauth/v2/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=request_body,
                cert=cert,
            )
            if response.status_code != 200:
                raise Exception(
                    ["Server didn't return an 'OK' response.  Content was: {!r}".format(response.content),
                    str(response.text), response.status_code]
                    )
                self.token_boleto_read = json.loads(response.text)
            else:
               os.environ['INTER_TOKEN_BOLETO_READ'] = response.json().get("access_token")
               os.environ['INTER_TOKEN_BOLETO_READ_LAST_UPDATE'] = str(time.time())
        self.token_boleto_read = os.environ.get('INTER_TOKEN_BOLETO_READ')
