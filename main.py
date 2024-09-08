import streamlit as st

st.set_page_config(page_title="Comparaison Historique du TMM et TRE en Tunisie", page_icon="📊", layout="wide")

Evolution_TMM = st.Page("Evolution_TMM.py", title="Évolution du TMM", icon=":material/show_chart:")
Evolution_TRE = st.Page("Evolution_TRE.py", title="Évolution du TRE", icon=":material/elevation:")
Comparaison_TMM_TRE = st.Page("Comparaison__variations_TMM_vs_TRE.py", title="Comparaison Historique du TMM et TRE", icon=":material/ssid_chart:")
Convertisseur_devises = st.Page("Convertisseur_devises.py", title='Convertisseur de devises', icon=':material/payments:')

pg = st.navigation({'Pages/ ' : [Evolution_TMM, Evolution_TRE, Comparaison_TMM_TRE],'Outils/' : [Convertisseur_devises]})
pg.run()

