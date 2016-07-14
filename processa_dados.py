from processa_sql import processaSql
from conexao import Conexao
from crud_util import CrudUtil

class processaDados:

    con = None

    def __init__(self):
        self.con = Conexao()

    def getDadosPullRequest(self, data):

        pullRequest = data['pull_request']
        id          = pullRequest['id']
        name        = pullRequest['titlex']

        retorno = {
            'titulo': name,
            'id'    : id
        }

        dadosPullRequest = self.con.execLinha(processaSql().getDadosPullRequestSql(id))
        #Pull Request already exists
        if len(dadosPullRequest) > 0 :
            retorno['repositorioPullCod'] = dadosPullRequest['repositorioPullCod']
            merged = 'M' if pullRequest['merged'] == 'true' else 'N'
            if dadosPullRequest['repositorioPullStatus'] != merged :
                CrudUtil('prod_t1').update('repositorio_pull', {'repositorioPullCod': dadosPullRequest['repositorioPullCod']}, {
                    'repositorioPullStatus': "M"
                })
        else:
            self
        return "payload: "+ str(data)