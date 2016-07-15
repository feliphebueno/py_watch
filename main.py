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

__author__ = "Bueno, Feliphe <feliphezion@gmail.com>"
__version__ = "2.0"

response = {'success': "", 'response': ""}

def main(payload, evento):
    if payload and evento:
        trata = payload.replace("'", '"').replace('*space*', " ")
        data = json.loads(trata)
        try:
            print processaEvento(data).processaEvento(evento)
            response['success'] = True
            response['response'] = "Requisicao processada com sucesso."
        except NameError as Undefined:
            response['success'] = False
            response['response'] = unicode(str(Undefined), errors='replace')
            response['stackTrace'] = traceback.format_exc()
        except Exception as e:
            response['success'] = False
            response['response'] = unicode(str(e), errors='replace')
            response['stackTrace'] = traceback.format_exc()
    else:
        response['success'] = False
        response['response'] = "Nenhum dado recebido para processamento."

    return response

if __name__ == "__main__":
    response = main(sys.argv[1], sys.argv[2])
    print json.dumps(response)
    if len(sys.argv) > 3:
        if sys.argv[3] == '--debug' and 'stackTrace' in response:
            print "Stack Trace:\n"+ response['stackTrace']
