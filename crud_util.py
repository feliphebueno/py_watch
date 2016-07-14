from orator import DatabaseManager
from conexao import Conexao

class CrudUtil():

    con = None

    def __init__(self, link = 'padrao'):
        self.con = Conexao(link)

    def insert(self, tabela, camposValores):
        try:
            self.con.qb().begin_transaction()
            id = self.con.qb().table(tabela).insert_get_id(camposValores)
            self.con.qb().commit()
            return id
        except Exception as e:
            self.con.qb().rollback()
            raise Exception("Database transaction failed. Details: "+ str(e))

    def update(self, tabela, where, camposValores):
        try:
            self.con.qb().begin_transaction()
            id = self.con.qb().table(tabela).where(where).update(camposValores)
            self.con.qb().commit()
            return id
        except Exception as e:
            self.con.qb().rollback()
            raise Exception("Database transaction failed. Details: " + str(e))

    def delete(self, tabela, where):
        try:
            self.con.qb().begin_transaction()
            id = self.con.qb().table(tabela).where(where).delete()
            self.con.qb().commit()
            return id
        except Exception as e:
            self.con.qb().rollback()
            raise Exception("Database transaction failed. Details: " + str(e))
