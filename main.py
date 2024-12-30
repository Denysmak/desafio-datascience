from PyPDF2 import PdfReader

reader = PdfReader('politica_viagens.pdf')
#Variável com o conteúdo do pdf em uma string
text = ''
for i in range(len(reader.pages)):
    page = reader.pages[i].extract_text()
    text += page




