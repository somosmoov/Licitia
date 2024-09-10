import streamlit as st
import requests

st.markdown("# Moov - Analisador de Documentos 🎈")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")


bugs = st.Page("reports/bugs.py", title="Log de erros", icon=":material/bug_report:")#, default=True)
alerts = st.Page("reports/alerts.py", title="Alertas", icon=":material/notification_important:")#, default=True)

upload = st.Page("tools/upload.py", title="Carrega Edital", icon=":material/upload:")#, default=True)
search = st.Page("tools/search.py", title="Pesquisas", icon=":material/search:")#, default=True)
history = st.Page("tools/history.py", title="Historico", icon=":material/history:")#, default=True)
qa = st.Page("tools/qa.py", title="Carrega Documento", icon=":material/upload:", default=True)

if st.session_state.logged_in:  
    pg = st.navigation(
        {
            "Acesso": [logout_page],
            "Ferramentas": [qa], #upload],# search],history],
            #"Relatórios": [bugs, alerts],
            
        }
    )
else:
   pg = st.navigation([login_page])

pg.run()
