#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
import random
import streamlit as st
import time
import webbrowser


# In[ ]:

st.image('./LOGO_NEW.png')


# Read df_sound csv
df_sound = pd.read_csv('./df_sound.csv')


# Créer un dataFrame user
df_user = pd.DataFrame(columns = df_sound.columns)


# In[14]:


# Creat users dataframe randomly
df_user = pd.concat([df_user, df_sound.sample(n = 10000, random_state = 1)])


# In[15]:


# reindex df_user
df_user.reset_index(inplace = True)


# In[44]:


# Read CSV name


df_name = pd.read_csv('./df_name.csv')


# In[45]:


df_name['orientation'] = df_name['Sexe'].apply(lambda x: 'M' if x == 'F' else 'F')


# In[46]:


# merge df_user and df_name
df_users = pd.merge(df_name, df_user, left_index = True, right_index = True)


# Fonction pour supprimer accents et mettre la chaîne de caractères en minuscule
import unicodedata

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower()



# Input username and sex
st.subheader("Dis nous d'abord qui tu es!")
x = st.text_input('', key = 1, placeholder = 'Prénom')
s = st.text_input('', key = 1, placeholder = 'Sexe', help = 'M ou F')
Orientation = st.text_input('', key = 1, placeholder = 'Orientation sexuelle', help = 'M ou F')


# Display pre selection for choose index

m_1 = st.text_input('', key = 1, placeholder = 'Selectionne une musique')

df_pre_selection = df_sound.loc[df_sound['track_name'].apply(lambda x: remove_accents(x)).str.contains(m_1)]

    

if len(df_pre_selection) == 0:
    st.warning("Votre musique n'est pas dans notre repertoire Veuillez selectionner une autre music")
    m_1 = st.text_input('', key = 2, placeholder = 'Selectionne une musique')
    df_pre_selection = df_sound.loc[df_sound['track_name'].apply(lambda x: remove_accents(x)).str.contains(m_1)]
    df_pre_selection = df_pre_selection.reset_index(drop = True)
    df_pre_selection = df_pre_selection.drop(columns = ['Unnamed: 0'])
        
else:
    if len(df_pre_selection) == 1:
        a_1 = df_pre_selection.iloc[0]
    else:
        df_pre_selection = df_pre_selection.reset_index(drop = True)
        df_pre_selection = df_pre_selection.drop(columns = ['Unnamed: 0'])
        st.dataframe(df_pre_selection)
        m_1 = st.number_input("selectionne l'index", value = 0, step = 1, key = 1)
        a_1 = df_pre_selection.iloc[m_1]
            
# Concat new user in df_users
dico = {'Prénom': [x], 'Sexe': [s], 'orientation': [Orientation], 'genre': a_1[0], 'artist_name': a_1[1], 'track_name': a_1[2], 'popularity': a_1[3],
    'acousticness': a_1[4], 'danceability': a_1[5], 'energy': a_1[6], 'instrumentalness': a_1[7],
    'liveness': a_1[8], 'loudness': a_1[9], 'tempo': a_1[10], 'valence': a_1[11], 'Alternative': a_1[12], 'Blues': a_1[13],
    'Country': a_1[14], 'Dance': a_1[15], 'Electronic': a_1[16], 'Folk': a_1[17], 'Hip-Hop': a_1[18],
    'Jazz': a_1[19], 'Pop': a_1[20], 'R&B': a_1[21], 'Rap': a_1[22], 'Reggae': a_1[23], 'Reggaeton': a_1[24],
    'Rock': a_1[25], 'Soul': a_1[26], 'World': a_1[27]}
df = pd.DataFrame(data = dico)
df_users = pd.concat([df_users, df])

df_users.reset_index(drop = True, inplace = True)

st.subheader('Félicitations, voici ton identifiant')
df_users.tail(1).index.values.astype(str)[0]


def match_music():

    # algorithm KNN
    X = df_users[['popularity', 'acousticness',
       'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
       'tempo', 'valence', 'Alternative', 'Blues', 'Country', 'Dance',
       'Electronic', 'Folk', 'Hip-Hop', 'Jazz', 'Pop', 'R&B', 'Rap', 'Reggae',
       'Reggaeton', 'Rock', 'Soul', 'World']]

    # Algorithm
    # input ton identifiant
    x = st.number_input(label = 'rentre ton identifiant :', value = 0, step = 1, key = 1)
    i = 1
    

    if df_users.iloc[x][2] == 'F':
        distanceKNN = NearestNeighbors(n_neighbors=i).fit(X)
        df = distanceKNN.kneighbors(df_users.loc[(df_users.index == x), X.columns])
        df_final = df_users.iloc[df[1][0]].loc[df_users.iloc[df[1][0]]['Sexe'] == "F"]
        while len(df_final.index) != 1:
            distanceKNN = NearestNeighbors(n_neighbors=i).fit(X)
            df = distanceKNN.kneighbors(df_users.loc[(df_users.index == x), X.columns])
            df_final = df_users.iloc[df[1][0]].loc[df_users.iloc[df[1][0]]['Sexe'] == "F"]
            i += 1
         
        st.subheader('Tu as un MATCH')   
        return st.dataframe(df_final[['Prénom', 'Sexe', 'genre', 'artist_name', 'track_name']])
    
    else:
        distanceKNN = NearestNeighbors(n_neighbors=i).fit(X)
        df = distanceKNN.kneighbors(df_users.loc[(df_users.index == x), X.columns])
        df_final = df_users.iloc[df[1][0]].loc[df_users.iloc[df[1][0]]['Sexe'] == "M"]
        while len(df_final.index) != 1:
            distanceKNN = NearestNeighbors(n_neighbors=i).fit(X)
            df = distanceKNN.kneighbors(df_users.loc[(df_users.index == x), X.columns])
            df_final = df_users.iloc[df[1][0]].loc[df_users.iloc[df[1][0]]['Sexe'] == "M"]
            i += 1
        
        st.subheader('Tu as un MATCH')
        
        return st.dataframe(df_final[['Prénom', 'Sexe', 'genre', 'artist_name', 'track_name']])
    
# Time spinner


match_music()

if st.button('Youtube'):
    webbrowser.open_new_tab('https://www.youtube.com/')

video_file = open('./Intro_appolon.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)

# In[ ]:




