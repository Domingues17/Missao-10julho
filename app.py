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

# --- 2. CSS PERSONALIZADO (Professional Elite Design) ---
st.markdown("""
    <style>
    /* Fundo Principal, Cores & Fontes */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }
    
    /* Hierarquia Visual e Títulos */
    h1, h2, h3, h4 { color: #f0f2f6 !important; font-weight: 700; border: none !important; }
    .main-title { font-size: 2.2rem !important; margin-bottom: 0.5rem !important; text-align: left; }
    .sub-title { font-size: 0.9rem !important; color: #8b949e !important; text-align: left; margin-bottom: 2rem !important; }

    /* Cards de Métricas Estilizados (Dashboard) */
    [data-testid="stMetricValue"] { font-size: 2.0rem !important; color: #f0f2f6 !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { font-size: 0.85rem !important; color: #8b949e !important; font-weight: 500 !important; }
    [data-testid="stMetricDelta"] { color: #f0f2f6 !important; font-size: 0.8rem !important; }

    div[data-testid="stMetric"] { 
        background-color: #161b22; 
        border-radius: 12px; 
        padding: 20px 25px; 
        border: 1px solid #30363d; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div[data-testid="stMetric"]:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 6px 18px rgba(0,0,0,0.5); 
        border-color: #444c56;
    }

    /* Botões Profissionais (Gradients & Shadows) */
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%); 
        color: white; border: none; font-weight: 600; font-size: 0.95rem; 
        transition: background 0.3s, box-shadow 0.3s; 
        box-shadow: 0 4px 6px rgba(31, 111, 235, 0.3);
    }
    .stButton>button:hover { background: linear-gradient(135deg, #388bfd 0%, #1f6feb 100%); box-shadow: 0 6px 10px rgba(31, 111, 235, 0.5); border: none; }
    
    /* Botões de Carga do Dia (PPL+UL) */
    div.row-widget.stButton button:not([id^="checkin_form"]) { background: none; border: 1px solid #30363d; color: #8b949e; background-color: #161b22; }
    div.row-widget.stButton button:not([id^="checkin_form"]):hover { background-color: #30363d; color: white; border-color: #444c56; }

    /* Tabs Estilizadas (Clean & Minimalist) */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 2px solid #30363d; padding-bottom: 2px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: transparent; border-radius: 10px 10px 0 0; 
        padding: 12px 25px; color: #8b949e !important; font-weight: 500; font-size: 0.95rem;
        transition: color 0.2s, background 0.2s;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #161b22 !important; color: #f0f2f6 !important; border: 2px solid #30363d !important; border-bottom: none !important; margin-bottom: -2px;
        box-shadow: 0 -4px 6px rgba(0,0,0,0.2);
    }
    
    /* Sidebar Profissional */
    .css-1634591, section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .css-1544g2n { color: #c9d1d9; }

    /* Inputs Detalhados */
    .stNumberInput, .stTextInput, .stSelectbox { border-radius: 10px !important; background-color: #0d1117 !important; border: 1px solid #30363d !important; color: #c9d1d9 !important; padding: 10px !important; }
    .stNumberInput input, .stTextInput input, .stSelectbox select { color: #c9d1d9 !important; font-size: 0.9rem !important; }
    
    /* Formulários & Tabelas */
    div[data-testid="stForm"] { background-color: #161b22; border-radius: 12px; padding: 25px; border: 1px solid #30363d; }
    div[data-testid="stDataFrame"] { border-radius: 10px; border: 1px solid #30363d; background-color: #0d1117; }
    
    /* Custom Element Styles */
    .section-card { background-color: #161b22; border-radius: 12px; padding: 20px; border: 1px solid #30363d; margin-bottom: 1.5rem; }
    
    /* Progress Bars Personalizadas */
    div[data-testid="stProgress"] > div > div > div { background: linear-gradient(135deg, #ff4b4b 0%, #f0f2f6 100%); border-radius: 6px; }
    div[data-testid="stProgress"] div[role="progressbar"]::after { color: #f0f2f6; font-size: 0.8rem; font-weight: 600; }
    
    /* Status Badge Style */
    .status-badge { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; background-color: #30363d; color: #8b949e; }
    .status-badge.elite { background-color: #ff4b4b; color: #f0f2f6; }
    .status-badge.avancado { background-color: #1f6feb; color: #f0f2f6; }
    .status-badge.intermedio { background-color: #28A745; color: white; }
    .status-badge.recruta { background-color: #444c56; color: white; }
    
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
# Registos de hoje para dashboard
data_hoje_str = datetime.now().strftime("%Y-%m-%d")
prot_hoje = df_dieta[df_dieta['Data'] == data_hoje_str]['Prot'].sum() if not df_dieta.empty else 0
kcal_hoje = df_dieta[df_dieta['Data'] == data_hoje_str]['Kcal'].sum() if not df_dieta.empty else 0

# XP por consistência (registo diário)
dias_registo_dieta = len(df_dieta['Data'].unique())
dias_registo_treino = len(df_treino['Data'].unique())
total_xp_consistencia = (dias_registo_dieta + dias_registo_treino) * 20 # 20 XP por dia de registo

# XP por meta de proteína
dias_meta_prot = len(df_dieta[df_dieta['Prot'] >= 150]['Data'].unique()) # Target ligeiramente menor para consistência
total_xp_meta_prot = dias_meta_prot * 100 # 100 XP por dia batendo a meta

# TOTAL XP (Aumentámos os targets para os níveis serem mais difíceis)
XP_PER_LEVEL = 15000 # 15k XP por nível
total_xp = int(total_xp_treino + total_xp_consistencia + total_xp_meta_prot)
xp_level = (total_xp % XP_PER_LEVEL)
level = int(total_xp // XP_PER_LEVEL) + 1
xp_next = XP_PER_LEVEL - xp_level

def get_rank_v3(lvl):
    if lvl > 12: return "ELITE", "elite"
    if lvl > 7: return "AVANÇADO", "avancado"
    if lvl > 3: return "INTERMÉDIO", "intermedio"
    return "RECRUTA", "recruta"

# Rank do dia
rank_text, rank_class = get_rank_v3(level)

# --- 5. UI: BARRA LATERAL (Professional Status View) ---
with st.sidebar:
    st.markdown("## 🛡️ STATUS DO ATLETA")
    st.markdown(f"**Rank Atual:** <span class='status-badge {rank_class}'>{rank_text} (Lvl {level})</span>", unsafe_allow_html=True)
    st.progress(min(xp_level / XP_PER_LEVEL, 1.0), text=f"{xp_level:,} XP (Faltam {xp_next:,} XP p/ Lvl {level+1})")
    
    st.divider()
    
    st.markdown("## 📅 CONTAGEM REGRESSIVA")
    col_dias_side, col_prog_side = st.columns([1,1])
    col_dias_side.metric("Dias p/ Meta", dias_restantes, help="Julho 10, 2026")
    col_prog_side.metric("% Cumprido", f"{int(progresso_tempo*100)}%", help=f"Check-in: Março 15")
    st.progress(progresso_tempo)

    st.divider()
    st.markdown("## ✅ REGISTO DO DIA")
    with st.form("checkin_form_side", clear_on_submit=True):
        p_hoje = st.number_input("Peso de Hoje (kg)", value=77.65, step=0.05, format="%.2f")
        submit_p = st.form_submit_button("Atualizar Peso")
        if submit_p:
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            # Substituir se já houver registo hoje, senão adicionar
            if not df_peso.empty and data_hoje in df_peso['Data'].values:
                df_peso.loc[df_peso['Data'] == data_hoje, 'Peso'] = p_hoje
            else:
                new_p = pd.DataFrame([[data_hoje, p_hoje]], columns=['Data', 'Peso'])
                df_peso = pd.concat([df_peso, new_p], ignore_index=True)
            salvar_dados(df_peso, 'peso.csv')
            st.success("Peso gravado!")
            # Recarregar para garantir que o dashboard atualiza
            st.rerun()

# --- 6. CORPO PRINCIPAL (Professional Tabs) ---
st.markdown("<h1 class='main-title'>Missão 10 de Julho: The HQ</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Plano de Recomposição Corporal: 77.65 kg → 70.00 kg. Ganhar Massa e Secar Gordura.</p>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🏋️ Diário de Treino", "🍎 Nutrição & Macros", "📈 Evolução"])

# --- TAB 1: DASHBOARD (Professional View) ---
with tab1:
    col_m1, col_m2, col_m3 = st.columns(3)
    
    # Peso Atual com Tendência (Calculado no carregamento para evitar erro se df vazio)
    peso_atual = df_peso['Peso'].iloc[-1] if not df_peso.empty else 77.65
    peso_anterior = df_peso['Peso'].iloc[-2] if len(df_peso) > 1 else peso_atual
    change_peso = peso_atual - peso_anterior
    # Meta Ideal para hoje
    data_hoje_dt = datetime.now().date()
    # Interpolação linear da meta: 77.65 em inicio_data, 70.0 em meta_data
    percent_temp = (data_hoje_dt - inicio_data).days / (meta_data - inicio_data).days
    peso_ideal_hoje = 77.65 - (percent_temp * (77.65 - 70.0))
    dist_ideal = peso_atual - peso_ideal_hoje

    col_m1.metric("Peso Atual", f"{peso_atual:.2f} kg", f"{change_peso:+.2f} kg vs Anterior", help=f"Caminho ideal: {peso_ideal_hoje:.2f}kg")
    
    # Proteína Hoje
    col_m2.metric("Proteína Hoje (Target 170g)", f"{prot_hoje} g", f"{170 - prot_hoje}g Faltam", help=f"Total Diário: {kcal_hoje:.0f} Kcal")
    
    # XP Acumulada
    col_m3.metric("XP Total de Missão", f"{total_xp:,}", f"+{total_xp_meta_prot:,} XP Prot", help=f"Volume: {total_xp_treino:,} XP | Dieta: {total_xp_meta_prot + total_xp_consistencia:,} XP")

    st.divider()
    
    # Gráfico de Peso Profissional (Melhorias Visuais Premium)
    if not df_peso.empty:
        st.subheader("Tendência de Peso vs Caminho Ideal (Meta 70.0 kg)")
        df_peso['Data'] = pd.to_datetime(df_peso['Data'])
        
        # Filtrar registos repetidos por data para o gráfico se necessário (caso de erro na gravação)
        df_peso_plot = df_peso.sort_values(by='Data').drop_duplicates(subset='Data', keep='last')
        
        fig = go.Figure()
        
        # Área sombreada da "Zona de Performance" (Suave)
        fig.add_trace(go.Scatter(
            x=[inicio_data, meta_data],
            y=[78.5, 71.0], fill=None, mode='lines', line_color='rgba(255, 75, 75, 0)', showlegend=False
        ))
        fig.add_trace(go.Scatter(
            x=[inicio_data, meta_data],
            y=[76.8, 69.0], fill='tonexty', mode='lines', line_color='rgba(255, 75, 75, 0)', 
            fillcolor='rgba(255, 75, 75, 0.08)', name='Zona de Performance Ideal'
        ))

        # Linha Real (Premium: Brilho e Marcador Personalizado)
        fig.add_trace(go.Scatter(
            x=df_peso_plot['Data'], y=df_peso_plot['Peso'], 
            name='Peso Real', mode='lines+markers',
            line=dict(color='#ff4b4b', width=4),
            marker=dict(size=9, color='#ff4b4b', line=dict(width=2, color='#f0f2f6'))
        ))
        
        # Linha Meta (Caminho Ideal - Suave e Truncada)
        fig.add_trace(go.Scatter(
            x=[inicio_data, meta_data], y=[77.65, 70.0], 
            name='Caminho Ideal', line=dict(color='#8b949e', dash='dot', width=1.5)
        ))
        
        fig.update_layout(
            template="plotly_dark", height=420, 
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(gridcolor='#1e2229', title='Peso (kg)', showgrid=True, tickfont=dict(color='#8b949e')),
            xaxis=dict(gridcolor='#1e2229', showgrid=True, tickfont=dict(color='#8b949e'))
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Regista o teu peso na barra lateral para ver o teu progresso visual.")

# --- TAB 2: TREINO (SET-BY-SET LOG) ---
with tab2:
    st.markdown("<h3 style='margin-bottom: 0.5rem;'>Diário de Performance Log: PPL (Push/Pull/Legs)</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: #8b949e; margin-bottom: 1.5rem;'>Segunda: Pull (Costas/Biceps), Terça: Push (Peito/Ombro/Triceps), Quarta: Legs (Pernas). Repetir ciclo (UL opcional).</p>", unsafe_allow_html=True)
    
    col_t_log, col_t_hist = st.columns([2,1])
    
    with col_t_log:
        with st.form("treino_form", clear_on_submit=True):
            st.markdown("#### Novo Set Concluído")
            c_ex, c_p, c_r = st.columns([2,1,1])
            # Exercícios focados e optimizados (remoção de duplicações desnecessárias)
            ex_opt = [
                "Bench Press (DB) [P]", "Incline DB Press [P]", "Dumbbell Squeeze Press [P]", "Skullcrusher (DB) [P]", "Chest Fly (DB) [P]",
                "Dumbbell Row [P]", "Chest Supported Incline Row [P]", "Zottman Curl (DB) [P]", "Shrug (DB) [P]", "Bicep Curl [P]", "Hammer Curl [P]",
                "Squat (DB) [P]", "Lunge (DB) [P]", "Deadlift (DB) [P]", "Overhead Press (DB) [P]", "Lateral Raise (DB) [P]", "Front Raise (DB) [P]",
                "Standing Calf Raise [P]", "Push Up [P]", "Outro [P]"
            ]
            ex = c_ex.selectbox("Exercício", ex_opt)
            # Carregar peso habitual para o exercício se houver histórico recente
            peso_habitual = df_treino[df_treino['Exercicio'] == ex]['Peso'].iloc[-1] if not df_treino.empty and ex in df_treino['Exercicio'].values else 44.0
            p = c_p.number_input("Carga Total (2 DB's) [kg]", value=peso_habitual, step=1.0)
            r = c_r.number_input("Reps (per Set)", value=10, step=1)
            submit_t = st.form_submit_button("🔥 Finalizar Set & Progredir Carga")
            
            if submit_t:
                if p <= 0 or r <= 0:
                    st.error("Peso e Reps devem ser maiores que zero.")
                else:
                    xp_ganho = int(p * r * 0.1) # 10% do volume vira XP
                    data_hoje_str = datetime.now().strftime("%Y-%m-%d")
                    new_set = pd.DataFrame([[data_hoje_str, ex, p, r, xp_ganho]], columns=['Data', 'Exercicio', 'Peso', 'Reps', 'XP_Set'])
                    df_treino = pd.concat([df_treino, new_set], ignore_index=True)
                    salvar_dados(df_treino, 'treino.csv')
                    st.toast(f"Set de {ex} Gravado! +{xp_ganho} XP de Performance", icon="🔥")
                    st.rerun() # Atualizar para mostrar no histórico

    with col_t_hist:
        st.markdown("#### Histórico de Hoje")
        df_t_hoje = df_treino[df_treino['Data'] == datetime.now().strftime("%Y-%m-%d")]
        if not df_t_hoje.empty:
            # Ordenar por histórico para ver o volume acumulado
            df_t_hoje_grp = df_t_hoje.groupby(['Exercicio', 'Peso']).agg({'Reps': 'sum', 'XP_Set': 'sum'}).reset_index()
            st.dataframe(df_t_hoje_grp[['Exercicio', 'Peso', 'Reps', 'XP_Set']], use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum set registado hoje.")

# --- TAB 3: NUTRIÇÃO & MACROS (PROFESSIONAL CONTROL) ---
with tab3:
    st.subheader("🍎 Controlo de Nutrição: 'Fuel for performance'")
    st.markdown("<p style='font-size: 0.85rem; color: #8b949e; margin-bottom: 2rem;'>Objetivo diário: ~2300 Kcal (170g Proteína, 62g Gordura, ~260g Hidratos). Jejum Intermitente (16/8) ativo até 12:30.</p>", unsafe_allow_html=True)
    
    col_d_log, col_d_hist = st.columns([2,1])
    
    with col_d_log:
        with st.form("dieta_form", clear_on_submit=True):
            st.markdown("#### Nova Refeição/Alimento")
            alimento = st.text_input("Refeição / Alimento", placeholder="Ex: 200g Salmão + 250g Batata Doce")
            col_p, col_k = st.columns(2)
            prot_habitual = df_dieta[df_dieta['Refeicao'] == alimento]['Prot'].iloc[-1] if not df_dieta.empty and alimento in df_dieta['Refeicao'].values else 0
            kcal_habitual = df_dieta[df_dieta['Refeicao'] == alimento]['Kcal'].iloc[-1] if not df_dieta.empty and alimento in df_dieta['Refeicao'].values else 0
            prot_g = col_p.number_input("Proteína (g)", value=prot_habitual, step=1)
            kcal_c = col_k.number_input("Calorias (kcal)", value=kcal_habitual, step=1)
            submit_d = st.form_submit_button("🍴 Adicionar ao Diário Alimentar")
            
            if submit_d:
                if (prot_g == 0 and kcal_c == 0) or alimento == "":
                    st.error("Alimento e pelo menos um macro devem ser preenchidos.")
                else:
                    data_hoje_str = datetime.now().strftime("%Y-%m-%d")
                    new_food = pd.DataFrame([[data_hoje_str, alimento, prot_g, kcal_c]], columns=['Data', 'Refeicao', 'Prot', 'Kcal'])
                    df_dieta = pd.concat([df_dieta, new_food], ignore_index=True)
                    salvar_dados(df_dieta, 'dieta.csv')
                    st.success(f"{alimento} adicionado ao diário alimentares de hoje.")
                    st.rerun()

    with col_d_hist:
        st.markdown("#### Histórico de Hoje")
        df_d_hoje = df_dieta[df_dieta['Data'] == datetime.now().strftime("%Y-%m-%d")]
        if not df_d_hoje.empty:
            st.dataframe(df_d_hoje[['Refeicao', 'Prot', 'Kcal']], use_container_width=True, hide_index=True)
            
            st.markdown("### Resumo Diário")
            c_prot, c_kcal = st.columns(2)
            # Metric formatado profissionalmente (substituição de stMetric)
            
            p_rem = 170 - prot_hoje
            k_rem = 2300 - kcal_hoje
            
            p_text = f"**{prot_hoje}g** <span style='color: #8b949e; font-size: 0.8rem;'>/ 170g (Bater Meta!)</span>" if p_rem > 0 else f"**{prot_hoje}g** <span style='color: #28A745; font-size: 0.8rem;'>Meta Batida! (+{-p_rem}g)</span>"
            k_text = f"**{kcal_hoje:.0f}** <span style='color: #8b949e; font-size: 0.8rem;'>Kcal / ~2300 Kcal</span>" if k_rem > 0 else f"**{kcal_hoje:.0f}** <span style='color: #ff4b4b; font-size: 0.8rem;'>/ Défice Ultrpassado (+{-k_rem:.0f}Kcal)</span>"

            # Simular um Styled Metric Card
            with c_prot:
                st.markdown(f"<div style='background-color: #0d1117; padding: 10px; border-radius: 8px; border: 1px solid #30363d;'><span style='color: #8b949e; font-size: 0.8rem;'>Total Proteína:</span><br>{p_text}</div>", unsafe_allow_html=True)
            with c_kcal:
                st.markdown(f"<div style='background-color: #0d1117; padding: 10px; border-radius: 8px; border: 1px solid #30363d;'><span style='color: #8b949e; font-size: 0.8rem;'>Total Kcal:</span><br>{k_text}</div>", unsafe_allow_html=True)

        else:
            st.info("Nenhum alimento registado hoje.")

# --- TAB 4: EVOLUÇÃO (VISUAL & HISTÓRICO COMPLETO) ---
with tab4:
    st.subheader("📈 Evolução Visual & Progressão de Missão")
    st.markdown("<p style='font-size: 0.85rem; color: #8b949e; margin-bottom: 2rem;'>Aqui podes fazer o tracking visual da tua recomposição corporal e ver o teu histórico completo de dados.</p>", unsafe_allow_html=True)
    
    col_photo, col_log = st.columns([1,1])
    
    with col_photo:
        with st.container():
            st.markdown("#### Check-in Visual")
            st.markdown("<p style='font-size: 0.8rem; color: #8b949e;'>Faz o upload da tua foto a cada 15 dias para criar a tua time-lapse visual da transformação.</p>", unsafe_allow_html=True)
            photo = st.file_uploader("Upload de foto (JPG/PNG)", type=['jpg', 'png'], help="Dica do Coach: Foto em jejum, mesma luz, mesmo local.")
            if photo:
                st.image(photo, caption=f"Check-in: {datetime.now().strftime('%d/%m/%Y')} | Lembrete: Próxima foto em 15 dias.", use_container_width=True)
                # No CSV por simplicidade, as fotos não são guardadas localmente pelo Streamlit (seria necessária uma DB de blobs ou AWS S3). 
                # Esta secção é apenas um visualizador para o check-in do dia.

    with col_log:
        st.markdown("#### Histórico Completo de Peso")
        if not df_peso.empty:
            df_peso_log = df_peso.sort_values(by='Data', ascending=False)
            df_peso_log['Data'] = pd.to_datetime(df_peso_log['Data']).dt.date
            st.dataframe(df_peso_log, use_container_width=True, hide_index=True)
            
            # Cálculo Profissional da Taxa de Perda
            primeiro_peso = df_peso['Peso'].iloc[0]
            primeira_data = pd.to_datetime(df_peso['Data'].iloc[0])
            hoje_dt = pd.to_datetime(datetime.now().strftime("%Y-%m-%d"))
            dias_passados = (hoje_dt - primeira_data).days
            perda_total_real = primeiro_peso - peso_atual
            
            if dias_passados > 0:
                taxa_semanal = (perda_total_real / dias_passados) * 7
                perda_falta = peso_atual - 70.0
                taxa_falta = (perda_falta / dias_restantes) * 7 if dias_restantes > 0 else 0
                
                st.markdown("<br>#### Resumo de Progressão", unsafe_allow_html=True)
                c_taxa, c_falta = st.columns(2)
                with c_taxa:
                    st.markdown(f"<div style='background-color: #0d1117; padding: 10px; border-radius: 8px; border: 1px solid #30363d;'><span style='color: #8b949e; font-size: 0.8rem;'>Taxa Semanal Atual:</span><br>**{taxa_semanal:.2f} kg / semana**<br><span style='color: #8b949e; font-size: 0.75rem;'>Défice real: {taxa_semanal * 7700 / 7:.0f} Kcal/dia</span></div>", unsafe_allow_html=True)
                with c_falta:
                    status_cor = "#28A745" if taxa_falta <= taxa_semanal else "#ff4b4b"
                    st.markdown(f"<div style='background-color: #0d1117; padding: 10px; border-radius: 8px; border: 1px solid #30363d;'><span style='color: #8b949e; font-size: 0.8rem;'>Perda Necessária p/ Meta:</span><br>**<span style='color: {status_cor};'>{taxa_falta:.2f} kg / semana</span>**<br><span style='color: #8b949e; font-size: 0.75rem;'>Faltam: {perda_falta:.1f}kg p/ 70kg em {dias_restantes} dias</span></div>", unsafe_allow_html=True)
            else:
                st.info("Iniciaste hoje a tua jornada. O histórico de progressão aparecerá amanhã.")

