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
question = " faça um sumario do edital indicando apenas o contratante e o objeto do mesmo"
messages = [
            {"role": "system", "content": "Você é um especialista em editais públicos brasileiros para tecnologia da informação "},
            {"role": "user", "content": f"Here's a document: {document} \n\n---\n\n {question}"},
            {"role": "assistant", "content": "     ."}
        ]
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
