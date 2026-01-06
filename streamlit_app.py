import streamlit as st
import pandas as pd
import auth
import database
import generator
import os

# --- Configuration ---
st.set_page_config(
    page_title="MIXMOVIE.AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Translations ---
LANG = {
    'en': {
        'title': "MIXMOVIE.AI",
        'subtitle': "The AI Netflix for Showrunners",
        'nav_home': "🏠 Home / Gallery",
        'nav_studio': "✨ Studio (Create)",
        'nav_library': "📂 My Library",
        'login_msg': "Please login to access the studio.",
        'welcome': "Welcome, ",
        'logout': "Logout",
        'recent_hits': "Trending Now",
        'create_title': "Create Your Masterpiece",
        'input_title': "Movie Title",
        'input_genre': "Genre",
        'input_style': "Visual Style",
        'input_year': "Setting Year",
        'btn_generate': "Generate Movie",
        'my_movies': "My Productions",
        'public': "Public",
        'private': "Private",
        'download': "Download",
        'watch': "Watch",
        'no_movies': "No movies created yet. Go to the Studio!",
        'toggle_lang': "Language/Idioma"
    },
    'pt': {
        'title': "MIXMOVIE.AI",
        'subtitle': "A Netflix da IA para Showrunners",
        'nav_home': "🏠 Início / Galeria",
        'nav_studio': "✨ Estúdio (Criar)",
        'nav_library': "📂 Minha Biblioteca",
        'login_msg': "Por favor, faça login para acessar o estúdio.",
        'welcome': "Bem-vindo, ",
        'logout': "Sair",
        'recent_hits': "Tendências Agora",
        'create_title': "Crie Sua Obra-Prima",
        'input_title': "Título do Filme",
        'input_genre': "Gênero",
        'input_style': "Estilo Visual",
        'input_year': "Ano de Ambientação",
        'btn_generate': "Gerar Filme",
        'my_movies': "Minhas Produções",
        'public': "Público",
        'private': "Privado",
        'download': "Baixar",
        'watch': "Assistir",
        'no_movies': "Nenhum filme criado ainda. Vá ao Estúdio!",
        'toggle_lang': "Language/Idioma"
    }
}

# --- Session State for Language ---
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'en'

def toggle_language():
    if st.session_state['lang'] == 'en':
        st.session_state['lang'] = 'pt'
    else:
        st.session_state['lang'] = 'en'

text = LANG[st.session_state['lang']]

# --- Sidebar ---
st.sidebar.title("MIXMOVIE.AI 🎬")
if st.sidebar.button(text['toggle_lang']):
    toggle_language()
    st.rerun()

user = auth.login()

# Navigation
if user:
    st.sidebar.write(f"{text['welcome']} {user['name']}")
    page = st.sidebar.radio("Navigate", [text['nav_home'], text['nav_studio'], text['nav_library']])
    if st.sidebar.button(text['logout']):
        auth.logout()
else:
    page = text['nav_home'] # Non-logged users can see Home
    st.sidebar.warning(text['login_msg'])

# --- Pages ---

# 1. HOME / GALLERY
if page == text['nav_home']:
    st.title(text['title'])
    st.subheader(text['subtitle'])

    st.markdown("### " + text['recent_hits'])

    public_movies = database.get_public_movies()

    if not public_movies.empty:
        # Create a grid
        cols = st.columns(3)
        for index, row in public_movies.iterrows():
            with cols[index % 3]:
                st.video(row['file_path'])
                st.write(f"**{row['title']}** ({row['year']})")
                st.caption(f"{row['genre']} | {row['style']}")
                if user and st.button(f"{text['download']} {row['title']}", key=f"dl_home_{row['id']}"):
                    # Streamlit download button logic
                    with open(row['file_path'], "rb") as file:
                        st.download_button(
                            label="⬇️",
                            data=file,
                            file_name=os.path.basename(row['file_path']),
                            mime="video/mp4",
                            key=f"real_dl_home_{row['id']}"
                        )
    else:
        st.info("The gallery is empty. Be the first to publish a movie!")

# 2. STUDIO (Create)
elif page == text['nav_studio']:
    st.title(text['nav_studio'])
    st.subheader(text['create_title'])

    with st.form("create_movie_form"):
        title = st.text_input(text['input_title'])
        col1, col2, col3 = st.columns(3)
        with col1:
            genre = st.selectbox(text['input_genre'], ["Sci-Fi", "Horror", "Action", "Romance", "Documentary", "Anime"])
        with col2:
            style = st.selectbox(text['input_style'], ["Cinematic", "Cartoon", "Claymation", "Noir", "Cyberpunk"])
        with col3:
            year = st.text_input(text['input_year'], "2024")

        submitted = st.form_submit_button(text['btn_generate'])

        if submitted and title:
            # Ensure user exists in DB
            database.add_user(user['email'], user['name'])

            # Generate
            video_path = generator.generate_movie(user['email'], title, genre, style, year)

            st.success(f"Movie '{title}' generated successfully!")
            st.video(video_path)

# 3. MY LIBRARY
elif page == text['nav_library']:
    st.title(text['nav_library'])

    user_movies = database.get_user_movies(user['email'])

    if not user_movies.empty:
        for index, row in user_movies.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.video(row['file_path'])
                with c2:
                    st.subheader(row['title'])
                    st.write(f"**Genre:** {row['genre']} | **Style:** {row['style']} | **Year:** {row['year']}")

                    # Privacy Toggle
                    is_public = row['is_public'] == 1
                    status_label = text['public'] if is_public else text['private']
                    btn_label = f"Make {text['private']}" if is_public else f"Make {text['public']}"

                    st.write(f"Status: **{status_label}**")

                    if st.button(btn_label, key=f"priv_{row['id']}"):
                        database.toggle_visibility(row['id'], is_public)
                        st.rerun()

                    # Download
                    with open(row['file_path'], "rb") as file:
                        st.download_button(
                            label=text['download'],
                            data=file,
                            file_name=os.path.basename(row['file_path']),
                            mime="video/mp4",
                            key=f"dl_lib_{row['id']}"
                        )
                st.divider()
    else:
        st.info(text['no_movies'])
