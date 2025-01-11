from PyPDF2 import PdfReader
from flask import *
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

#Leitura do pdf, extração do conteúdo e transformação desse conteúdo em string
reader = PdfReader('politica_viagens.pdf')
text = ''
for i in range(len(reader.pages)):
    page = reader.pages[i].extract_text()
    text += page
    
load_dotenv()
api_key = os.getenv("API_KEY")
os.environ['GOOGLE_API_KEY'] = api_key

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pr",
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



import json

@app.route('/', methods=['POST'])
def obter_json():
    data = request.get_json()
    if not data:
        return {'error':'JSON inválido'}
    global json_salvo
    json_salvo = data


    ai_msg = llm.invoke(
    f"""
    Leia o seguinte texto de referência:
    {text}

    Com base nesse texto, avalie se a seguinte requisição será aceita:
        {json_salvo}

        Retorne um json no seguinte formato:
        {modelo}
    """).content.replace('json', '')
 
    formatted_string = json.dumps(ai_msg).strip()
    response_json = json.loads(formatted_string)
    return response_json

    
    

 
if __name__=='__main__':
    
    app.run(port=7777)