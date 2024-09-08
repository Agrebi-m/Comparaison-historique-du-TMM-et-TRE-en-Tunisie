import pandas as pd
import streamlit as st
import plotly.express as px
import datetime

with open("style.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True) 

st.markdown('''
<p style="color: rgb(168, 168, 168);">📊 COMPARATIF ></p>
''', unsafe_allow_html=True)


st.markdown('''
  <p class='title' style="font-weight: 700; font-size: 3rem; line-height: 100%;">Comparaison historique entre<br> TMM et TRE 🇹🇳</p>  
            
            ''', unsafe_allow_html=True)

st.markdown('''
 <a href="https://www.bct.gov.tn/bct/siteprod/index.jsp">Source: BCT de Tunis</a>
''', unsafe_allow_html=True)

st.divider()

df_TMM = pd.read_excel('BCT TMM.xlsx')
df_TRE = pd.read_excel('BCT TRE.xlsx')

df_TMM.rename(columns={'Date/Indicateurs':'Date'}, inplace=True)
df_TRE.rename(columns={'Date/Indicateurs':'Date'}, inplace=True)


df_TMM['Indicateurs'] = 'TMM'
df_TRE['Indicateurs'] = 'TRE'

df_TMM = df_TMM.reindex(columns=['Date', 'Indicateurs', 'Taux (%)'])
df_TRE = df_TRE.reindex(columns=['Date', 'Indicateurs', 'Taux (%)'])

st.subheader('🔎 DATA')

df_TAUX = pd.concat([df_TMM, df_TRE], axis=0)

#Double-slider
min_year = df_TAUX['Date'].dt.year.min()
max_year = df_TAUX['Date'].dt.year.max()

year_range = st.slider(
    "Sélectionnez la plage d'années :",
    min_year,
    max_year,
    (min_year, max_year)
)

with st.container():
    col1, col2 = st.columns([1,3])
    
    with col1:
        df_TAUX_filtered = df_TAUX[(df_TAUX['Date'].dt.year >= year_range[0]) & (df_TAUX['Date'].dt.year <= year_range[1])]
        df_TAUX_filtered['Date'] = df_TAUX_filtered['Date'].dt.strftime('%d-%m-%Y')
        st.dataframe(df_TAUX_filtered, hide_index=True, use_container_width=True, height=485)

    with col2:
            with st.container(border=True):
                result = year_range[1] - year_range[0]
                if result != 0:
                    fig = px.line(df_TAUX_filtered, x='Date', y='Taux (%)', title='Variation historique du TMM et TRE par année et par mois', line_shape='spline', color='Indicateurs', color_discrete_map= {'TMM':'#0068C9', 'TRE':'red'})
                    st.plotly_chart(fig, use_container_width=True) 
                else:
                    fig = px.line(df_TAUX_filtered, x='Date', y='Taux (%)', title='Variation historique du TMM et TRE par année et par mois', line_shape='spline', color='Indicateurs', color_discrete_map= {'TMM':'#0068C9', 'TRE':'red'})
                    
                    for indicator in df_TAUX_filtered['Indicateurs'].unique():
                        fig.update_traces(
                        selector=dict(name=indicator),
                        mode='lines+text',
                        text=df_TAUX_filtered[df_TAUX_filtered['Indicateurs'] == indicator]['Taux (%)'],
                        textposition='top center'
                    )                   
                    st.plotly_chart(fig, use_container_width=True) 

# Coder
st.sidebar.markdown('''
        <div class="coder">
            <p><br>✌️ Elaboré par: <span style="font-weight: 700">Mohamed Agrebi</span></p>
            <a href="https://www.linkedin.com/in/mohamed-agrebi-053799174/">LinkedIn</a>
        </div>
            
            ''', unsafe_allow_html=True)
