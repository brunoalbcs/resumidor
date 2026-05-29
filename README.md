# Resumidor de PDF e TXT
Aplicação simples para resumir documentos com IA

<img width="1874" height="921" alt="resumidor_readme" src="https://github.com/user-attachments/assets/0ff2f542-bb36-47d1-aebf-607e5d62b701" />

### Pré-requisito: Chave de API
Para utilizar a inteligência artificial, é necessário criar uma chave de API no Google AI Studio. 
Acesse o site [Google AI Studio](https://aistudio.google.com/app/apikey), faça login com sua conta Google e gere uma chave rápida e gratuitamente. Após gerar, basta colar a chave na barra lateral da aplicação.

### Como rodar o projeto

Crie e ative um ambiente virtual:
```bash
python -m venv venv
# No Windows: venv\Scripts\activate
# No Linux/Mac: source venv/bin/activate
```

Instale as dependências:
```bash
pip install -r requirements.txt
```

Execute a aplicação:
```bash
streamlit run app.py
```
