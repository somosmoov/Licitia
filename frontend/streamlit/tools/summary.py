import streamlit as st
import openai
from openai import OpenAI
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
#openai_api_key = st.text_input("OpenAI API Key", type="password")
def setup_openai_api():
    openai.api_key = st.secrets["OPENAI_KEY"]

# Defina a URL do seu Key Vault
#key_vault_url = KEY_VAULT_URL

# Crie um cliente para acessar o Key Vault
#credential = DefaultAzureCredential()
#client = SecretClient(vault_url=key_vault_url, credential=credential)

# Acesse o segredo
#secret_name = "OpenAI-API-Key"
#retrieved_secret = client.get_secret(secret_name)
#st.write("A chave da API da OpenAI é:", retrieved_secret.value)
#st.write("VALOR recuperado:", retrieved_secret)

# Create an OpenAI client.
#client = OpenAI(api_key=retrieved_secret.value)
# Chamada da função de configuração
setup_openai_api()
#client = OpenAI(api_key=openai_api_key)

# Ask the user for a question via `st.text_area`.
#question = st.text_input(
#    "Faça um questionamento",
#    placeholder="Por exemplo: Pode fornecer um sumário?",
#    disabled=not uploaded_file,
#)
question = " faça um sumario do edital indicando apenas o contratante e o objeto do mesmo"
#if st.session_state.uploaded_file:
if 'uploaded_file' in st.session_state and st.session_state.uploaded_file:
    #st.write("uploaded_file", st.session_state.uploaded_file)
    #st.write("file_summary", st.session_state.file_summary)
    if "file_summary" not in st.session_state:
        # Process the uploaded file and question.
        #document = uploaded_file.read().decode()
        st.write(" Edital em análise: ", st.session_state.file_name)
        document = st.session_state.doc
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]
        #st.write(document)
        # Configuração para a streaming
        stream = openai.ChatCompletion.create(
            #model="gpt-3.5-turbo",
            model="gpt-4-0613",
            messages=messages,
            stream=True,
        )
        # Inicializando o resumo na sessão
         # Inicializando o resumo na sessão
        st.session_state.summary = ""

        # Iterando sobre a stream e acumulando as mensagens
        for chunk in stream:
            if 'choices' in chunk and len(chunk['choices']) > 0:
                delta = chunk['choices'][0]['delta'].get('content', '')
                st.session_state.summary += delta
                st.write(st.session_state.summary)
        st.session_state.file_summary = st.session_state.file_name
        
    elif st.session_state.file_summary == st.session_state.file_name:
        #st.write("uploaded_file", st.session_state.uploaded_file)
        st.write("Arquivo sumarizado",st.session_state.file_summary)
        st.write("Sumario: ", st.session_state.summary)
    else:
        st.write(" Edital em análise: ", st.session_state.file_name)
        document = st.session_state.doc
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]
        #st.write(document)
        # Generate an answer using the OpenAI API.
        stream = openai.ChatCompletion.create(
            #model="gpt-3.5-turbo",
            model="gpt-4-0613",
            messages=messages,
            stream=True,
        )
        # Inicializando o resumo na sessão
        st.session_state.summary = ""
        # Iterando sobre a stream e acumulando as mensagens
        for chunk in stream:
            if 'choices' in chunk and len(chunk['choices']) > 0:
                delta = chunk['choices'][0]['delta'].get('content', '')
                st.session_state.summary += delta
                st.write(st.session_state.summary)
        
        st.session_state.file_summary = st.session_state.file_name    
else: 
    st.write(" Carregue o Edital para análise")
