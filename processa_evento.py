from processa_dados import processaDados

class processaEvento:

    data = ''

    def __init__(self, data):
        self.data = data

    #Processa eventos no repositorio no Github
    def processaEvento(self, evento):

        #Novo Pull Request
        if evento == 'pull_request':
            dadosPullRequest = processaDados().getDadosPullRequest(self.data)
            data = self.data
            if 'action' in data and data['action'] == 'opened':
                pull = data['pull_request']
                head = pull['head']
                dataHora = pull['created_at'][0:10] + ' ' + pull['created_at'][11:-4]
            else:
                raise Exception("Payload incompleto ou em formato incorreto.")

        # Novo Push
        elif evento == 'push':
            ""
        else:
            ""
        return

