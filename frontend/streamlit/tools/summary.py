import streamlit as st
from openai import OpenAI
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
#openai_api_key = st.text_input("OpenAI API Key", type="password")
openai_api_key = st.secrets["OPENAI_KEY"]

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
client = OpenAI(api_key=openai_api_key)

# Ask the user for a question via `st.text_area`.
#question = st.text_input(
#    "Faça um questionamento",
#    placeholder="Por exemplo: Pode fornecer um sumário?",
#    disabled=not uploaded_file,
#)
question = " faça um sumario do edital indicando apenas o contratante e o objeto do mesmo"
if st.session_state.uploaded_file & ("file_summary" not in st.session_state):
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
    # Generate an answer using the OpenAI API.
    stream = client.chat.completions.create(
        #model="gpt-3.5-turbo",
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )

    # Stream the response to the app using `st.write_stream`.
    st.write_stream(stream)
    st.session_state.file_summary = st.session_state.file_name
    st.session_state.summary = stream
elif st.session_state.uploaded_file & (st.session_state.file_summary == st.session_state.file_name):
     st.write_stream(stream)
else: 
    st.write(" Carregue o Edital para análise")
