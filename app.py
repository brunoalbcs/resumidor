import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os

# 1. CONFIGURAÇÃO DA PÁGINA
# Deixa a página mais larga para acomodar melhor a janela dividida (esquerda/direita)
st.set_page_config(page_title="Resumidor de Documentos", layout="wide")

st.title("Resumidor de Documentos")
st.write("Faça o upload do documento para resumir.")

# 2. CHAVE DA API (Segurança)
# Usamos o markdown para criar um link clicável na barra lateral
st.sidebar.markdown("https://aistudio.google.com/app/api-keys")
# Criamos um campo de senha na barra lateral para você colocar sua chave do Google
api_key = st.sidebar.text_input("Acesse o site acima e cole sua chave de API aqui:", type="password")


# 3. DIVIDINDO A TELA EM DUAS COLUNAS
# col_esquerda será a janela de upload, col_direita será a do resumo
col_esquerda, col_direita = st.columns(2)

# ==========================================
# JANELA DA ESQUERDA (UPLOAD E EXTRAÇÃO)
# ==========================================
with col_esquerda:
    st.subheader("Upload de Arquivo")

    # O file_uploader permite vários tipos de arquivos. Vamos suportar PDF e TXT.
    arquivo_enviado = st.file_uploader("Arraste um arquivo PDF ou TXT", type=["pdf", "txt"])

    texto_extraido = ""  # Variável que vai guardar todo o texto do documento

    if arquivo_enviado is not None:
        # A biblioteca 'os' nos ajuda a pegar a extensão do arquivo (ex: '.pdf' ou '.txt')
        extensao = os.path.splitext(arquivo_enviado.name)[1].lower()

        st.info(f"Arquivo recebido: {arquivo_enviado.name}")

        # LÓGICA PARA ARQUIVO TXT (Nativo do Python, muito fácil)
        if extensao == ".txt":
            # Lê o arquivo direto e decodifica para texto (string)
            texto_extraido = arquivo_enviado.getvalue().decode("utf-8")
            st.success("Texto extraído com sucesso do arquivo TXT!")

        # LÓGICA PARA ARQUIVO PDF (Usando a biblioteca PyPDF)
        elif extensao == ".pdf":
            # Inicializa o leitor de PDF
            leitor_pdf = PdfReader(arquivo_enviado)

            # Loop que passa por todas as páginas e junta o texto
            for pagina in leitor_pdf.pages:
                texto_extraido += pagina.extract_text() + "\n"

            st.success(f"Texto extraído com sucesso! (Total de {len(leitor_pdf.pages)} páginas)")

        # Mostramos uma prévia do texto extraído para o usuário ver que funcionou
        with st.expander("Ver texto bruto extraído (Prévia)"):
            st.text(texto_extraido[:1000] + "... [texto truncado]")

# ==========================================
# JANELA DA DIREITA (IA E RESUMO)
# ==========================================
with col_direita:
    st.subheader("Resumo com Inteligência Artificial")

    # Só mostramos o botão se a pessoa já enviou um arquivo
    if arquivo_enviado is not None:

        if st.button("Gerar Resumo com IA"):

            # Validação: Verifica se o usuário colocou a chave da API
            if not api_key:
                st.error("Por favor, coloque sua chave da API do Gemini na barra lateral esquerda.")
            else:
                with st.spinner("A IA está lendo seu documento..."):
                    try:
                        # 1. LIMPEZA DA CHAVE (Resolve o erro 403 de espaço em branco)
                        api_key_limpa = api_key.strip()
                        genai.configure(api_key=api_key_limpa)

                        # 2. SELEÇÃO DO MODELO FLASH-LITE
                        # Modelo ultrarrápido ideal para resumos de texto
                        modelo = genai.GenerativeModel('gemini-2.5-flash-lite')

                        # Criando o Prompt
                        prompt = f"""
                                Você é um assistente especialista em analisar documentos.
                                Leia o texto abaixo e gere um resumo claro e estruturado, destacando:
                                1. O objetivo principal do documento.
                                2. Os principais tópicos abordados.

                                Texto do documento:
                                {texto_extraido}
                                """

                        # Chamando a função
                        resposta = modelo.generate_content(prompt)

                        # Mostrando o resultado
                        st.markdown(resposta.text)

                    except Exception as erro:
                        # Tratamento de erro caso a chave esteja errada ou a internet caia
                        st.error(f"Ocorreu um erro ao comunicar com a IA: {erro}")
    else:
        st.warning("Aguardando você enviar um documento.")