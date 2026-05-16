import streamlit as st
import pandas as pd
from pathlib import Path

# Configuração do caminho do csv pensando no deploy (substitui o os.path)
DATA_PATH = Path(__file__).parent.parent / "data" / "processed" / "top_100_verbs.csv"

# Paleta de cores
COLOR_PRIMARY = "#1d1160"
COLOR_SECONDARY = "#E6E6FA"
COLOR_CORRECT = "#4CAF50"
COLOR_WRONG = "#F44336"

# Fluxo principal
def main():
    # 1.1 Configuração e carregamento dos dados
    setup_page()
    df_verbs = load_data()

    # 1.2 Se o csv não carregar
    if df_verbs is None:
        st.error("**Ops! We couldn't load the verbs.** Please try again later.")
        st.stop()

    # 2. Sidebar para selecionar modo de estudo
    selected_set, sets = render_sidebar(df_verbs)
    
    # 3. Estado da sessão do streamlit
    init_state(selected_set, df_verbs, sets)

    # 4. Configurações CSS e renderização
    apply_custom_theme()
    render_header()
    past_simple_color, past_participle_color = get_feedback_colors()
    update_input_borders(past_simple_color, past_participle_color)

    # 5.1 Se finalizou o set de estudo, mostrar "congrats" e parar a execução
    if st.session_state.remaining_verbs.empty and not st.session_state.show_answer:
        st.success(f"⭐ **Congrats!** You've completed **{st.session_state.current_mode}**!")
        st.stop()

    # 5.2 Caso existam verbos no set, recupera o verbo atual e continua o loop do quiz
    verb = st.session_state.current_verb
    render_quiz(verb)
    render_feedback(verb)

# Funções auxiliares
def setup_page():
    """Define as configurações básicas do layout da página."""
    st.set_page_config(
        page_title="Tense Memo",
        page_icon="📓", # fazer em um logo?
        layout="centered"
    )

@st.cache_data
def load_data():
    """Carrega o arquivo CSV de verbos e armazena em cache."""
    try: return pd.read_csv(DATA_PATH)
    except: return None
# Para próxima versão penso em fazer persistência de dados com Firebase

def apply_custom_theme():
    """Aplica CSS e customiza a exibição dos verbos e do score board."""
    st.markdown(f"""
    <style>
        .verb-display {{
            font-size: 3.5rem; font-weight: 800; text-align: center;
            color: #ffffff; margin-bottom: 2rem; padding: 1.5rem;
            background-color: #000000; border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .score-board {{
            text-align: right; font-size: 1.2rem; font-weight: bold;
            color: {COLOR_PRIMARY}; margin-bottom: 2rem;
        }}
        .score-text {{ display: inline-block; }}
        .score-text.pop {{ animation: pop 0.4s ease-out; }}
        @keyframes pop {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.15); color: {COLOR_CORRECT}; }}
            100% {{ transform: scale(1); }}
        }}
        .score-up {{
            color: {COLOR_CORRECT}; position: absolute; margin-left: 10px;
            animation: floatUp 1.2s ease-out forwards; pointer-events: none;
        }}
        @keyframes floatUp {{
            0% {{ opacity: 0; transform: translateY(0); }}
            20% {{ opacity: 1; transform: translateY(-5px); }}
            100% {{ opacity: 0; transform: translateY(-20px); }}
        }}
        div[data-testid="stTextInput"] label, 
        div[data-testid="stTextInput"] label p {{ font-size: 1rem !important; font-weight: 600 !important; }}
        div[data-testid="stTextInput"] div[data-baseweb="input"] input {{ font-size: 1.15rem !important; padding: 0.6rem !important; }}
    </style>
    """, unsafe_allow_html=True)

