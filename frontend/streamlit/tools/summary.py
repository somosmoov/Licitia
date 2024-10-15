import streamlit as st
from openai import OpenAI
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
#openai_api_key = st.secrets["OPENAI_KEY"]

# Sete a URL do seu Key Vault
KEY_VAULT_URL = "https://keyvaultdesen.vault.azure.net/"
# Defina a URL do seu Key Vault
key_vault_url = KEY_VAULT_URL

# Crie um cliente para acessar o Key Vault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=key_vault_url, credential=credential)

# Acesse o segredo
secret_name = "OpenAI-API-Key"
retrieved_secret = client.get_secret(secret_name)

# Create an OpenAI client.
client = OpenAI(api_key=retrieved_secret.value)
#client = OpenAI(api_key=openai_api_key)

question = (
    "Atue como um expert em editais publicos, analise o edital fornecido e responda aos seguintes questionamentos:"
    "Qual é o Edital?, "
    "Qual o processo?,"
    "Modalidade?, "
    "Contratante ou interessado?, "
    "Descreva o objeto de forma objetiva, "
    "Valor da contratação,"
    "data de abertura?,"
    "horario de abertura?,"
    "criterio de julgamento?,"
    "PREFERÊNCIA ME/EPP/EQUIPARADAS",
    "modo de disputa? ",
    " endereço para entrega das propostas"    
)
instructions = (
    "Você receberá um documento e uma pergunta. "
    "Sua tarefa é responder à pergunta usando apenas o documento fornecido "
    "e citar a(s) passagem(s) do documento usado para responder à pergunta. "
    "Se o documento não contiver as respostas aos questionamentos relacione o respectivo questionamento com a resposta: informação não identificada no documento."
    "Se for fornecida uma resposta à pergunta, ela deverá ser anotada com uma citação. "
    "Use o seguinte formato para citar passagens relevantes: {\"Ref \":...}"
)
#if st.session_state.uploaded_file:
if 'uploaded_file' in st.session_state :
    #st.write("uploaded_file", st.session_state.uploaded_file)
    #st.write("file_summary", st.session_state.file_summary)
    if "file_summary" not in st.session_state:
        # Process the uploaded file and question.
        #document = uploaded_file.read().decode()
        st.write(" Edital em análise: ", st.session_state.file_name)
        document = st.session_state.doc
        messages = [
            {"role": "system", "content": f"Você é um especialista em editais públicos brasileiros para tecnologia da informação {instructions} "},
            {"role": "user", "content": f"Here's a document: {document} \n\n---\n\n {question}"},
            {"role": "assistant", "content": "quando referenciar a quantias em dinheiro utilize o Real como moeda e seu simbolo"}
        ]
        #st.write(document)
        # Configuração para a streaming
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            #stream=True,
        )      
        st.session_state.summary = completion.choices[0].message.content # https://platform.openai.com/docs/guides/chat-completions/response-format
        st.write(st.session_state.summary)
        st.session_state.file_summary = st.session_state.file_name        
    elif st.session_state.file_summary == st.session_state.file_name:
        #st.write("uploaded_file", st.session_state.uploaded_file)
        st.write(" Edital em análise: ", st.session_state.file_name)
        st.write( st.session_state.summary)
    else:
        st.write(" Edital em análise: ", st.session_state.file_name)
        document = st.session_state.doc
        messages = [
            {"role": "system", "content": f"Você é um especialista em editais públicos brasileiros para tecnologia da informação {instructions} "},
            {"role": "user", "content": f"Here's a document: {document} \n\n---\n\n {question}"},
            {"role": "assistant", "content": " "quando referenciar a quantias em dinheiro utilize o Real como moeda e seu simbolo"}
        ]
        #st.write(document)
        # Generate an answer using the OpenAI API.
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            #stream=True,
        )
        st.session_state.summary = completion.choices[0].message.content # https://platform.openai.com/docs/guides/chat-completions/response-format
        st.write(st.session_state.summary)               
        st.session_state.file_summary = st.session_state.file_name    
else: 
    st.write(" Carregue o Edital para análise")
