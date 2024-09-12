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
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]
        #st.write(document)
        # Configuração para a streaming
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            #stream=True,
        )
        
        # Inicializando o resumo na sessão
        st.session_state.summary = ""
        st.write(completion.choices[0].message.content)
        #st.write(dict(completion).get('usage'))
        #st.write(completion.model_dump_json(indent=2))
               
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
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            #stream=True,
        )
       
        st.write(completion.choices[0].message.content)
      
        st.write(st.session_state.summary)
        
        st.session_state.file_summary = st.session_state.file_name    
else: 
    st.write(" Carregue o Edital para análise")