def update_input_borders(past_simple_color, past_participle_color):
    """Altera as cores das bordas dos inputs de acordo com o feedback."""
    st.markdown(f"""
    <style>
        div[data-testid="stTextInput"]:has(input[aria-label="Past Simple"]) div[data-baseweb="input"],
        div[data-testid="stTextInput"]:has(input[aria-label="Past Simple"]) div[data-baseweb="input"]:focus-within {{
            border: 2px solid {past_simple_color} !important;
            box-shadow: none !important;
        }}
        div[data-testid="stTextInput"]:has(input[aria-label="Past Participle"]) div[data-baseweb="input"],
        div[data-testid="stTextInput"]:has(input[aria-label="Past Participle"]) div[data-baseweb="input"]:focus-within {{
            border: 2px solid {past_participle_color} !important;
            box-shadow: none !important;
        }}
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Renderiza o título, descrição e o scoreboard."""
    st.title("📓 Tense Memo")
    # Descrição do app
    st.markdown("""
    Build your fluency, one verb at a time.
    """, unsafe_allow_html=True)
    # Lógica de animação do score board
    just_scored = st.session_state.get('show_answer') and st.session_state.get('past_simple_correct') and st.session_state.get('past_participle_correct')
    pop_class = "pop" if just_scored else ""
    plus_one = "<span class='score-up'>+1</span>" if just_scored else ""
    
    st.markdown(f"""
    <div class='score-board'>
        <span class='score-text {pop_class}'>Score: {st.session_state.score} / {len(st.session_state.current_df)}</span>{plus_one}
    </div>
    """, unsafe_allow_html=True)

def get_feedback_colors():
    """Retorna as cores de acordo com o acerto/erro."""
    past_simple_color = COLOR_PRIMARY
    if st.session_state.get('past_simple_correct', False): past_simple_color = COLOR_CORRECT
    elif st.session_state.get('past_simple_wrong', False): past_simple_color = COLOR_WRONG

    past_participle_color = COLOR_PRIMARY
    if st.session_state.get('past_participle_correct', False): past_participle_color = COLOR_CORRECT
    elif st.session_state.get('past_participle_wrong', False): past_participle_color = COLOR_WRONG
    return past_simple_color, past_participle_color

def init_state(selected_set, df_verbs, sets):
    """Inicializa ou reseta as variáveis do streamlit ao trocar de set."""
    if 'current_mode' not in st.session_state or st.session_state.current_mode != selected_set:
        start_idx, end_idx = sets[selected_set]
        st.session_state.update({
            'current_mode': selected_set,
            'current_df': df_verbs.iloc[start_idx:end_idx],
            'remaining_verbs': df_verbs.iloc[start_idx:end_idx].copy(),
            'current_verb': df_verbs.iloc[start_idx:end_idx].sample(1).iloc[0],
            'score': 0, 'total_attempts': 0, 'show_answer': False, 'form_key': 0,
            'past_simple_correct': False, 'past_participle_correct': False, 'past_simple_wrong': False, 'past_participle_wrong': False
        })

def next_verb():
    """Sorteia o próximo verbo e reseta os estados da interface"""
    if not st.session_state.remaining_verbs.empty:
        st.session_state.current_verb = st.session_state.remaining_verbs.sample(1).iloc[0]
    st.session_state.update({
        'show_answer': False, 'form_key': st.session_state.form_key + 1,
        'past_simple_correct': False, 'past_participle_correct': False, 'past_simple_wrong': False, 'past_participle_wrong': False
    })

def render_sidebar(df_verbs):
    """Renderiza a barra lateral com o seletor de modos e a legenda explicativa."""
    sets = {
        # "Test to be": (0, 3), 
        "Set 1": (0, 23), 
        "Set 2": (23, 43), 
        "Set 3": (43, 63), 
        "Set 4": (63, 83), 
        "Set 5": (83, len(df_verbs)),
        "Hard Mode": (0, len(df_verbs))
    }
    
    st.sidebar.title("⚙️ Options")
    selected_set = st.sidebar.selectbox("Choose your study mode:", list(sets.keys()))
    st.sidebar.markdown(f"<div style='background-color: {COLOR_SECONDARY}; padding: 10px; border-radius: 8px; color: {COLOR_PRIMARY}; text-align: center; margin-bottom: 15px;'><b>Currently studying:</b> {selected_set}</div>", unsafe_allow_html=True)
    # Legenda explicando cada set
    st.sidebar.markdown(f"""
    <div style="padding: 15px; border-radius: 10px; color: #333333; background-color: #f1f3f6; font-size: 0.95rem; border-left: 5px solid {COLOR_PRIMARY};">
    <b>About the Sets:</b><br><br>
    • <b>Set 1</b>: Verb <i>to be</i> + Top 1-20 most used verbs.<br>
    • <b>Sets 2 to 5</b>: Groups of 20 verbs ordered by frequency.<br>
    • <b>Hard Mode</b>: Practice all 100 verbs at once!
    </div>
    """, unsafe_allow_html=True)
    return selected_set, sets

def render_quiz(verb):
    """Renderiza o verbo principal aplicando lógica do "be" no quiz/formulário."""
    present_verb = verb['present_3rd'] if pd.isna(verb['present']) else verb['present']
    st.markdown(f"<div class='verb-display'>{present_verb}</div>", unsafe_allow_html=True)

    # Formulário de resposta
    with st.form(key=f'f_{st.session_state.form_key}'):
        col1, col2 = st.columns(2)
        # Lógica para travar o input se já acertou
        past_simple_disabled = st.session_state.show_answer or st.session_state.past_simple_correct
        past_participle_disabled = st.session_state.show_answer or st.session_state.past_participle_correct
        
        # Preenche com a resposta certa se já acertou, senão deixa vazio
        past_simple_value = str(verb['past_simple']) if st.session_state.past_simple_correct else ""
        past_participle_value = str(verb['past_participle']) if st.session_state.past_participle_correct else ""

        past_simple_input = col1.text_input("Past Simple", value=past_simple_value, disabled=past_simple_disabled, autocomplete="off")
        past_participle_input = col2.text_input("Past Participle", value=past_participle_value, disabled=past_participle_disabled, autocomplete="off")
        
        if not st.session_state.show_answer:
            if st.form_submit_button("Check Answer", use_container_width=True):
                if past_simple_input and past_participle_input:
                    is_past_simple_correct = past_simple_input.strip().lower() == str(verb['past_simple']).strip().lower()
                    is_past_participle_correct = past_participle_input.strip().lower() == str(verb['past_participle']).strip().lower()
                    st.session_state.update({'past_simple_correct': is_past_simple_correct, 'past_simple_wrong': not is_past_simple_correct, 'past_participle_correct': is_past_participle_correct, 'past_participle_wrong': not is_past_participle_correct, 'show_answer': True})
                    if is_past_simple_correct and is_past_participle_correct:
                        st.session_state.score += 1
                        st.session_state.remaining_verbs = st.session_state.remaining_verbs.drop(verb.name)
                    st.rerun()
                else:
                    st.warning("Please fill both fields!")
        else:
            st.form_submit_button("Check Answer", disabled=True, use_container_width=True)

def render_feedback(verb):
    """Exibe mensagens de acerto/erro, o gabarito lavanda e os botões de navegação."""
    if st.session_state.show_answer:
        if st.session_state.past_simple_correct and st.session_state.past_participle_correct:
            if not st.session_state.remaining_verbs.empty:
                st.success("Correct ✅")
                if st.button("Next Verb", type="primary", use_container_width=True):
                    next_verb()
                    st.rerun()
            else:
                # Se era o último verbo, resetar para mostrar a tela final
                st.session_state.show_answer = False
                st.rerun()
        else:
            st.error(f"Incorrect ❌")
            past_simple_icon = "✅" if st.session_state.past_simple_correct else ""
            past_participle_icon = "✅" if st.session_state.past_participle_correct else ""
            st.markdown(f"<div style='background-color: {COLOR_SECONDARY}; padding: 15px; border-radius: 8px; color: {COLOR_PRIMARY}; font-size: 1rem; margin-bottom: 15px;'><b>Feedback:</b><br><br>• Past Simple: <b>{verb['past_simple']}</b> {past_simple_icon}<br>• Past Participle: <b>{verb['past_participle']}</b> {past_participle_icon}</div>", unsafe_allow_html=True)
            col_try_again, col_next_verb = st.columns(2)
            if col_try_again.button("Try Again", use_container_width=True): st.session_state.show_answer = False; st.rerun()
            if len(st.session_state.remaining_verbs) > 1 and col_next_verb.button("Next Verb", type="primary", use_container_width=True): next_verb(); st.rerun()

if __name__ == "__main__":
    main()