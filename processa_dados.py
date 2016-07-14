from processa_sql import processaSql
from conexao import Conexao
from crud_util import CrudUtil
from config import configs
import requests, json

class processaDados:

    con = None
    sql = None

    def __init__(self):
        self.con = Conexao()
        self.sql = processaSql()

    def getDadosPullRequest(self, data):

        pullRequest = data['pull_request']
        id          = pullRequest['id']
        name        = pullRequest['title']

        retorno = {
            'titulo': name,
            'id'    : id
        }

        dadosPullRequest = self.con.execLinha(self.sql.getDadosPullRequestSql(id))

        #Pull Request already exists
        if len(dadosPullRequest) > 0 :
            retorno['repositorioPullCod'] = dadosPullRequest['repositorioPullCod']
            merged = 'M' if pullRequest['merged'] == 'true' else 'N'
            print self.getDadosApi('https://api.github.com/users/feliphebueno')
            if dadosPullRequest['repositorioPullStatus'] != merged :
                CrudUtil('prod_t1').update('repositorio_pull', {'repositorioPullCod': dadosPullRequest['repositorioPullCod']}, {
                    'repositorioPullStatus': "M"
                })
        else:
            user = self.getDadosUser(pullRequest['user'])
            repo = self.getDadosRepo(data['repository'])

        return "payload: "+ str(data)

    def getDadosUser(self, userData):
        if 'login' in userData:
            login   = userData['login']
            id      = userData['id']
            retorno = {
                'login' : login,
                'id'    : id
            }
            contributor = self.con.execLinha(self.sql.getContributorSql(login))
        else:
            userName    = userData['name']
            email       = userData['email']
            retorno = {
                'userName' : userName,
                'email'    : email
            }

            contributor = self.con.execLinha(self.sql.getContributorSql(userName))

        #User already exists
        if len(contributor) > 0:
            retorno['contributorCod']   = contributor['contributorCod']
            retorno['contributorNome']  = contributor['contributorNome']
        else:
            urlUserAPI = userData['url'] if 'url' in userData else 'https://api.github.com/users/'. userData['userName']
            dadosUser = self.getDadosApi(urlUserAPI)

            contributorCod = CrudUtil('prod_t1').insert('contributor', {
                'contributorNome'  : dadosUser['name'],
                'contributorLogin': dadosUser['login'],
                'contributorId': dadosUser['id'],
                'contributorEmail': dadosUser['email'],
                'contributorAvatar': dadosUser['avatar_url'],
                'contributorUrl': dadosUser['html_url'],
                'contributorLocation': dadosUser['location'],
                'contributorUltimaAtualizacao': dadosUser['updated_at'],
            })

            retorno['contributorCod']   = contributorCod
            retorno['contributorNome']  = dadosUser['name']

        return retorno

    def getDadosRepo(self, repoData):

        id          = repoData['id']
        name        = repoData['name']
        fullName    = repoData['full_name']

        retorno = {
            'repositorioNome' : name,
            'repositorioFullName': fullName,
            'repositorioId': id,
        }

        repositorio = self.con.execLinha(self.sql.getRepositorioSql(id))

        #User already exists
        if len(repositorio) > 0:
            retorno['repositorioCod']   = repositorio['repositorioCod']
            retorno['repositorioNome']  = repositorio['repositorioNome']
        else:
            urlUserAPI = repoData['url'] if 'url' in repoData else 'https://api.github.com/users/'. repoData['userName']
            dadosUser = self.getDadosApi(urlUserAPI)

            contributorCod = CrudUtil('prod_t1').insert('contributor', {
                'contributorNome'  : dadosUser['name'],
                'contributorLogin': dadosUser['login'],
                'contributorId': dadosUser['id'],
                'contributorEmail': dadosUser['email'],
                'contributorAvatar': dadosUser['avatar_url'],
                'contributorUrl': dadosUser['html_url'],
                'contributorLocation': dadosUser['location'],
                'contributorUltimaAtualizacao': dadosUser['updated_at'],
            })

            retorno['contributorCod']   = contributorCod
            retorno['contributorNome']  = dadosUser['name']

        return retorno

    def getDadosApi(self, url, auth = True):

        if auth == True:
            user        = configs['apiKeys']['github']['user']
            password    = configs['apiKeys']['github']['password']
            r = requests.get(url, auth=(user, password))
        else:
            r = requests.get(url)

        if r.status_code == 200 and r.headers['Content-Type'] == 'application/json; charset=utf-8':
            response = r.json()
        else:
            raise Exception("Github API access failed. \nRequest headers: \n"+ str(r.headers))

        return response
