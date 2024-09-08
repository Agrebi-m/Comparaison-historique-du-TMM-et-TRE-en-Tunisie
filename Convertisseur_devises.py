from bs4 import BeautifulSoup
import requests
import streamlit as st
import pandas as pd

url = 'https://www.bct.gov.tn/bct/siteprod/cours.jsp'
page = requests.get(url) 
soup = BeautifulSoup(page.text, 'html.parser')

journey = soup.find_all('h5')[1]

table = soup.find_all('tbody')[0]
rows = table.find_all('tr')

data = []

for row in rows:
    cols = [data.text.strip() for data in row.find_all('td')]
    data.append(cols)

TND_ROW = pd.DataFrame({'Monnaie': ['DINAR TUNISIEN'], 'Symbole': ['TND'], 'Unité': ['1'], 'Valeur': ['1']})
devises_table = pd.DataFrame(data, columns=['Monnaie','Symbole','Unité','Valeur'])

devises_table = pd.concat([TND_ROW, devises_table], ignore_index=True)

symbol_table = pd.DataFrame({'':['🇹🇳','🇩🇿','🇸🇦','🇨🇦','🇩🇰','🇺🇸','🇬🇧','🇯🇵','🇲🇦','🇳🇴','🇸🇪','🇨🇭','🇰🇼','🇦🇪','🇪🇺','🇱🇾','🇲🇷','🇧🇭','🇶🇦','🇨🇳']})
final_devises_table = pd.concat([symbol_table, devises_table], axis=1)

final_devises_table['Valeur'] = final_devises_table['Valeur'].str.replace(',','.').astype(float)
final_devises_table['Unité'] = final_devises_table['Unité'].str.replace(',','.').astype(float)


with open("style.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True) 

st.markdown('''
<p style="color: rgb(168, 168, 168);">💷 DEVISES ></p>
''', unsafe_allow_html=True)

st.markdown('''
  <p class='title' style="font-weight: 700; font-size: 3rem; line-height: 100%;">Cours Moyens des Devises Cotées en dinar tunisien 🇹🇳</p>  
            
            ''', unsafe_allow_html=True)

st.markdown('''
 <a href="https://www.bct.gov.tn/bct/siteprod/index.jsp">Source: BCT de Tunis</a>
''', unsafe_allow_html=True)

st.subheader(journey.text)

st.divider()

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader('💴 Cours de change')
        final_devises_table.loc[19, 'Monnaie'] = final_devises_table.loc[19, 'Monnaie'].upper()
        st.dataframe(final_devises_table, hide_index=True, height=737)        
        
    with col2:
        
        st.subheader('🪄 Convertisseur de devises')
        devises = [
    '🇹🇳 - DINAR TUNISIEN',
    '🇩🇿 - DINAR ALGERIEN',
    '🇸🇦 - RYAL SAOUDIEN',
    '🇨🇦 - DOLLAR CANADIEN',
    '🇩🇰 - COURONNE DANOISE',
    '🇺🇸 - DOLLAR DES USA',
    '🇬🇧 - LIVRE STERLING',
    '🇯🇵 - YEN JAPONAIS',
    '🇲🇦 - DIRHAM MAROCAIN',
    '🇳🇴 - COURONNE NORVEGIENNE',
    '🇸🇪 - COURONNE SUEDOISE',
    '🇨🇭 - FRANC SUISSE',
    '🇰🇼 - DINAR KOWEITIEN',
    '🇦🇪 - DIRHAM DES EAU',
    '🇪🇺 - EURO',
    '🇱🇾 - DINAR LIBYEN',
    '🇲🇷 - OUGUIYA MAURITANIEN',
    '🇧🇭 - DINAR DE BAHREIN',
    '🇶🇦 - RYAL QUATARI',
    '🇨🇳 - YUAN CHINOIS'
]

        De = st.selectbox("De :", devises, index=14, placeholder="Selectionnez votre devises ...")
        
        if De != '🇹🇳 - DINAR TUNISIEN' and De is not None :
            A = '🇹🇳 - DINAR TUNISIEN'
            st.write(f"A : {A}")           
        else:
            A = st.selectbox("A :", devises, index=None, placeholder="Selectionnez votre devises ...")

        Amount = st.text_input("Montant :")
        
        if st.button("Convertir", type='primary'):
            try:
               
            # Conversion de devise à dinar
                if De != '🇹🇳 - DINAR TUNISIEN':
                    de_table = final_devises_table[final_devises_table['Monnaie'] == De.split('-')[1].strip()]
                    a_table = final_devises_table[final_devises_table['Monnaie'] == A.split('-')[1].strip()]
                    final_table = pd.concat([de_table, a_table], axis=0).reset_index(drop=True)
                    st.write('📅 Résultat de conversion :')
                    st.dataframe(final_table, hide_index=True, use_container_width=True)
                    
                    de_unit = final_table.loc[0, 'Unité']
                    de_value = final_table.loc[0, 'Valeur']
                    a_unit = final_table.loc[1, 'Unité']
                    a_value = final_table.loc[1, 'Valeur']
              
                    Amount_float = float(Amount)  
                    converted_amount = (Amount_float * de_value) / de_unit
                    st.success(f'{Amount_float} {final_table.loc[0, 'Symbole']} = {converted_amount} {final_table.loc[1, 'Symbole']} ')
                else:
                    de_table = final_devises_table[final_devises_table['Monnaie'] == De.split('-')[1].strip()]
                    a_table = final_devises_table[final_devises_table['Monnaie'] == A.split('-')[1].strip()]
                    final_table = pd.concat([de_table, a_table], axis=0).reset_index(drop=True)
                    st.write('📅 Résultat de conversion :')
                    st.dataframe(final_table, hide_index=True, use_container_width=True)
                    
                    de_unit = final_table.loc[0, 'Unité']
                    de_value = final_table.loc[0, 'Valeur']
                    a_unit = final_table.loc[1, 'Unité']
                    a_value = final_table.loc[1, 'Valeur']
              
                    Amount_float = float(Amount)  
                    converted_amount = (Amount_float / a_value) * a_unit
                    st.success(f'{Amount_float} {final_table.loc[0, 'Symbole']} = {converted_amount} {final_table.loc[1, 'Symbole']} ')

                  
            except ValueError as e:
                st.exception(e)
        
        

                    


                
                
            
               
            





    








# Coder
st.sidebar.markdown('''
        <div class="coder">
            <p><br>✌️ Elaboré par: <span style="font-weight: 700">Mohamed Agrebi</span></p>
            <a href="https://www.linkedin.com/in/mohamed-agrebi-053799174/">LinkedIn</a>
        </div>
            
            ''', unsafe_allow_html=True)

  


