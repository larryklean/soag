# -*- coding:utf-8
'''
   Created on 22/10/2011
   @author: C&C - HardSoft
'''
import Entidades
import Colunas
import ColunasEntidades
import PrimaryKeys
import ForeignKeys
import erwin as modelo
import os

def importarErwin(db, idErwin):

    parms = db(db.parametros.id == 1).select().first()
    erwint = db(db.erwins.id == idErwin).select().first()
    orig = os.path.join( '\\\\'
                       , '127.0.0.1'
                       , 'c$'
                       , parms.web2py
                       , 'applications'
                       , parms.soag
                       , 'uploads'
                       , erwint.arquivo)

    model = modelo.Erwin()

    erwin = model.load(arquivo=orig)

    if  not erwin['retorno']:
        flash = 'Falha na Execucao'
        labelErrors = 'Resultado da importacao do erwin'
        msgsErrors = {1: 'erro ao chamar o objeto Python.Erwin'}
        return {'retorno': False, 'flash': flash,
                                  'labelErrors': labelErrors,
                                  'msgsErrors': msgsErrors,
                                  'erwin': None}

    flash = 'Importacao efetuada.'
    labelErrors = 'Resultado da importacao do erwin'

    ret = {'entitys': model.getEntitys(),
           'attributes': model.getAttributes(),
           'domains': model.getDomains(),
           'keyGroups': model.getKeyGroups(),
           'relationShips': model.getRelationShips()}

    return {'retorno': True, 'flash': flash,
                             'labelErrors': labelErrors,
                             'msgsErrors': {},
                             'erwin': ret}

class LoadDB:

    def __init__(self, db, cAppl=0, iderwin=0):

        self.db      = db
        self.cAppl   = cAppl
        self.iderwin = iderwin
        self.retCode = []

    def loadDB(self, model):

        colunas    = Colunas.Colunas(self.db, cAppl=self.cAppl, model=model)
        returnCode = colunas.insertColunas()

        if  returnCode[0]:
            self.retCode.append(returnCode[1])
            entidades   = Entidades.Entidades(self.db, cAppl=self.cAppl,
                                             iderwin=self.iderwin, model=model)
            returnCode  = entidades.insertEntidades()
            if  returnCode[0]:
                self.retCode.append(returnCode[1])
                colunasEntidades = ColunasEntidades.ColunasEntidades(
                                        self.db, cAppl=self.cAppl, model=model)
                returnCode       = colunasEntidades.insertColunasEntidades()
                if  returnCode[0]:
                    self.retCode.append(returnCode[1])
                    primaryKeys = PrimaryKeys.PrimaryKeys(
                                        self.db, cAppl=self.cAppl, model=model)
                    returnCode  = primaryKeys.insertPrimaryKeys()
                    if  returnCode[0]:
                        self.retCode.append(returnCode[1])
                        foreignKeys = ForeignKeys.ForeignKeys(
                                        self.db, cAppl=self.cAppl, model=model)
                        returnCode  = foreignKeys.insertForeignKeys()
                        if  returnCode[0]:
                            self.retCode.append(returnCode[1])
                            return [1, self.retCode]

        return returnCode

    def processarErwin(self, idErwin, user, model):

        lDB = self.loadDB(model)

        if  lDB[0]:
            self.db(self.db.erwins.id==idErwin).update(status=5,
                                         mensagem='Carga efetuada no Sistema.')

        flash = 'Processamento efetuado.'

        labelErrors = 'Resultado da importacao do erwin'

        msgsErrors = {}

        idx = 0

        for msg in lDB[1]:
            if  len(msg) > 1:
                idx += 1
                msgsErrors[idx] = msg

        return {'retorno': True, 'flash': flash,
                                 'labelErrors': labelErrors,
                                 'msgsErrors': msgsErrors}
