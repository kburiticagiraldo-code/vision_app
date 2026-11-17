import streamlit as st

CSS = """
<style>
h1, h2, h3 { color: #f5c542; }
.hero {
    text-align: center; padding: 2rem 1rem 1.5rem; margin-bottom: 1.5rem;
    border-radius: 18px; border: 1px solid #3a2f4a;
    background: linear-gradient(135deg, #2a1a2e, #14141f);
}
.hero-emoji { font-size: 3.2rem; }
.hero-titulo { font-size: 2.2rem; font-weight: 800; color: #f5c542; margin: .2rem 0; }
.hero-sub { color: #cfc9bb; font-size: 1.05rem; }
.paso {
    position: relative; height: 100%; padding: 1.2rem 1rem 1rem;
    border-radius: 14px; border: 1px solid #3a2f4a; background: #1a1a28;
}
.paso-num {
    position: absolute; top: -12px; left: 12px; width: 26px; height: 26px;
    border-radius: 50%; background: #f5c542; color: #14141f;
    font-weight: 800; text-align: center; line-height: 26px;
}
.paso-titulo { font-weight: 700; font-size: 1.1rem; margin-bottom: .4rem; color: #f5c542; }
.paso-texto { font-size: .92rem; color: #cfc9bb; }
</style>
"""


def aplicar_estilo():
    st.markdown(CSS, unsafe_allow_html=True)


def hero(titulo, subtitulo, emoji="🎬"):
    st.markdown(
        f'<div class="hero"><div class="hero-emoji">{emoji}</div>'
        f'<div class="hero-titulo">{titulo}</div>'
        f'<div class="hero-sub">{subtitulo}</div></div>',
        unsafe_allow_html=True,
    )
