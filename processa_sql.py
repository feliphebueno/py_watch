from conexao import Conexao
import sys

class processaSql:

    con = None

    def __init__(self):
        self.con = Conexao()
        return

    def getDadosPullRequestSql(self, id):
        qb = self.con.qb('prod_t1')
        return qb.table('repositorio_pull').where('repositorioPullId', id)

    def getContributorSql(self, login):
        qb = self.con.qb('prod_t1')
        return qb.table('contributor').where('contributorLogin', login)

    def getRepositorioSql(self, id):
        qb = self.con.qb('prod_t1')
        return qb.table('repositorio').where('repositorioId', id)