import config, sys
from orator import DatabaseManager

class Conexao():

    databases   = {}
    link        = None

    def __init__(self, link = 'padrao'):
        if config.configs['databases']:
            self.databases = config.configs['databases']
            self.link = link
        else:
            raise Exception("Index 'databases' nao encontrado na variavel config.")

    def qb(self, linkDb = ''):

        if linkDb != '':
            link = linkDb
        else:
            link = self.link

        try:
            if link in self.databases:
                database = self.databases[link]
                return DatabaseManager({
                    database['driver']: {
                        'driver'    : database['driver'],
                        'host'      : database['host'],
                        'database'  : database['database'],
                        'user'      : database['user'],
                        'password'  : database['password'],
                        'prefix'    : database['prefix']
                    }
                })
            else:
                raise Exception("O link '"+ link +"' nao foi encontrado na variavel config.")
        except Exception as e:
            raise Exception("Falha ao conectar ao banco de dados: \n"+ e[1])

    def execLinha(self, qb):
        linha = self.executar(qb)
        if len(linha) > 0 :
            return linha[0]
        else:
            return {}

    def executar(self, qb):
        return qb.get()