import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="HQ: Missão 10 de Julho", layout="wide", initial_sidebar_state="expanded")

# Criar ficheiros de dados se não existirem
for file in ['treino.csv', 'dieta.csv', 'peso.csv']:
    if not os.path.exists(file):
        if file == 'treino.csv':
            pd.DataFrame(columns=['Data', 'Exercicio', 'Peso', 'Reps', 'XP']).to_csv(file, index=False)
        elif file == 'dieta.csv':
            pd.DataFrame(columns=['Data', 'Alimento', 'Prot', 'Kcal']).to_csv(file, index=False)
        elif file == 'peso.csv':
            pd.DataFrame(columns=['Data', 'Peso']).to_csv(file, index=False)

# --- LÓGICA DE GAMIFICAÇÃO ---
def get_xp():
    df = pd.read_csv('treino.csv')
    return df['XP'].sum()

total_xp = get_xp()
level = int(total_xp // 5000) + 1
xp_next_level = 5000 - (total_xp % 5000)

# --- UI: SIDEBAR ---
with st.sidebar:
    st.title("👤 Status do Atleta")
    st.subheader(f"Rank: {'Elite' if level > 10 else 'Avançado' if level > 5 else 'Recruta'}")
    st.progress(min((total_xp % 5000) / 5000, 1.0), text=f"Level {level} - {xp_next_level} XP para o próximo")
    
    st.divider()
    peso_input = st.number_input("Peso de Hoje (kg)", value=77.65, step=0.05)
    if st.button("Registar Peso"):
        new_p = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), peso_input]], columns=['Data', 'Peso'])
        new_p.to_csv('peso.csv', mode='a', header=False, index=False)
        st.success("Peso gravado!")

# --- UI: CORPO PRINCIPAL ---
st.title("🎯 Missão 10 de Julho")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Performance", "🏋️ Treino", "🍎 Dieta", "📸 Check-in"])

# --- TAB 1: DASHBOARD ---
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tendência de Peso vs Meta")
        df_p = pd.read_csv('peso.csv')
        if not df_p.empty:
            fig = go.Figure()
            # Linha Real
            fig.add_trace(go.Scatter(x=df_p['Data'], y=df_p['Peso'], name='Peso Real', line=dict(color='#ff4b4b', width=4)))
            # Linha Meta (70kg em 10 de Julho)
            fig.add_trace(go.Scatter(x=[df_p['Data'].iloc[0], '2026-07-10'], y=[77.65, 70.0], 
                                     name='Caminho Ideal', line=dict(color='gray', dash='dash')))
            fig.update_layout(template="plotly_dark", height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Proteína Diária (170g Target)")
        df_d = pd.read_csv('dieta.csv')
        hoje = datetime.now().strftime("%Y-%m-%d")
        prot_hoje = df_d[df_d['Data'] == hoje]['Prot'].sum()
        st.metric("Proteína Acumulada", f"{prot_hoje}g", f"{prot_hoje - 170}g vs Meta")
        st.progress(min(prot_hoje / 170, 1.0))

# --- TAB 2: TREINO SET-BY-SET ---
with tab2:
    st.subheader("🏋️ Log de Treino")
    with st.form("set_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([2,1,1])
        ex = c1.selectbox("Exercício", ["Bench Press (DB)", "Dumbbell Row", "Squat (DB)", "Overhead Press", "Lunge", "Outro"])
        p = c2.number_input("Carga (Total kg)", value=44.0)
        r = c3.number_input("Reps", value=10)
        submit = st.form_submit_button("🔥 Finalizar Set")
        
        if submit:
            xp_ganho = int(p * r * 0.1)
            new_set = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), ex, p, r, xp_ganho]], 
                                   columns=['Data', 'Exercicio', 'Peso', 'Reps', 'XP'])
            new_set.to_csv('treino.csv', mode='a', header=False, index=False)
            st.balloons()
            st.success(f"Set Gravado! Ganhaste {xp_ganho} XP.")

# --- TAB 3: DIETA ---
with tab3:
    st.subheader("🍎 Registo de Alimentos")
    with st.form("diet_form", clear_on_submit=True):
        alimento = st.text_input("Refeição", placeholder="Ex: 200g Salmão + 200g Batata Doce")
        c1, c2 = st.columns(2)
        p_g = c1.number_input("Proteína (g)", value=0)
        k_c = c2.number_input("Calorias (kcal)", value=0)
        if st.form_submit_button("🍴 Adicionar ao Diário"):
            new_food = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), alimento, p_g, k_c]], 
                                    columns=['Data', 'Alimento', 'Prot', 'Kcal'])
            new_food.to_csv('dieta.csv', mode='a', header=False, index=False)
            st.success("Nutrição atualizada!")

# --- TAB 4: FOTOS ---
with tab4:
    st.subheader("📸 Evolução Visual")
    photo = st.file_uploader("Captura de Check-in", type=['jpg', 'png'])
    if photo:
        st.image(photo, caption=f"Check-in: {datetime.now().strftime('%d/%m/%Y')}")
        st.info("Dica: Tira a foto sempre no mesmo local e com a mesma luz.")
