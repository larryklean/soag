# -*- coding:utf-8
'''
   Created on 25/09/2011
   @author: C&C - HardSoft
'''

class Aplicacao:

   def __init__(self, db, cAppl):

       self.db         = db
       self.aplicacoes = self.db.aplicacoes

       try:
           self.query               = self.db(self.aplicacoes.id==cAppl).select()
           self.applId              = self.query[0].aplicacao
           self.applName            = self.query[0].descricao
           self.contratante         = self.query[0].contratante
           self.grupo               = self.query[0].grupo
           self.analista            = self.query[0].analista
           self.soag                = self.query[0].soag
           self.glog                = self.query[0].glog
           self.delecaoLogica       = self.query[0].delecaoLogica
           self.colunaDelecaoLogica = self.query[0].colunaDelecaoLogica
           self.empresa             = self.query[0].empresa
       except:
           self.applId              = 0
           self.applName            = ''
           self.contratante         = ''
           self.grupo               = ''
           self.analista            = ''
           self.soag                = 0
           self.glog                = 0
           self.delecaoLogica       = 0
           self.colunaDelecaoLogica = ''
           self.empresa             = 0

   def getApplId(self):
       return self.applId

   def getApplName(self):
       return self.applName

   def getContratante(self):
       return self.contratante

   def getGrupo(self):
       return self.grupo

   def getAnalista(self):
       return self.analista

   def getSoag(self):
       return self.soag

   def getGlog(self):
       return self.glog

   def getDelecaoLogica(self):
       return self.delecaoLogica

   def getColunaDelecaoLogica(self):
       return self.colunaDelecaoLogica

   def getEmpresaId(self):
       return self.empresa
