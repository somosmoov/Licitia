import streamlit as st
from openai import OpenAI
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.secrets["OPENAI_KEY"]

# Defina a URL do seu Key Vault
#key_vault_url = KEY_VAULT_URL

# Crie um cliente para acessar o Key Vault
#credential = DefaultAzureCredential()
#client = SecretClient(vault_url=key_vault_url, credential=credential)

# Create an OpenAI client.
#client = OpenAI(api_key=retrieved_secret.value)
client = OpenAI(api_key=openai_api_key)
question = " Analise o edital fornecido e responda aos seguintes questionamentos: Tem conta vinculada?, Solicita planilha de custos e formação de preços?, Qual o modo de disputa?, Qual o valor orçado?, Tem salário mínimo?, Edital se baseia em qual a lei?, Qual a vigência?, Quais documentos para faturamento?, Pede declaração de Contratos firmados?, Quais os documentos para faturamento?, Quaisosperfis? "
instructions = (
    "Você receberá um documento e uma pergunta. "
    "Sua tarefa é responder à pergunta usando apenas o documento fornecido "
    "e citar a(s) passagem(s) do documento usado para responder à pergunta. "
    "Se o documento não contiver as informações necessárias para responder a esta questão, "
    "basta escrever: Informação insuficiente. "
    "Se for fornecida uma resposta à pergunta, ela deverá ser anotada com uma citação. "
    "Use o seguinte formato para citar passagens relevantes: {...}"
)
#if st.session_state.uploaded_file:
if 'uploaded_file' in st.session_state :
    #st.write("uploaded_file", st.session_state.uploaded_file)
    #st.write("file_analitic", st.session_state.file_analitic)
    if "file_analitic" not in st.session_state:
        # Process the uploaded file and question.
        #document = uploaded_file.read().decode()
        st.write(" Edital em análise: ", st.session_state.file_name)
        document = st.session_state.doc
        # Generate an answer using the OpenAI API.
        messages = [
            {"role": "system", "content": f"Você é um especialista em editais públicos brasileiros para tecnologia da informação {instructions} "},
            {"role": "user", "content": f"Here's a document: {document} \n\n---\n\n {question}"},
            {"role": "assistant", "content": "     ."}
        ]
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            #stream=True,
        )      
        st.session_state.analitic = completion.choices[0].message.content # https://platform.openai.com/docs/guides/chat-completions/response-format
        st.write(st.session_state.analitic)
        st.session_state.file_analitic = st.session_state.file_name        
    elif st.session_state.file_analitic == st.session_state.file_name:
        #st.write("uploaded_file", st.session_state.uploaded_file)
        st.write("Arquivo sumarizado",st.session_state.file_analitic)
        st.write("Sumario: ", st.session_state.analitic)
    else:
        st.write(" Edital em análise: ", st.session_state.file_name)
        document = st.session_state.doc
        # Generate an answer using the OpenAI API.
        messages = [
            {"role": "system", "content": f"Você é um especialista em editais públicos brasileiros para tecnologia da informação {instructions} "},
            {"role": "user", "content": f"Here's a document: {document} \n\n---\n\n {question}"},
            {"role": "assistant", "content": "     ."}
        ]
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
