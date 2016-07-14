import sys, json
from processa_evento import processaEvento
response = {'success': "", 'response': ""}

def main(payload, evento):
    if payload and evento:
        trata = payload.replace("'", '"').replace('*space*', " ")
        data = json.loads(trata)

        try:
            processaEvento(data).processaEvento(evento)
            response['success'] = True
            response['response'] = "Requisicao processada com sucesso."
        except NameError as Undefined:
            response['success'] = False
            response['response'] = unicode(str(Undefined), errors='replace')
        except Exception as e:
            response['success'] = False
            response['response'] = unicode(str(e), errors='replace')
    else:
        response['success'] = False
        response['response'] = "Nenhum dado recebido para processamento."

    return response

if __name__ == "__main__":
    print json.dumps(main(sys.argv[1], sys.argv[2]))
