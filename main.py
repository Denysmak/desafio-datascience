from PyPDF2 import PdfReader
from flask import *
from langchain_google_genai import ChatGoogleGenerativeAI
import os


reader = PdfReader('politica_viagens.pdf')
#Variável com o conteúdo do pdf em uma string
text = ''
for i in range(len(reader.pages)):
    page = reader.pages[i].extract_text()
    text += page
api_key = 'AIzaSyDk30zoRZAaRJsJFTMXQk8OMjs4EsP4A5k'


os.environ['GOOGLE_API_KEY'] = api_key

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

json_salvo = {}


app = Flask(__name__)

modelo = {
"accepted": False,
"violated_policies": [
"Maximum trip duration exceeded (15 days)",
"Maximum ticket price exceeded (R$ 1.000,00)"
]
}


@app.route('/processo', methods=['POST'])
def obter_json():
    data = request.get_json()
    if not data:
        return {'error':'JSON inválido'}
    #até o momento o json é salvo, mas não tem mensagem confirmando
    global json_salvo
    json_salvo = data
    ai_msg = llm.invoke(f'leia esse texto:{text} e usando ela como base, me mande um json confirmando se essa requisição:{json_salvo} será aceita, use esse exemplo como modelo:{modelo}')
    return ai_msg.content
if __name__=='__main__':
    app.run(port=7777)
