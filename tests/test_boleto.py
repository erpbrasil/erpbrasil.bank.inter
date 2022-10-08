# -*- coding: utf-8 -*-
import os
import unittest
from datetime import datetime

from febraban.cnab240.user import User
from febraban.cnab240.user import UserAddress
from febraban.cnab240.user import UserBank

from erpbrasil.bank.inter.api import ApiInter
from erpbrasil.bank.inter.boleto import BoletoInter


class TestBancoApiInter(unittest.TestCase):
    def setUp(self):
        certificado_cert = os.environ.get("certificado_inter_cert")
        certificado_key = os.environ.get("certificado_inter_key")
        print(ApiInter._api)
        self.api = ApiInter(
            cert=(certificado_cert, certificado_key),
            conta_corrente="10869106",
            clientId="50acb448-5107-4f57-81ea-54a615c5da0a",
            clientSecret="0a0275ff-4fcc-4f7f-a092-edcbb5bb6bd8",
        )
        self.dados = []

        myself = User(
            name="KMEE INFORMATICA LTDA",
            identifier="23130935000198",
            bank=UserBank(
                bankId="341",
                branchCode="1234",
                accountNumber="33333",
                accountVerifier="4",
                bankName="BANCO ITAU SA",
            ),
        )
        now = datetime.now()
        for i in range(3):
            payer = User(
                name="Sacado Teste",
                identifier="26103754097",
                email="mileo@kmee.com.br",
                personType="FISICA",
                phone="35988763663",
                address=UserAddress(
                    streetLine1="Rua dos TESTES",
                    district="CENTRO",
                    city="SAO PAULO",
                    stateCode="SP",
                    zipCode="31327130",
                    streetNumber="15",
                ),
            )
            slip = BoletoInter(
                sender=myself,
                amount="100.00",
                payer=payer,
                issue_date=now,
                due_date=now,
                identifier="456" + str(i),
                instructions=[
                    "TESTE 1",
                    "TESTE 2",
                    "TESTE 3",
                    "TESTE 4",
                ],
            )
            self.dados.append(slip)

    def test_data(self):
        for item in self.dados:
            self.assertTrue(item._emissao_data())

    def test_boleto_api(self):
        for item in self.dados:
            resposta = self.api.boleto_inclui(item._emissao_data())
            item.nosso_numero = resposta["nossoNumero"]
            item.seu_numero = resposta["seuNumero"]
            item.linha_digitavel = resposta["linhaDigitavel"]
            item.barcode = resposta["codigoBarras"]

            self.assertListEqual(
                list(resposta.keys()),
                ["seuNumero", "nossoNumero", "codigoBarras", "linhaDigitavel"],
                "Erro ao registrar boleto",
            )

        resposta = self.api.boleto_consulta(
            data_inicial="2020-01-01", data_final="2020-12-01", ordenar_por="SEUNUMERO"
        )
        self.assertTrue(resposta, "Falha ao consultar boletos")

        for item in self.dados:
            resposta = self.api.boleto_pdf(nosso_numero=item.nosso_numero)
            self.assertTrue(resposta, "Falha ao imprimir boleto")

        for item in self.dados:
            resposta = self.api.boleto_baixa(
                nossoNumero=item.nosso_numero,
                motivoCancelamento="SUBSTITUICAO",
            )
            self.assertTrue(resposta, "Falha ao Baixar boletos")


suite = unittest.TestLoader().loadTestsFromTestCase(TestBancoApiInter)

if __name__ == "__main__":
    unittest.main()
