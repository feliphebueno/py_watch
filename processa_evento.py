# -*- coding: UTF-8 -*-
from processa_dados import processaDados
import json
class processaEvento:

    data = ''
    processaDados = None

    def __init__(self, data):
        self.data = data
        self.processaDados = processaDados()

    #Processa eventos no repositorio no Github
    def processaEvento(self, evento):

        #Novo Pull Request
        if evento == 'pull_request':
            dados = self.data
            dadosPullRequest = self.processaDados.getDadosPullRequest(dados)

            if 'action' in dados and dados['action'] == 'opened' and 'id' in dadosPullRequest:
                pull = dados['pull_request']
                usuarios = {1}

                head = pull['head']
                data = pull['created_at'][0:10]
                hora = pull['created_at'][11:-4]

                user  = self.processaDados.getDadosApi(dados['sender']['url'])
                stats = self.processaDados.getStatsPull(pull['commits_url'])

                titulo      = "Novo Pull Request no repositorio "+ dados['repository']['name']
                descricao   = 'Aberto por <strong>'+ user['name'] +'</strong>, em <strong>'+ data +'</strong>, as \
                               <strong>'+ hora +'</strong>Arquivos Alterados: <strong>'+ str(stats['files']) +'</strong>. \
                               Adi&otilde;es: <strong>'+ str(stats['add']) +'</strong>. Remo&ccedil;&otilde;es: <strong> '\
                               + str(stats['del']) +'</strong>',

                warnLevel   = 'danger';
                link        = pull['html_url'];

                for usuarioCod in usuarios:
                    self.processaDados.enviaNotificacao(usuarioCod, titulo, descricao, warnLevel, link)
            else:
                raise Exception("Payload incompleto ou em formato incorreto.")

        # Novo Push
        elif evento == 'push':
            ""
        else:
            ""
        return

