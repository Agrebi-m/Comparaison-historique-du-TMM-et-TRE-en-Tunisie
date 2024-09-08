import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
import base64
from babel.dates import format_date


with open("style.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True) 

# Sidebar
st.sidebar.subheader('FILTRES')

st.markdown('''
<p style="color: rgb(168, 168, 168);">📈 DASHBOARD ></p>
''', unsafe_allow_html=True)


st.markdown('''
  <p class='title' style="font-weight: 700; font-size: 3rem; line-height: 100%;">Evolution du Taux du Marché Monétaire <br>depuis 1987 🇹🇳</p>  
            
            ''', unsafe_allow_html=True)

st.markdown('''
 <a href="https://www.bct.gov.tn/bct/siteprod/index.jsp">Source: BCT de Tunis</a>
''', unsafe_allow_html=True)

st.divider()
st.subheader('⚡️METRICS')

df = pd.read_excel('BCT TMM.xlsx', sheet_name='Feuil1')
df.rename(columns={'Date/Indicateurs':'Date'}, inplace=True)

def df_style(value):
    if value == principal_max_rate:
        return 'background-color: #0068C9; color:white'
    elif value == principal_min_rate:
        return 'background-color: #EBF4F6;'
    else:
        return ''

# Filters options 
Options = st.sidebar.selectbox('Année', df['Date'].dt.year.unique(), placeholder='Choisir une date ...', index=None)

# KPI
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
now = datetime.datetime.now()
current_month = now.month
current_year = now.year

# Actual rate
actual_month_rate = df.loc[(df['Date'].dt.month == current_month) & (df['Date'].dt.year == current_year),'Taux (%)'].iloc[0]
previous_month_rate = df.loc[(df['Date'].dt.month == current_month - 1) & (df['Date'].dt.year == current_year),'Taux (%)'].iloc[0]
actual_rate_growth = ((actual_month_rate - previous_month_rate) / previous_month_rate)* 100

# Average rate
if Options != None:
    df_avg_rate = df[df['Date'].dt.year == Options]
    avg_rate = df_avg_rate['Taux (%)'].mean().round(2)
else:
    avg_rate = df['Taux (%)'].mean().round(2)

#Min rate
if Options != None:
    df_min_rate = df[df['Date'].dt.year == Options]
    min_rate = df_min_rate['Taux (%)'].min().round(2)
else:
    min_rate = df['Taux (%)'].min().round(2)

#Max rate
if Options != None:
    df_max_rate = df[df['Date'].dt.year == Options]
    max_rate = df_max_rate['Taux (%)'].max().round(2)
else:
    max_rate = df['Taux (%)'].max().round(2)
    
with st.container(border=True):
    metric1, metric2, metric3, metric4 = st.columns(4) 
    metric1.metric('Taux du mois actuel', actual_month_rate, delta= actual_rate_growth.round(2))
    metric2.metric('Taux moyen de la période*', avg_rate, delta='≈', delta_color='off')
    metric3.metric('Taux minimal de la période*', min_rate, delta='▾', delta_color='off')
    metric4.metric('Taux maximal de la période*', max_rate, delta='▴', delta_color='off')

if Options == None:
    st.markdown(f'<p style="font-size: .8em; color: gray;">*Période: 1987 à {now.year}</p>',unsafe_allow_html=True)
else:
    st.markdown(f'<p style="font-size: .8em; color: gray;">*Période: {Options}</p>',unsafe_allow_html=True)

df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')

with st.container():
    col1, col2 = st.columns([1,4])
    if Options != None :
        df_filtred = df[df['Date'].str.contains(str(Options))]
        mean_value = df_filtred['Taux (%)'].mean().round(2)
        principal_max_rate = df_filtred['Taux (%)'].max()
        principal_min_rate = df_filtred['Taux (%)'].min()

        with col1:
            st.dataframe(df_filtred.style.format({'Taux (%)':'{:.2f}'}).map(df_style, subset=['Taux (%)']), hide_index=True, use_container_width=True, height=480)
        
        with col2:
            with st.container(border=True):
                fig = px.line(df_filtred, x='Date', y='Taux (%)', title='Variation du TMM par année et par mois', line_shape='spline')
                fig.add_hline(y=mean_value, line_dash='dash', line_color='#7FA1C3', annotation_text=f'Ligne de Moyenne : {mean_value}', annotation_position='bottom left')
                fig.update_traces(mode='lines+text', text=df_filtred['Taux (%)'], textposition='top center')
                st.plotly_chart(fig, use_container_width=True)
    else:
        mean_value = df['Taux (%)'].mean().round(2)
        principal_max_rate = df['Taux (%)'].max()
        principal_min_rate = df['Taux (%)'].min()
        
        with col1:
            st.dataframe(df.style.format({'Taux (%)':'{:.2f}'}).map(df_style, subset=['Taux (%)']), hide_index=True, use_container_width=True, height=480)
        
        with col2:
            with st.container(border=True):
                fig = px.line(df, x='Date', y='Taux (%)', title='Variation du TMM par année et par mois', line_shape='spline')
                fig.add_hline(y=mean_value, line_dash='dash', line_color='#7FA1C3', annotation_text=f'Ligne de Moyenne : {mean_value}', annotation_position='bottom left')
                st.plotly_chart(fig, use_container_width=True)
                

# Analysis

st.subheader('📑 ANALYSE')

month_in_french = format_date(now, "MMMM", locale='fr_FR')

if actual_rate_growth >= 0 :
    st.markdown(f''' 
<p>Le taux du marché monétaire TMM du mois de {month_in_french} {now.year} s'élève à <span style="font-family: Source Code Pro; font-size: .8em; color: rgb(9, 171, 59); background: rgb(248, 249, 251);padding: .2em .4em; border-radius: .25rem">{actual_month_rate}%</span>, avec une évolution de <span style="font-family: Source Code Pro; font-size: .8em; color: rgb(9, 171, 59); background: rgb(248, 249, 251);padding: .2em .4em; border-radius: .25rem">▴{actual_rate_growth.round(2)}%</span> par rapport au mois précédent.</p>
''', unsafe_allow_html=True)
else:
    st.markdown(f''' 
<p>Le taux du marché monétaire TMM du mois de {now.strftime('%B').encode('latin1').decode('utf-8')} {now.year} s'élève à <span style="font-family: Source Code Pro; font-size: .8em; color: rgb(9, 171, 59); background: rgb(248, 249, 251);padding: .2em .4em; border-radius: .25rem">{actual_month_rate}%</span>, avec une évolution de <span style="font-family: Source Code Pro; font-size: .8em; color: red; background: rgb(248, 249, 251);padding: .2em .4em; border-radius: .25rem">▾{actual_rate_growth.round(2)}%</span> par rapport au mois précédent.</p>
''', unsafe_allow_html=True)

if Options == None:
    st.markdown(f'''
<p>Le taux moyen de la période s'étalant de 1987 à {now.year} s'élève à <span style="font-family: Source Code Pro; font-size: .8em; color: rgb(9, 171, 59); background: rgb(248, 249, 251);padding: .2em .4em; border-radius: .25rem">{avg_rate}%</span>.
<br>Durant la même période, le taux minimal enregistré est de <span style="font-family: Source Code Pro; font-size: .8em; color: rgb(9, 171, 59); background: rgb(248, 249, 251);padding: .2em .4em; border-radius: .25rem">{min_rate}%</span>. Le taux maximal s'élève à <span style="font-family: Source Code Pro; font-size: .8em; color: rgb(9, 171, 59); background: rgb(248, 249, 251);padding: .2em .4em; border-radius: .25rem">{max_rate}%</span>
</p>
''', unsafe_allow_html=True)
else:
    st.markdown(f'''
<p>Le taux moyen de l'année {Options} s'élève à <span style="font-family: Source Code Pro; font-size: .8em; color: rgb(9, 171, 59); background: rgb(248, 249, 251);padding: .2em .4em; border-radius: .25rem">{avg_rate}%</span>.
<br>Durant la même période, le taux minimal enregistré est de <span style="font-family: Source Code Pro; font-size: .8em; color: rgb(9, 171, 59); background: rgb(248, 249, 251);padding: .2em .4em; border-radius: .25rem">{min_rate}%</span>. Le taux maximal s'élève à <span style="font-family: Source Code Pro; font-size: .8em; color: rgb(9, 171, 59); background: rgb(248, 249, 251);padding: .2em .4em; border-radius: .25rem">{max_rate}%</span>
</p>
''', unsafe_allow_html=True)


# Coder
st.sidebar.divider()
st.sidebar.markdown('''
        <div class="coder">
            <p>✌️ Elaboré par: <span style="font-weight: 700">Mohamed Agrebi</span></p>
            <a href="https://www.linkedin.com/in/mohamed-agrebi-053799174/">LinkedIn</a>
        </div>
            
            ''', unsafe_allow_html=True)


