# -*- coding: utf-8 -*-
import json
import requests

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

    _api = 'https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos'

    def __init__(self, cert, conta_corrente):
        self._cert = cert
        self.conta_corrente = conta_corrente

    def _prepare_headers(self):
        return {
            'content-type': 'application/json',
            'x-inter-conta-corrente': self.conta_corrente,
        }

    def _call(self, http_request, url, params=None, data=None, **kwargs):
        response = http_request(
            url,
            headers=self._prepare_headers(),
            params=params or {},
            data=json.dumps(data or {}),
            cert=self._cert,
            verify=False,
            **kwargs
        )
        if response.status_code > 299:
            error = response.json()
            message = '%s - Código %s' % (
                response.status_code,
                error.get('error-code')
            )
            raise Exception(message)
        return response

    def boleto_inclui(self, boleto):
        """ POST
        https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos

        :param boleto:
        :return:
        """
        result = self._call(
            requests.post,
            url=self._api,
            data=boleto
        )
        return result.content and result.json() or result.ok

    def boleto_consulta(self, filtrar_por='TODOS', data_inicial=None, data_final=None,
                        ordenar_por='NOSSONUMERO'):
        """ GET
        https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos?
            filtrarPor=TODOS&
            dataInicial=2020-01-01&
            dataFinal=2020-12-01&
            ordenarPor=SEUNUMERO

        :param filtrar_por:
        :param data_inicial:
        :param data_final:
        :param ordenar_por:
        :return:
        """
        result = self._call(
            requests.get,
            url=self._api,
            params=dict(
                filtrarPor=filtrar_por,
                dataInicial=data_inicial,
                dataFinal=data_final,
                ordenarPor=ordenar_por
            )
        )
        return result.content and result.json() or result.ok

    def boleto_baixa(self, nosso_numero, codigo_baixa):
        """ POST
        https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos/
            00576501185/baixas

        :param nosso_numero:
        :return:
        """
        url = '{}/{}/baixas'.format(
            self._api,
            nosso_numero
        )
        result = self._call(
            requests.post,
            url=url,
            data=dict(
                codigoBaixa=codigo_baixa,
            )
        )
        return result.content and result.json() or result.ok

    def boleto_pdf(self, nosso_numero):
        """ GET
        https://apis.bancointer.com.br:8443/openbanking/v1/certificado/boletos/
            00595764723/pdf

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
