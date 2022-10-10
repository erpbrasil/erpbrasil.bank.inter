import os

import requests


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
        #cert_file_path = os.environ.get("certificado_inter_cert")
        #key_file_path = os.environ.get("certificado_inter_key")
        #cert = (cert_file_path, key_file_path)
        response = requests.post(
            "https://cdpj.partners.bancointer.com.br/oauth/v2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=request_body,
            cert=cert,
        )

        if response.status_code != 200:
            print("Server didn't return an 'OK' response.  Content was: {!r}".format(response.content))
            self.token_boleto_write = json.loads(response.text)
        else:
           self.token_boleto_write = response.json().get("access_token")



    def generate_token_boleto_read(self, scope, cert):
        request_body = (
            "client_id={0}&client_secret={1}&scope={2}&grant_type={3}".format(
                self.client_id, self.client_secret, scope, self.grant_type
            )
        )
        #cert_file_path = os.environ.get("certificado_inter_cert")
        #key_file_path = os.environ.get("certificado_inter_key")
        #cert = (cert_file_path, key_file_path)
        response = requests.post(
            "https://cdpj.partners.bancointer.com.br/oauth/v2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=request_body,
            cert=cert,
        )
        if response.status_code != 200:
            print("Server didn't return an 'OK' response.  Content was: {!r}".format(response.content))
            self.token_boleto_read = json.loads(response.text)
        else:
           self.token_boleto_read = response.json().get("access_token")
