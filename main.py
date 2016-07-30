"""
    Sappiens Framework
    Copyright (C) 2014, BRA Consultoria

    Website do autor: www.braconsultoria.com.br/sappiens
    Email do autor: sappiens@braconsultoria.com.br

    Website do projeto, equipe e documentacao: www.sappiens.com.br

    Este programa e software livre; voce pode redistribui-lo e/ou
    modifica-lo sob os termos da Licenca Publica Geral GNU, conforme
    publicada pela Free Software Foundation, versao 2.

    Este programa e distribuido na expectativa de ser util, mas SEM
    QUALQUER GARANTIA; sem mesmo a garantia implicita de
    COMERCIALIZACAO ou de ADEQUACAO A QUALQUER PROPOSITO EM
    PARTICULAR. Consulte a Licenca Publica Geral GNU para obter mais
    detalhes.

    Voce deve ter recebido uma copia da Licenca Publica Geral GNU
    junto com este programa; se nao, escreva para a Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
    02111-1307, USA.

    Copias da licenca disponiveis em /Sappiens/_doc/licenca


"""

import sys, json, traceback
from processa_evento import processaEvento
from flask import Flask, request

__author__ = "Bueno, Feliphe <feliphezion@gmail.com>"
__version__ = "2.0"

def start(payload, evento):
    if payload and evento:
        retorno = {
            'success': True,
            'retorno': str(processaEvento(payload).processaEvento(evento)),
        }
    else:
        retorno = {
            'success': False,
            'retorno': "Nenhum dado recebido para processamento."
        }

    return retorno

app = Flask(__name__)
@app.route("/", methods=['POST'])
def main():
    response = {'success': "", 'response': ""}
    try:
        payload = request.get_json(True)

        retorno = start(payload, request.headers.get("Http-X-Github-Event"))
        response = {
            'success' : retorno['success'],
            'retorno' : retorno['retorno']
        }
    except NameError as Undefined:
        response['success'] = False
        response['response'] = unicode(str(Undefined), errors='replace')
        response['stackTrace'] = '<pre>' + traceback.format_exc() + '</pre>'
    except Exception as e:
        response['success'] = False
        response['response'] = unicode(str(e), errors='replace')
        response['stackTrace'] = '<pre>' + traceback.format_exc() + '</pre>'
    finally:
        if len(sys.argv) > 3:
            if request.headers.get("--debug") and 'stackTrace' in response:
                print "Stack Trace:\n" + response['stackTrace']

        return str(response)

@app.route("/")
def hello():
    return "<h1>Python flask server http/1.1 200 OK</h1>"

if __name__ == "__main__":
    app.run(host='localhost', port=8081, debug=True)