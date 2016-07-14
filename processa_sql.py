from conexao import Conexao
import sys

class processaSql:

    con = None

    def __init__(self):
        self.con = Conexao()
        return

    def getDadosPullRequestSql(self, id):
        db = self.con.qb('prod_t1')
        return db.table('repositorio_pull').where('repositorioPullId', id)