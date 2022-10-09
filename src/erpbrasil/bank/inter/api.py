# -*- coding: utf-8 -*-
import json

import requests

from .auth import Auth

FILTRAR_POR = [
    "TODOS",
    "VENCIDOSAVENCER",
    "EXPIRADOS",
    "PAGOS",
    "TODOSBAIXADOS",
]

ORDENAR_CONSULTA_POR = [
    "NOSSONUMERO",  # (Default)
    "SEUNUMERO",
    "DATAVENCIMENTO_ASC",
    "DATAVENCIMENTO_DSC",
    "NOMESACADO",
    "VALOR_ASC",
    "VALOR_DSC",
    "STATUS_ASC",
    "STATUS_DSC",
]


class ApiInter(object):
    """Implementa a Api do Inter"""

    # _api = 'https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos'
    _api = "https://cdpj.partners.bancointer.com.br/cobranca/v2/boletos/"

    def __init__(self, conj_cert, conta_corrente, clientId, clientSecret):
        self._cert = conj_cert
        self.conta_corrente = conta_corrente
        self.auth = Auth(
            clientId,
            # "50acb448-5107-4f57-81ea-54a615c5da0a",
            clientSecret,
            # "0a0275ff-4fcc-4f7f-a092-edcbb5bb6bd8",
        )
        self.auth.generate_token_boleto_write("boleto-cobranca.write", self._cert)
        self.auth.generate_token_boleto_read("boleto-cobranca.read", self._cert)

    def _prepare_headers(self, token):
        return {
            "content-type": "application/json",
            "x-inter-conta-corrente": self.conta_corrente,
            "Authorization": "Bearer " + token,
        }

    def _call(self, token, http_request, url, params=None, data=None, **kwargs):
        debug1 = self._prepare_headers(token)
        debug2 = json.dumps(data or {})
        debug3 = params or {}
        response = http_request(
            url,
            headers=self._prepare_headers(token),
            params=params or {},
            data=json.dumps(data or {}),
            cert=self._cert,
            verify=True,
            **kwargs,
        )
        if response.status_code > 299:
            # error = response.json()
            error = response  # .json()
            # message = '%s - Código %s' % (
            #    response.status_code,
            #    error.get('error-code')
            # )
            # raise Exception(message)
            raise Exception(
                [str(response.text), response.status_code, debug1, debug2, debug3]
            )
        return response

    def boleto_inclui(self, boleto):
        """POST

        :param boleto:
        :return:
        """
        result = self._call(
            self.auth.token_boleto_write, requests.post, url=self._api, data=boleto
        )
        return result.content and result.json() or result.ok

    def boleto_consulta(
        self,
        filtrar_por="TODOS",
        data_inicial=None,
        data_final=None,
        ordenar_por="NOSSONUMERO",
        page=0,
    ):
        result = self._call(
            self.auth.token_boleto_read,
            requests.get,
            url=self._api,
            params=dict(
                filtrarPor=filtrar_por,
                dataInicial=data_inicial,
                dataFinal=data_final,
                ordenarPor=ordenar_por,
                page=page,
            ),
        )
        return result.content and result.json() or result.ok

    def boleto_recupera(self, nosso_numero):

        _url = f"{self._api}/{nosso_numero}"

        result = self._call(
            self.auth.token_boleto_read,
            requests.get,
            url=_url,
        )

        return result.content and result.json() or result.ok

    def boleto_baixa(self, nossoNumero, motivoCancelamento):
        """POST
        https://cdpj.partners.bancointer.com.br/cobranca/v2/boletos/{nossoNumero}/cancelar


        :param nosso_numero:
        :return:
        """
        url = "{}{}/cancelar".format(self._api, nossoNumero)
        result = self._call(
            self.auth.token_boleto_write,
            requests.post,
            url=url,
            data=dict(
                motivoCancelamento=motivoCancelamento,
            ),
        )
        return result.content and result.json() or result.ok

    def boleto_pdf(self, nosso_numero):
        """GET
        https://cdpj.partners.bancointer.com.br/cobranca/v2/boletos/
            00595764723/pdf

        :param nosso_numero:
        :return:
        """
        url = "{}{}/pdf".format(self._api, nosso_numero)
        result = self._call(
            self.auth.token_boleto_read,
            requests.get,
            url=url,
        )
        return result.content
