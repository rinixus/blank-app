from __future__ import annotations

from io import BytesIO
from pathlib import Path
import zipfile

import streamlit as st

st.set_page_config(page_title="Minecraft Addon: Illager Raid Trio", page_icon="🧟")

BASE_DIR = Path(__file__).parent
ADDON_DIR = BASE_DIR / "addon"


def build_zip(source_dir: Path) -> bytes:
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                bundle.write(path, path.relative_to(source_dir))
    return buffer.getvalue()


st.title("Addon pronto: 3 Illagers novos na Raid")
st.write(
    "Este pacote para **Minecraft Bedrock** adiciona três inimigos novos com comportamento e visual próprio:"
)

st.markdown(
    """
- 🤡 **Illager Palhaço**: rápido e caótico, entra em raids.
- 🦸 **Illager Super-Herói**: mais vida e dano alto, estilo mini-chefe.
- 🥷 **Illager Ninja**: muito veloz, focado em perseguição.

O download já vem com:
- Behavior Pack (comportamento, spawn rules e raid membership)
- Resource Pack (client entities, geometrias e nomes localizados)
"""
)

zip_bytes = build_zip(ADDON_DIR)

st.download_button(
    label="📦 Baixar addon Illager Raid Trio (.zip)",
    data=zip_bytes,
    file_name="illager_raid_trio_addon.zip",
    mime="application/zip",
)

st.subheader("Como instalar")
st.markdown(
    """
1. Baixe o ZIP no botão acima.
2. Extraia o conteúdo e copie as duas pastas para:
   - `behavior_packs/IllagerRaidTrio_BP`
   - `resource_packs/IllagerRaidTrio_RP`
3. Ative os dois packs no seu mundo Bedrock.
4. Entre em uma raid (ou use `/summon irt:illager_clown`, etc.).
"""
)

st.caption("Compatível com Minecraft Bedrock 1.20.30+")
