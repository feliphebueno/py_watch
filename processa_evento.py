# -*- coding: UTF-8 -*-
from processa_dados import processaDados
import json, sys
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

            pull = dados['pull_request']
            usuarios = {1}

            head = pull['head']

            if 'action' in dados and dados['action'] == 'opened' and 'id' in dadosPullRequest:

                user = self.processaDados.getDadosUser(dados['pull_request']['user'])
                #stats = self.processaDados.getStatsPull(pull['commits_url'])

                data = pull['created_at'][0:10]
                hora = pull['created_at'][11:-4]

                titulo      = "Novo Pull Request no repositorio "+ dados['repository']['name']
                descricao   = 'Aberto por <strong>'+ user['contributorNome'] +'</strong>, em <strong>'+ data +'</strong>, as \
                               <strong>'+ hora +'</strong>Arquivos Alterados: <strong>'+ str(pull['changed_files']) +'</strong>. \
                               Adi&otilde;es: <strong>'+ str(pull['additions']) +'</strong>. Remo&ccedil;&otilde;es: <strong> '\
                               + str(pull['deletions']) +'</strong>',

            elif 'action' in dados and dados['action'] == 'closed' and 'id' in dadosPullRequest:

                user = self.processaDados.getDadosUser(pull['merged_by'])

                data = pull['merged_at'][0:10]
                hora = pull['merged_at'][11:-4]

                merged = "Mesclado" if pull['merged'] == True else "Nao mesclado"

                titulo      = "Pull Request <strong>"+ pull['title'] +"</strong> no repositorio "+ dados['repository']['name'] +" fechado."
                descricao   = 'Fechado por <strong>'+ user['contributorNome'] +'</strong>, em <strong>'+ data +'</strong>, as \
                               <strong>'+ hora +'</strong>, com status de <strong>'+ merged +'</strong>.'
            else:
                raise Exception("Payload incompleto ou em formato incorreto.")

            warnLevel = 'danger';
            link = pull['html_url'];

            for usuarioCod in usuarios:
                self.processaDados.enviaNotificacao(usuarioCod, titulo, descricao, warnLevel, link)

            return "OKZ"
        # Novo Push
        elif evento == 'push':
            repositorio = self.processaDados.getDadosRepo(dados['repository'])
            self.processaDados.getBranches(repositorio['repositorioCod'], dados['repository']['branches_url'][0:-9])
            usuarios    = {1}

            head = dados['head_commit']

            data = head['timestamp'][0:10]
            hora = head['timestamp'][11:-4]

            titulo = 'Novo Push no repositorio '+ repositorio['repositorioNome']
            descricao = 'Ultimo commit no branch '+ dados['ref']  +',<br /> por <strong>'+ head['author']['name'] +'</strong>, \
                         em <strong>'+ data +'</strong>, as <strong>'+ hora +'</strong>Arquivos adicionados: <strong>'+ \
                        str(len(head['added'])) +'</strong>. Removidos: <strong>'+ str(len(head['removed'])) +'</strong>. \
                        Alterados: <strong>'+ str(len(head['modified'])) +'</strong>.';

            warnLevel   = 'warning';
            link        = head['url'];

            for usuarioCod in usuarios:
                self.processaDados.enviaNotificacao(usuarioCod, titulo, descricao, warnLevel, link)

            return "OKX"
           #Novo branch
        elif evento == 'create':
            if 'ref_type'in dados and dados['ref_type'] == "branch":

                usuarios = {1}

                user = self.processaDados.getDadosUser(dados['sender'])
                repositorio = self.processaDados.getDadosRepo(dados['repository'])

                self.processaDados.getBranches(repositorio['repositorioCod'], dados['repository']['branches_url'][0:-9])

                data = dados['repository']['pushed_at'][0:10]
                hora = dados['repository']['pushed_at'][11:-4]

                titulo = 'Novo Branch criado no repositorio ' + repositorio['repositorioNome']
                descricao = 'Branch ' + dados['ref'] + ' criado por <strong>' + user['contributorNome']+ '</strong>.';

                warnLevel = 'warning';
                link = dados['repository']['url'] +"/tree/"+ dados['ref'];

                for usuarioCod in usuarios:
                    self.processaDados.enviaNotificacao(usuarioCod, titulo, descricao, warnLevel, link)

                return "OKX"
        else:
            return "Evento desconhecido"

