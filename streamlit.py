import streamlit as st
import pandas as pd
from pymongo import MongoClient
import time
import altair as alt
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
client = MongoClient("mongodb://localhost:27017/")
db = client['base_villes']
collection = db['weatherData']
refresh_interval = 5
st.title('Tableau de Bord des Données Météorologiques')
count=st_autorefresh(interval=60000,key='datarefresh')
@st.cache_data(ttl=10)  # Mise en cache des données pendant 10 secondes
def get_data():
   donnees= list(collection.find())
   df=pd.json_normalize(donnees)
   return df

# Utilisation de la fonction mise en cache
df = get_data()
# df = pd.DataFrame(donnees)
df1=df
if len(df)>60:
    df1=df.head(60)

 
# df['time'] = pd.to_datetime(df['time'], format='%Y:%m:%d %H:%M:%S')
df["weather.temperature.temp"]=df["weather.temperature.temp"].astype(int)
st.dataframe(df.head(1))

fig, ax = plt.subplots()
ax.plot(df1['time'], df1['weather.temperature.temp'], marker='o', linestyle='-')
ax.set_title('Température en fonction du temps')
ax.set_xlabel('Temps')
ax.set_ylabel('Température (°C)')
# Afficher le graphique dans Streamlit
st.pyplot(fig)
# c=alt.Chart(df).encode(y='weather.temperature.temp',x='weather.temperature.temp')
# st.altair_chart(c)
# st.line_chart(df['humidité'])
# st.line_chart(df['vitesse_vent'])


