import re
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Portal de Apps", page_icon="🗂️", layout="wide")

# -------------------------
# Utils
# -------------------------
def normalize_streamlit_url(url: str | None) -> str:
    if not url:
        return ""
    url = url.strip()
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    # validação simples para domínios *.streamlit.app
    pat = r"^https?://[a-z0-9-]+\.streamlit\.app/?$"
    return url if re.match(pat, url) else url  # mantém mesmo se não bater, só não bloqueia

# -------------------------
# Catálogo (edite app_url com a URL real do deploy)
# -------------------------
APPS = [
    {
        "name": "Day Trade Analytics",
        "owner": "bomcabelo",
        "repo": "dsa-day-trade-analytics",
        "branch": "main",
        "entry_path": "dsa_app.py",
        "description": "Dashboard analítico para day trade (DSA).",
        "app_url": "",  # cole aqui a URL pública exata quando tiver
        "github_url": "https://github.com/bomcabelo/dsa-day-trade-analytics",
    },
    {
        "name": "Evento Streamlit",
        "owner": "bomcabelo",
        "repo": "evento-streamlit",
        "branch": "main",
        "entry_path": "aplicativo.py",
        "description": "Aplicativo para gerenciamento/divulgação de evento.",
        "app_url": "",  # cole aqui a URL pública exata quando tiver
        "github_url": "https://github.com/bomcabelo/evento-streamlit",
    },
    {
        "name": "Marketing LLM",
        "owner": "bomcabelo",
        "repo": "marketing-llm-streamlit",
        "branch": "main",
        "entry_path": "app.py",
        "description": "Gerador de conteúdo com LLM focado em SEO.",
        # Exemplo (substitua pela sua URL real):
        # "app_url": "https://marketing-llm-app-3h3nx3vpxf8qymo5tzhjbe.streamlit.app",
        "app_url": "",
        "github_url": "https://github.com/bomcabelo/marketing-llm-streamlit",
    },
]

# -------------------------
# UI
# -------------------------
st.title("🗂️ Portal de Apps — bomcabelo")

col_l, col_r = st.columns([2, 1])
with col_l:
    query = st.text_input("Filtrar por nome/descrição:", placeholder="Digite um termo…").strip().lower()
with col_r:
    preview = st.toggle("Pré-visualizar apps dentro da página (iframe)", value=False,
                        help="Alguns apps podem bloquear iframe; se ficar em branco, use o botão 'Abrir app'.")

def match(app: dict, q: str) -> bool:
    if not q:
        return True
    alvo = f"{app['name']} {app.get('description','')}".lower()
    return q in alvo

apps_filtrados = [a for a in APPS if match(a, query)]

# -------------------------
# Card de app
# -------------------------
def app_card(app: dict, idx: int):
    with st.container(border=True):
        st.subheader(app["name"])
        st.caption(f"Repo: `{app['owner']}/{app['repo']}` — Branch: `{app['branch']}` — Entry: `{app['entry_path']}`")
        if app.get("description"):
            st.write(app["description"])

        # URL (permitir preencher/editar no próprio portal)
        key_url = f"url_{idx}"
        current = normalize_streamlit_url(app.get("app_url", ""))
        url = st.text_input("URL pública do app (streamlit.app)", value=current, key=key_url,
                            placeholder="https://<subdominio>.streamlit.app")

        # ações
        b1, b2, b3 = st.columns([1, 1, 6])
        with b1:
            if url:
                st.link_button("Abrir app ▶️", url, use_container_width=True)
            else:
                st.button("Abrir app ▶️", disabled=True, use_container_width=True)
        with b2:
            st.link_button("GitHub 💻", app["github_url"], use_container_width=True)

        # preview (pode falhar se o app bloquear iframe)
        if preview and url:
            st.write("")
            try:
                components.iframe(url, height=700)
            except Exception:
                st.warning("Não foi possível incorporar via iframe. Use o botão 'Abrir app'.")

# -------------------------
# Grid
# -------------------------
if not apps_filtrados:
    st.info("Nenhum app encontrado para esse filtro.")
else:
    cols = st.columns(2)
    for i, app in enumerate(apps_filtrados):
        with cols[i % 2]:
            app_card(app, i)

st.divider()
st.markdown(
    "💡 Para **adicionar mais apps**, inclua um item em `APPS` com "
    "`name`, `owner`, `repo`, `branch`, `entry_path`, `description` e (opcional) `app_url`/`github_url`."
)
st.caption("Como a URL do Streamlit Cloud contém um sufixo aleatório, **cole a URL pública exata do deploy** no campo acima.")
