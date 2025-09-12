import re
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Portal de Apps", page_icon="🗂️", layout="wide")

# =========================
# Catálogo dos seus apps
# =========================
def guess_streamlit_url(owner: str, repo: str, branch: str, entry_path: str) -> str:
    """
    Gera a URL do app no Streamlit Cloud a partir do padrão de nomeação:
    https://{owner}-{repo}-{branch}-{entry_path_with_dashes}.streamlit.app
    """
    slug_path = re.sub(r"[^a-zA-Z0-9]", "-", entry_path).strip("-").lower()
    return f"https://{owner}-{repo}-{branch}-{slug_path}.streamlit.app"

APPS = [
    {
        "name": "Day Trade Analytics",
        "owner": "bomcabelo",
        "repo": "dsa-day-trade-analytics",
        "branch": "main",
        "entry_path": "dsa_app.py",
        "description": "Dashboard analítico para day trade (DSA).",
        # Se já souber a URL exata, pode sobrescrever em "app_url"
        "app_url": guess_streamlit_url("bomcabelo","dsa-day-trade-analytics","main","dsa_app.py"),
        "github_url": "https://dsa-day-trade-analytics-dsvnvnovhvepuj3u6yr5bu.streamlit.app/",
    },
    {
        "name": "Evento Streamlit",
        "owner": "bomcabelo",
        "repo": "evento-streamlit",
        "branch": "main",
        "entry_path": "aplicativo.py",
        "description": "Aplicativo para gerenciamento/divulgação de evento.",
        "app_url": guess_streamlit_url("bomcabelo","evento-streamlit","main","aplicativo.py"),
        "github_url": "https://evento-app-7gxfdv3xwusgrt4sjaeenn.streamlit.app/",
    },
    {
        "name": "Marketing LLM",
        "owner": "bomcabelo",
        "repo": "marketing-llm-streamlit",
        "branch": "main",
        "entry_path": "app.py",
        "description": "Gerador de conteúdo com LLM focado em SEO.",
        "app_url": guess_streamlit_url("bomcabelo","marketing-llm-streamlit","main","app.py"),
        "github_url": "https://marketing-llm-app-3h3nx3vpxf8qymo5tzhjbe.streamlit.app/",
    },
]

# =========================
# UI: título, busca e opções
# =========================
st.title("🗂️ Portal de Apps — bomcabelo")

col_l, col_r = st.columns([2, 1])
with col_l:
    query = st.text_input("Filtrar por nome/descrição:", placeholder="Digite um termo…").strip().lower()
with col_r:
    preview = st.toggle("Pré-visualizar apps dentro da página (iframe)", value=False,
                        help="Alguns apps podem bloquear iframe; se ficar em branco, use o botão 'Abrir app'.")

# Filtragem simples
def match(app: dict, q: str) -> bool:
    if not q:
        return True
    alvo = f"{app['name']} {app.get('description','')}".lower()
    return q in alvo

apps_filtrados = [a for a in APPS if match(a, query)]

# =========================
# Card de app
# =========================
def app_card(app: dict):
    with st.container(border=True):
        st.subheader(app["name"])
        st.caption(f"Repo: `{app['owner']}/{app['repo']}` — Branch: `{app['branch']}` — Entry: `{app['entry_path']}`")
        if app.get("description"):
            st.write(app["description"])

        b1, b2, b3 = st.columns([1, 1, 6])
        with b1:
            st.link_button("Abrir app ▶️", app["app_url"], use_container_width=True)
        with b2:
            st.link_button("GitHub 💻", app["github_url"], use_container_width=True)

        if preview:
            st.write("")  # espaçamento
            components.iframe(app["app_url"], height=700)

# =========================
# Grid responsivo
# =========================
if not apps_filtrados:
    st.info("Nenhum app encontrado para esse filtro.")
else:
    # layout em 2 colunas (ajuste para 3 se tiver muitos apps)
    cols = st.columns(2)
    for i, app in enumerate(apps_filtrados):
        with cols[i % 2]:
            app_card(app)

st.divider()
st.markdown(
    "💡 Para **adicionar mais apps**, basta inserir um novo item em `APPS` com "
    "`name`, `owner`, `repo`, `branch`, `entry_path`, `description` e (opcional) `app_url`/`github_url`."
)
st.caption(
    "Se a URL gerada não abrir, copie o endereço do app no Streamlit Cloud e substitua o campo `app_url`."
)
