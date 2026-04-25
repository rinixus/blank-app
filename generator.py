import time
import shutil
import os
import re
from database import add_movie
import streamlit as st

SAMPLE_VIDEO_SOURCE = "sample_video.mp4"
GENERATED_DIR = "generated_movies"

if not os.path.exists(GENERATED_DIR):
    os.makedirs(GENERATED_DIR)


def sanitize_filename(filename):
    """
    Sanitizes the filename to prevent directory traversal and special chars.
    """
    # Remove characters that aren't alphanumerics, underscores, hyphens or spaces
    s = re.sub(r'[^a-zA-Z0-9_\-\s]', '', filename)
    # Replace spaces with underscores
    s = s.replace(' ', '_')
    return s


def build_icaros_flowey_guide(hero_name="alma humana"):
    """
    Creates a lightweight narrative mod script where the angel narrator
    Ícaros guides the player in a final confrontation against Flowey.
    """
    return f"""MOD: ÍCAROS, O ANJO NARRADOR — ROTA DA ESPERANÇA

[Prólogo]
Uma luz dourada corta o silêncio. Ícaros desce em voo e fala com você, {hero_name}:
"Eu sou Ícaros. Não vim para lutar por você — vim para te lembrar de quem você é."

[Fase 1: Jardim Distorcido]
Flowey tenta confundir sua determinação com memórias quebradas.
Ícaros orienta:
1) Respire e observe os padrões das vinhas.
2) Defenda nos pulsos verdes, avance nos intervalos.
3) Use COMPAIXÃO quando ouvir ecos de medo.

[Fase 2: Ecos das Almas]
Flowey amplifica vozes de dúvida.
Ícaros sussurra:
- "A esperança é um ritmo. Mantenha o passo."
- "Quando a tela tremer, mova em diagonal para quebrar o cerco."
- "A cada acerto, lembre-se: você não está só."

[Fase 3: Coração do Caos]
No ápice do combate, Ícaros abre as asas e cria uma janela de luz.
Comando final: CANALIZAR LUZ.
Combine ataque preciso + ato de misericórdia para enfraquecer Flowey sem perder sua essência.

[Final]
Flowey cai em silêncio. Ícaros pousa ao seu lado:
"Vitória verdadeira não é destruir o inimigo, mas recusar se tornar igual a ele."

Recompensa do mod:
- Título: Guardião da Aurora
- Efeito visual: Halo de Ícaros
- Narrador desbloqueado para novas rotas
"""


def save_icaros_guide(user_email, title, hero_name="alma humana"):
    """Saves the Ícaros mod script to a text artifact and returns the path."""
    safe_title = sanitize_filename(title) or "mod_icaros"
    safe_user = sanitize_filename(user_email) or "player"
    guide_filename = f"{int(time.time())}_{safe_user}_{safe_title}_icaros_mod.txt"
    guide_path = os.path.join(GENERATED_DIR, guide_filename)

    with open(guide_path, "w", encoding="utf-8") as file:
        file.write(build_icaros_flowey_guide(hero_name=hero_name))

    return guide_path


def generate_movie(user_email, title, genre, style, year):
    """
    Simulates AI video generation.
    1. Shows a progress bar.
    2. Copies the sample video to a new path.
    3. Saves entry to DB.
    """

    # Simulation UI
    progress_text = "AI Showrunner is crafting your scene..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.03)  # Simulate work (3 seconds total)
        my_bar.progress(percent_complete + 1, text=progress_text)

    my_bar.empty()

    # "Generation" (Copying file)
    # Security fix: Sanitize title
    safe_title = sanitize_filename(title)
    filename = f"{int(time.time())}_{safe_title}.mp4"
    destination_path = os.path.join(GENERATED_DIR, filename)

    # Ensure source exists (downloaded in step 1)
    if os.path.exists(SAMPLE_VIDEO_SOURCE):
        shutil.copy(SAMPLE_VIDEO_SOURCE, destination_path)
    else:
        # Fallback if sample missing
        with open(destination_path, 'w', encoding='utf-8') as f:
            f.write("Mock Video Content")

    # Save to DB
    add_movie(user_email, title, genre, style, year, destination_path)

    return destination_path
