from PyPDF2 import PdfReader
from flask import *


reader = PdfReader('politica_viagens.pdf')
#Variável com o conteúdo do pdf em uma string
text = ''
for i in range(len(reader.pages)):
    page = reader.pages[i].extract_text()
    text += page

app = Flask(__name__)

json_salvo = {}

@app.route('/', methods=['GET'])
def testeget():
    data_set = {'teste':'funcionou'}
    json_dump = json.dumps(data_set)
    return json_dump


@app.route('/processo', methods=['POST'])
def obter_json():
    data = request.get_json()
    if not data:
        return {'error':'JSON inválido'}
    #até o momento o json é salvo, mas não tem mensagem confirmando
    global json_salvo
    json_salvo = data
    print(json_salvo)
    return 'recebemos o seu json'
if __name__=='__main__':
    app.run(port=7777)



