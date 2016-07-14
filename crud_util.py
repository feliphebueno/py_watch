from orator import DatabaseManager
from conexao import Conexao

class CrudUtil():

    con = None

    def __init__(self, link = 'padrao'):
        self.con = Conexao(link)

    def insert(self, tabela, camposValores):
        return self.con.qb().table(tabela).insert_get_id(camposValores)

    def update(self, tabela, where, camposValores):
        return self.con.qb().table(tabela).where(where).update(camposValores)

    def delete(self, tabela, where):
        return self.con.qb().table(tabela).where(where).delete()
