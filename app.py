import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# --- 1. CONFIGURAÇÃO DA PÁGINA (WIDE & MODERN) ---
st.set_page_config(
    page_title="HQ: Missão 10 de Julho",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎯"
)

# --- 2. CSS PERSONALIZADO (Professional Dark Theme) ---
st.markdown("""
    <style>
    /* Fundo Principal e Cores */
    .stApp { background-color: #0e1117; color: white; }
    
    /* Títulos */
    h1, h2, h3 { color: #f0f2f6 !important; font-family: 'Inter', sans-serif; }
    
    /* Cards de Métricas (Dashboard) */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; color: #ff4b4b !important; }
    [data-testid="stMetricLabel"] { font-size: 0.9rem !important; color: #8b949e !important; }
    div[data-testid="stMetric"] { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }

    /* Botões Profissionais */
    .stButton>button { width: 100%; border-radius: 8px; height: 3.2em; background-color: #1f6feb; color: white; border: none; font-weight: bold; transition: background 0.3s; }
    .stButton>button:hover { background-color: #388bfd; border: none; }
    
    /* Tabs Estilizadas */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #161b22; border-radius: 8px 8px 0 0; padding: 10px 20px; color: white !important; font-weight: 500; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b !important; border-bottom: 2px solid #ff4b4b !important; }
    
    /* Sidebar */
    .css-1634591 { background-color: #161b22; }
    
    /* Inputs */
    .stNumberInput, .stTextInput, .stSelectbox { border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE DADOS (CSVs Simples) ---
DATA_DIR = '.' # Para Streamlit Cloud, os dados ficam na raiz

def carregar_dados(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        # Criar estruturas base se não existirem
        if filename == 'peso.csv': pd.DataFrame(columns=['Data', 'Peso']).to_csv(filepath, index=False)
        if filename == 'treino.csv': pd.DataFrame(columns=['Data', 'Exercicio', 'Peso', 'Reps', 'XP_Set']).to_csv(filepath, index=False)
        if filename == 'dieta.csv': pd.DataFrame(columns=['Data', 'Refeicao', 'Prot', 'Kcal']).to_csv(filepath, index=False)
    return pd.read_csv(filepath)

def salvar_dados(df, filename):
    filepath = os.path.join(DATA_DIR, filename)
    df.to_csv(filepath, index=False)

# Carregar dados inicialmente
df_peso = carregar_dados('peso.csv')
df_treino = carregar_dados('treino.csv')
df_dieta = carregar_dados('dieta.csv')

# --- 4. CÁLCULOS DE PERFORMANCE & XP ---
meta_data = datetime(2026, 7, 10).date()
inicio_data = datetime(2026, 3, 15).date()
dias_restantes = (meta_data - datetime.now().date()).days
progresso_tempo = min((datetime.now().date() - inicio_data).days / (meta_data - inicio_data).days, 1.0)

# XP de Treino (Volume total * multiplicador)
total_xp_treino = df_treino['XP_Set'].sum() if not df_treino.empty else 0

# XP de Dieta (Days hitting protein goal) - Exemplo simples
dias_prot = len(df_dieta[df_dieta['Prot'] >= 150]['Data'].unique()) # Target ligeiramente menor para consistência
total_xp_dieta = dias_prot * 50 # 50 XP por dia de consistência

total_xp = total_xp_treino + total_xp_dieta
xp_level = (total_xp % 10000)
level = int(total_xp // 10000) + 1
xp_next = 10000 - xp_level

def get_rank(lvl):
    if lvl > 15: return "Elite"
    if lvl > 8: return "Avançado"
    if lvl > 3: return "Intermédio"
    return "Recruta"

# --- 5. UI: BARRA LATERAL (Status Profissional) ---
with st.sidebar:
    st.markdown("## 👤 STATUS DO ATLETA")
    st.markdown(f"### Rank: **{get_rank(level)}** (Lvl {level})")
    st.progress(min(xp_level / 10000, 1.0), text=f"{xp_level} XP ({xp_next} XP para Lvl {level+1})")
    
    st.divider()
    
    st.markdown("## 📅 CONTAGEM REGRESSIVA")
    col_dias, col_prog = st.columns([1,2])
    col_dias.metric("Dias", dias_restantes)
    col_prog.progress(progresso_tempo, text=f"{int(progresso_tempo*100)}% Cumprido")

    st.divider()
    st.markdown("## ✅ CHECK-IN RÁPIDO")
    with st.form("checkin_form", clear_on_submit=True):
        p_hoje = st.number_input("Peso de Hoje (kg)", value=77.65, step=0.05)
        submit_p = st.form_submit_button("Registar Peso")
        if submit_p:
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            new_p = pd.DataFrame([[data_hoje, p_hoje]], columns=['Data', 'Peso'])
            df_peso = pd.concat([df_peso, new_p], ignore_index=True)
            salvar_dados(df_peso, 'peso.csv')
            st.success("Peso gravado!")

# --- 6. CORPO PRINCIPAL (TABS) ---
st.title("🎯 Missão 10 de Julho: The HQ")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Dashboard", "🏋️ Performance Log", "🍎 Nutrition Control", "📈 Evolution"])

# --- TAB 1: EXECUTIVE DASHBOARD ---
with tab1:
    col_m1, col_m2, col_m3 = st.columns(3)
    
    # Peso Atual com Tendência
    peso_atual = df_peso['Peso'].iloc[-1] if not df_peso.empty else 77.65
    peso_anterior = df_peso['Peso'].iloc[-2] if len(df_peso) > 1 else peso_atual
    change_peso = peso_atual - peso_anterior
    col_m1.metric("Peso Atual", f"{peso_atual:.2f} kg", f"{change_peso:+.2f} kg vs Anterior")
    
    # Proteína Hoje
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    prot_hoje = df_dieta[df_dieta['Data'] == data_hoje]['Prot'].sum() if not df_dieta.empty else 0
    col_m2.metric("Proteína Hoje (Target 170g)", f"{prot_hoje} g", f"{170 - prot_hoje}g Faltam")
    
    # XP Acumulada (Sinal de esforço)
    col_m3.metric("XP Total", f"{total_xp:,}", f"+{total_xp_dieta} XP Dieta")

    st.divider()
    
    # Gráfico de Peso Profissional
    st.subheader("Tendência de Peso vs Meta (70 kg)")
    if not df_peso.empty:
        df_peso['Data'] = pd.to_datetime(df_peso['Data'])
        
        fig = go.Figure()
        
        # Área sombreada da "Zona de Performance"
        fig.add_trace(go.Scatter(
            x=[inicio_data, meta_data],
            y=[78.5, 71.0], fill=None, mode='lines', line_color='rgba(255, 75, 75, 0)', showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[inicio_data, meta_data],
            y=[76.8, 69.0], fill='tonexty', mode='lines', line_color='rgba(255, 75, 75, 0)', 
            fillcolor='rgba(255, 75, 75, 0.1)', name='Zona de Performance'
        ))

        # Linha Real
        fig.add_trace(go.Scatter(
            x=df_peso['Data'], y=df_peso['Peso'], 
            name='Peso Real', line=dict(color='#ff4b4b', width=4), mode='lines+markers',
            marker=dict(size=8, color='#ff4b4b', line=dict(width=2, color='white'))
        ))
        
        # Linha Meta (Caminho Ideal)
        fig.add_trace(go.Scatter(
            x=[inicio_data, meta_data], y=[77.65, 70.0], 
            name='Caminho Ideal', line=dict(color='#8b949e', dash='dash', width=2)
        ))
        
        fig.update_layout(
            template="plotly_dark", height=400, 
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(gridcolor='#30363d', title='Peso (kg)'),
            xaxis=dict(gridcolor='#30363d')
        )
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: PERFORMANCE LOG (SET-BY-SET) ---
with tab2:
    st.subheader("🏋️ Registo Detalhado de Sets")
    with st.form("treino_form", clear_on_submit=True):
        c_ex, c_p, c_r = st.columns([2,1,1])
        ex_opt = ["Bench Press (DB)", "Dumbbell Row", "Goblet Squat (DB)", "Overhead Press", "Lunge", "Skullcrushers", "Outro"]
        ex = c_ex.selectbox("Exercício", ex_opt)
        p = c_p.number_input("Carga Total (kg)", value=44.0, step=1.0)
        r = c_r.number_input("Reps", value=10, step=1)
        submit_t = st.form_submit_button("✅ Finalizar Set e Ganhar XP")
        
        if submit_t:
            xp_ganho = int(p * r * 0.1) # 10% do volume vira XP
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            new_set = pd.DataFrame([[data_hoje, ex, p, r, xp_ganho]], columns=['Data', 'Exercicio', 'Peso', 'Reps', 'XP_Set'])
            df_treino = pd.concat([df_treino, new_set], ignore_index=True)
            salvar_dados(df_treino, 'treino.csv')
            st.toast(f"Set Gravado! +{xp_ganho} XP", icon="🔥")

    st.divider()
    st.subheader("📜 Histórico de Hoje")
    df_t_hoje = df_treino[df_treino['Data'] == datetime.now().strftime("%Y-%m-%d")]
    if not df_t_hoje.empty:
        st.dataframe(df_t_hoje[['Exercicio', 'Peso', 'Reps', 'XP_Set']], use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum set registado hoje.")

# --- TAB 3: NUTRITION CONTROL ---
with tab3:
    st.subheader("🍎 Diário Alimentar Detalhado")
    with st.form("dieta_form", clear_on_submit=True):
        alimento = st.text_input("Refeição / Alimento", placeholder="Ex: 200g Frango Grelhado")
        col_p, col_k = st.columns(2)
        prot_g = col_p.number_input("Proteína (g)", value=0, step=1)
        kcal_c = col_k.number_input("Calorias (kcal)", value=0, step=1)
        submit_d = st.form_submit_button("🍴 Adicionar à Dieta")
        
        if submit_d:
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            new_food = pd.DataFrame([[data_hoje, alimento, prot_g, kcal_c]], columns=['Data', 'Refeicao', 'Prot', 'Kcal'])
            df_dieta = pd.concat([df_dieta, new_food], ignore_index=True)
            salvar_dados(df_dieta, 'dieta.csv')
            st.success("Alimento adicionado!")

    st.divider()
    st.subheader("📋 Log de Hoje")
    df_d_hoje = df_dieta[df_dieta['Data'] == datetime.now().strftime("%Y-%m-%d")]
    if not df_d_hoje.empty:
        col_list, col_summary = st.columns([2,1])
        with col_list:
            st.dataframe(df_d_hoje[['Refeicao', 'Prot', 'Kcal']], use_container_width=True, hide_index=True)
        with col_summary:
            st.markdown("### Resumo Diário")
            st.write(f"**Total Prot:** {prot_hoje}g / 170g")
            st.write(f"**Total Kcal:** {df_d_hoje['Kcal'].sum()} / ~2300 Kcal")

# --- TAB 4: EVOLUTION ---
with tab4:
    st.subheader("📸 Evolução Visual & Registos")
    col_photo, col_log = st.columns([1,2])
    
    with col_photo:
        photo = st.file_uploader("Upload de foto de Check-in (15 em 15 dias)", type=['jpg', 'png'])
        if photo:
            st.image(photo, caption=f"Check-in: {datetime.now().strftime('%d/%m/%Y')}", use_container_width=True)
            st.info("Dica do Coach: Tira a foto sempre no mesmo local, mesma luz e em jejum.")

    with col_log:
        st.subheader("Histórico Completo de Peso")
        if not df_peso.empty:
            st.dataframe(df_peso.sort_values(by='Data', ascending=False), use_container_width=True, hide_index=True)
