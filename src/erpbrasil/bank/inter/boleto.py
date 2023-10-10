# -*- coding: utf-8 -*-


# from erpbrasil.febraban.boleto.custom_property import CustomProperty
# from erpbrasil.febraban.entidades import Boleto


class BoletoInter:
    """ Implementa a Api do BancoInter """

    @classmethod
    def convert_to(cls, obj, **kwargs):
        obj.__class__ = cls
        obj.__special_init__()
        for key, value in kwargs.items():
            if hasattr(obj, key):
                obj.__dict__[key] = value

    def __init__(self, sender, amount, payer, issue_date, due_date,
                 identifier, instructions=None, mora=None, multa=None,
                 discount1=None, discount2=None, discount3=None):
        self._sender = sender
        self._amount = amount
        self._payer = payer
        self._issue_date = issue_date.strftime("%Y-%m-%d")
        self._due_date = due_date.strftime("%Y-%m-%d")
        self._identifier = identifier
        self._instructions = instructions or []

        self.mora = mora or dict(
            codigoMora="ISENTO",
            valor=0,
            taxa=0
        )
        self.multa = multa or dict(
            codigoMulta="NAOTEMMULTA",
            valor=0,
            taxa=0
        )
        self.discount1 = discount1 or dict(
            codigoDesconto="NAOTEMDESCONTO",
            taxa=0,
            valor=0,
            data=""
        )
        self.discount2 = discount2 or dict(
            codigoDesconto="NAOTEMDESCONTO",
            taxa=0,
            valor=0,
            data=""
        )
        self.discount3 = discount3 or dict(
            codigoDesconto="NAOTEMDESCONTO",
            taxa=0,
            valor=0,
            data=""
        )

    def _emissao_data(self):
        data = {
            "seuNumero": self._identifier[:15],
            "valorNominal": self._amount,
            "dataVencimento": self._due_date,
            "numDiasAgenda": 30,
            "pagador": {
                "cpfCnpj": self._payer.identifier,
                "nome": self._payer.name,
                # "email": self._payer.email,
                # "telefone": self._payer.phone[2:],
                "cep": self._payer.address.zipCode,
                "numero": self._payer.address.streetLine2,
                # "complemento": self._payer.address.streetLine2,
                "bairro": self._payer.address.district,
                "cidade": self._payer.address.city,
                "uf": self._payer.address.stateCode,
                "endereco": self._payer.address.streetLine1,
                # "ddd": self._payer.phone[:2],
                "tipoPessoa": "JURIDICA",
            },
            "desconto1": self.discount1,
            "desconto2": self.discount2,
            "desconto3": self.discount3,
            "multa": self.multa,
            "mora": self.mora,
            "beneficiarioFinal": {
                "nome": self._sender.name,
                "cpfCnpj": self._sender.identifier,
                "cep": self._sender.address.zipCode,
                "endereco": self._sender.address.streetLine1,
                "bairro": self._sender.address.district,
                "cidade": self._sender.address.city,
                "uf": self._sender.address.stateCode,
                "tipoPessoa": "JURIDICA",
            }
        }

        if self._instructions:
            data['mensagem'] = {'linha{}'.format(k + 1): v for k, v in enumerate(self._instructions)}

        return data
