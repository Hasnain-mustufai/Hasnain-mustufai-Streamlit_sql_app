import streamlit as st
import pandas as pd
from pandas import read_sql

from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

engine = create_engine("mysql+pymysql://root:1258@localhost/all_olympic")

query = "SELECT * FROM athletes;"

df = pd.read_sql(query, engine)

df.sample(3)


# Titre
st.markdown("<h1 style='text-align: center;'>Dashbord Jeux Olympique</h1>", unsafe_allow_html=True)


# KPIs simples
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Athlètes", len(df))
col2.metric("Total Pays", df["NOC"].nunique())
col3.metric("Total Sports", df["Sport"].nunique())

# Trouver le sport le plus populaire
top_sport = df["Sport"].value_counts().idxmax()
top_sport_count = df["Sport"].value_counts().max()

col4.metric("Sport le plus populaire", f"{top_sport} ({top_sport_count})")

# Graphique simple : top 10 sports
top_sports = df["Sport"].value_counts().head(10)

st.subheader("Top 10 Sports les plus populaires")
st.bar_chart(top_sports)

st.sidebar.text("Athlet les plus populaires")

df_views =read_sql("SHOW FULL TABLES WHERE table_type = 'VIEW';",
engine)

st.markdown("<h1 style='text-align: center;'>Views</h1>", unsafe_allow_html=True)
st.dataframe(df_views)

df_age = pd.read_sql("SELECT * FROM age_moy_sport;", engine)

st.markdown("<h2 style='text-align:center;'>Âge moyen par sport</h2>", unsafe_allow_html=True)
st.dataframe(df_age)

st.sidebar.text("Athlet moyen par sport")
st.caption("Age moyen par sport")
st.bar_chart(df_age.set_index("Sport"))
st.divider()

df_medaille = read_sql("SELECT * FROM medailles_par_pays;", engine)

st.markdown("<h2 style='text-align:center;'>Médaille par pays(Top 5)</h2>", unsafe_allow_html=True)
st.dataframe(df_medaille)

st.sidebar.text("Athlet par pays(Top 5)")
st.caption("répartitions en pourcentages")

# st.write(df_medaille.columns)

# Création du pie chart
fig, ax = plt.subplots(figsize=(8, 8))

ax.pie(
    df_medaille["total_medals"],
    labels=df_medaille["NOC"],
    autopct="%1.1f%%",
    startangle=90,
    colors=plt.cm.Set3.colors
)

ax.set_title("Répartition des médailles par pays", fontsize=16)

st.pyplot(fig)

st.divider()
part=read_sql("SELECT * FROM participations_année;", engine)
st.markdown("<h2 style='text-align:center;'>Participations Annuel(Top 10)</h2>", unsafe_allow_html=True)
st.dataframe(part)

#poo = st.write(part.columns)
#print(poo)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot( data=part, x="Year", y="total_athletes", palette="viridis", ax=ax )
ax.set_title("Nombre de participants annuelle", fontsize=16)
ax.set_xlabel("Année")
ax.set_ylabel("Nombre de participations")
plt.xticks(rotation=45)
st.pyplot(fig)

st.divider()
rep =read_sql("SELECT * FROM repartition_sport;", engine)
st.markdown("<h2 style='text-align:center;'>Nombre de participants par Sport</h2>", unsafe_allow_html=True)
st.dataframe(rep)

# st.write(rep.columns)
rep= rep.sort_values("total", ascending=False)

fig, ax = plt.subplots(figsize=(15, 22))
sns.barplot( data=rep, y="Sport",
             x="total",
             palette="viridis", ax=ax )
ax.set_title("Répartition des sports (Top 10)", fontsize=18)
ax.set_xlabel("Total", fontweight="bold", fontsize=22)
ax.set_ylabel("Sport", fontweight="bold", fontsize=22)
plt.grid(axis='x', linestyle='--', alpha=0.4)
ax.tick_params(axis='y', labelsize=14, width=1)
ax.tick_params(axis='x', labelsize=14, width=1)

ax.set_xlim(0, rep["total"].max() * 1.25)


st.pyplot(fig)