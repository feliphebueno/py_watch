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
        dados = self.data

        #Novo Pull Request
        if evento == 'pull_request':
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

                return "OK"
            else:
                raise Exception("Payload incompleto ou em formato incorreto.")

        # Novo Push
        elif evento == 'push':
            repositorio = self.processaDados.getDadosRepo(dados['repository'])
            branches    = self.processaDados.getBranches(repositorio['repositorioCod'], dados['repository']['branches_url'][0:-9])
            usuarios    = {1}

            head = dados['head_commit']

            data = head['timestamp'][0:10]
            hora = head['timestamp'][11:-4]

            titulo = 'Novo Push no repositorio '+ repositorio['repositorioNome']
            descricao = 'Ultimo commit no branch '+ dados['ref']  +',<br /> por <strong>'+ head['author']['name'] +'</strong>, \
                         em <strong>'+ data +'</strong>, as <strong>'+ hora +'</strong>Arquivos adicionados: <strong>'+ \
                        str(len(head['added'])) +'</strong>. Removidos: <strong>'+ str(len(head['removed'])) +'</strong>. \
                        Alterados: <strong>'+ str(len(head['modified'])) +'</strong>';

            warnLevel   = 'warning';
            link        = head['url'];

            for usuarioCod in usuarios:
                self.processaDados.enviaNotificacao(usuarioCod, titulo, descricao, warnLevel, link)

            return "OK"
        else:
            return "Evento desconhecido"

