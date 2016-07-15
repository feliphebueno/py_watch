from processa_sql import processaSql
from conexao import Conexao
from crud_util import CrudUtil
from config import configs
import requests, json, datetime, sys

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

            if dadosPullRequest['repositorioPullStatus'] != merged :
                CrudUtil('prod_t1').update('repositorio_pull', {'repositorioPullCod': dadosPullRequest['repositorioPullCod']}, {
                    'repositorioPullStatus': "M"
                })
        else:
            user = self.getDadosUser(pullRequest['user'])
            repo = self.getDadosRepo(data['repository'])

            repositorioPullCod = CrudUtil('prod_t1').insert('repositorio_pull', {
                'repositorioCod': repo['repositorioCod'],
                'contributorCod': user['contributorCod'],
                'repositorioPullId': pullRequest['id'],
                'repositorioPullTitulo': pullRequest['title'],
                'repositorioPullMensagem': pullRequest['body'],
                'repositorioPullUrl': pullRequest['url'],
                'repositorioPullMesclavel': 'S' if pullRequest['mergeable'] == 'true' else 'N',
                'repositorioPullComentarios': pullRequest['comments'],
                'repositorioPullCommits': pullRequest['commits'],
                'repositorioPullAdicoes': pullRequest['additions'],
                'repositorioPullRemocoes': pullRequest['deletions'],
                'repositorioPullArquivosAlterados': pullRequest['changed_files'],
                'repositorioPullData': pullRequest['created_at'][0:10],
                'repositorioPullDataMerged': None if type(pullRequest['merged_at']) != str else pullRequest['merged_at'][0:10],
                'repositorioPullStatus': 'M' if pullRequest['merged'] == 'true' else 'N',
            })

            retorno['repositorioPullCod'] = repositorioPullCod

        return retorno

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
                'contributorUltimaAtualizacao': dadosUser['updated_at'][0:10],
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

        #Repo already exists
        if len(repositorio) > 0:
            retorno['repositorioCod']   = repositorio['repositorioCod']
            retorno['repositorioNome']  = repositorio['repositorioNome']
        else:
            urlRepoAPI = 'https://api.github.com/repos/'+ repoData['full_name']
            dadosRepo = self.getDadosApi(urlRepoAPI)
            dadosOwner = self.getDadosUser(dadosRepo['owner'])

            repositorioCod = CrudUtil('prod_t1').insert('repositorio', {
                'repositorioOwnerCod'               : dadosOwner['contributorCod'],
                'repositorioId'                     : dadosRepo['id'],
                'repositorioNome'                   : dadosRepo['name'],
                'repositorioFullName'               : dadosRepo['full_name'],
                'repositorioDescricao'              : dadosRepo['description'],
                'repositorioPrivado'                : 'S' if dadosRepo['private'] == True else 'N',
                'repositorioUrl'                    : dadosRepo['html_url'],
                'repositorioUrlTeam'                : dadosRepo['teams_url'],
                'repositorioUrlBranches'            : dadosRepo['branches_url'],
                'repositorioDataCriacao'            : dadosRepo['created_at'][0:10],
                'repositorioDataUltimaAtualizacao'  : dadosRepo['updated_at'][0:10],
            })

            retorno['repositorioCod']   = repositorioCod

        return retorno

    def getStatsPull(self, commitsUrl):

        commits = self.getDadosApi(commitsUrl)

        files   = 0
        add     = 0
        deleted = 0

        for commit in commits:
            dados = self.getDadosApi(commit['url'])

            files   += len(dados['files'])
            add     += dados['stats']['additions']
            deleted += dados['stats']['deletions']

        return {
            'files' : files,
            'add'   : add,
            'del'   : deleted
        }


    def enviaNotificacao(self, usuarioCod, titulo, descricao, warnLevel, link):

        camposValores = {
            'usuarioCod': 2,#remetente
            'notificacaoUsuarioCod': usuarioCod,#destinatario
            'notificacaoTitulo': titulo,
            'notificacaoDesc': descricao,
            'notificacaoWarnLevel': warnLevel,
            'notificacaoDataHora': str(datetime.datetime.now())[0:-7],
            'notificacaoLink': link,
        }

        #t1
        repositorioCod = CrudUtil('prod_t1').insert('_notificacao', camposValores)

        #s2(only in production
        #repositorioCod = CrudUtil('prod_s2').insert('_notificacao', camposValores)

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
