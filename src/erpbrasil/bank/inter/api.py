# -*- coding: utf-8 -*-
import json
import requests
from datetime import datetime

FILTRAR_POR = [
    'TODOS',
    'VENCIDOSAVENCER',
    'EXPIRADOS',
    'PAGOS',
    'TODOSBAIXADOS',
]

ORDENAR_CONSULTA_POR = [
    'NOSSONUMERO',  # (Default)
    'SEUNUMERO',
    'DATAVENCIMENTO_ASC',
    'DATAVENCIMENTO_DSC',
    'NOMESACADO',
    'VALOR_ASC',
    'VALOR_DSC',
    'STATUS_ASC',
    'STATUS_DSC',
]


class ApiInter(object):
    """ Implementa a Api do Inter"""

    _api = 'https://cdpj.partners.bancointer.com.br/cobranca/v2/'
    data_do_ultimo_token = None
    token = None

    def __init__(self, cert, conta_corrente, client_id, client_secret):
        self._cert = cert
        self.conta_corrente = conta_corrente
        self._client_id = client_id
        self._client_secret = client_secret

    def _prepare_token(self):
        URL_OAUTH = "https://cdpj.partners.bancointer.com.br/oauth/v2/token"
        D1 = "client_id={}".format(self._client_id)
        D2 = "client_secret={}".format(self._client_secret)
        D3 = "scope=boleto-cobranca.read boleto-cobranca.write"
        D4 = "grant_type=client_credentials"
        DADOS = f"{D1}&{D2}&{D3}&{D4}"
        response = requests.post(
            URL_OAUTH,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=DADOS,
            cert=self._cert,
            timeout=(10)
        )
        if not response.text:
            print("Sem resposta do serviço de OAuth.")
            return
        # Isola o access_token do JSON recebido
        access_token = response.json().get("access_token")
        if not access_token:
            return
        TOKEN = access_token
        return TOKEN


    def _prepare_headers(self):
        if self.token is not None:
            tempo_token = (datetime.now() - self.data_do_ultimo_token).total_seconds()
            if tempo_token > 3600:
                new_token = self._prepare_token()
                self.data_do_ultimo_token = datetime.now()
                self.token = new_token
        else:
            self.token = self._prepare_token()
            self.data_do_ultimo_token = datetime.now()
        return {
            "Authorization": "Bearer " + self.token,
            "Content-type": "application/json",
            "x-inter-conta-corrente": self.conta_corrente,
        }

    def _call(self, http_request, url, params=None, data=None, **kwargs):
        response = http_request(
            url,
            headers=self._prepare_headers(),
            params=params or {},
            data=data,
            cert=self._cert,
            verify=True,
            **kwargs
        )
        if response.status_code > 299:
            message = '%s - Código %s' % (
                response.status_code,
                response.text,
            )
            raise Exception(message)
        return response

    def boleto_inclui(self, boleto):
        """ POST
        https://cdpj.partners.bancointer.com.br/cobranca/v2/boletos

        :param boleto:
        :return:
        """
        result = self._call(
            requests.post,
            url=self._api,
            data=json.dumps(boleto),
        )
        return result.content and result.json() or result.ok

    def consulta_boleto_detalhado(self, nosso_numero=False):
        """ 
            GET https://cdpj.partners.bancointer.com.br/cobranca/v2/boletos/{nossoNumero}
        """
        if not nosso_numero:
            raise Exception('Nosso número não informado.')

        url = self._api + 'boletos/{}'.format(nosso_numero)

        result = self._call(
            requests.get,
            url=url,
        )
        return result.content and result.json() or result.ok

    def boleto_baixa(self, nosso_numero, codigo_baixa):
        """ POST
        https://cdpj.partners.bancointer.com.br/cobranca/v2/boletos/
        {nossoNumero}/cancelar

        :param nosso_numero:
        :return:
        """
        url = '{}boletos/{}/cancelar'.format(
            self._api,
            nosso_numero
        )
        result = self._call(
            requests.post,
            url=url,
            data='{{"motivoCancelamento":"{}"}}'.format(codigo_baixa)

        )
        return result.content and result.json() or result.ok

    def boleto_pdf(self, nosso_numero):
        """ GET
        https://cdpj.partners.bancointer.com.br/cobranca/v2/boletos/
        {nossoNumero}/pdf

        :param nosso_numero:
        :return:
        """
        url = '{}/{}/pdf'.format(
            self._api,
            nosso_numero
        )
        result = self._call(
            requests.get,
            url=url,
        )
        return result.content
