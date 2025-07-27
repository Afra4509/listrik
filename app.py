import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import pandas as pd
from io import BytesIO
import base64

# Konfigurasi halaman
st.set_page_config(
    page_title="⚡ Kalkulator Rangkaian Listrik DC",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    with open('physics_listrik.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Fungsi untuk memuat CSS jika file ada, jika tidak gunakan CSS inline
try:
    load_css()
except FileNotFoundError:
    # CSS inline sebagai fallback
    st.markdown("""
    <style>
    /* Dark/Light Mode Variables */
    :root {
        --primary-color: #2E86AB;
        --secondary-color: #A23B72;
        --accent-color: #F18F01;
        --background-light: #F8F9FA;
        --background-dark: #1E1E1E;
        --text-light: #2D3748;
        --text-dark: #E2E8F0;
        --card-light: #FFFFFF;
        --card-dark: #2D3748;
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .physics-card {
        background: var(--card-light);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 15px 0;
        border-left: 4px solid var(--accent-color);
    }
    
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        text-align: center;
    }
    
    .formula-box {
        background: #f8f9fa;
        border: 2px solid var(--primary-color);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        text-align: center;
    }
    
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 10px;
        color: rgba(0,0,0,0.3);
        z-index: 999;
    }
    
    .stSelectbox > div > div {
        border-radius: 10px;
    }
    
    .stNumberInput > div > div > input {
        border-radius: 10px;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary-color) 0%, var(--secondary-color) 100%);
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Watermark
st.markdown("""
<div class="watermark">
    © afrafdhma | Afra Fadhma Dinata
</div>
""", unsafe_allow_html=True)

# Header utama
st.markdown("""
<div class="main-header">
    <h1>⚡ Kalkulator Rangkaian Listrik DC ⚡</h1>
    <p>BAB 02: Rangkaian Listrik Arus Searah - Analisis Interaktif</p>
</div>
""", unsafe_allow_html=True)

# Sidebar untuk input
st.sidebar.markdown("### ⚙️ Panel Kontrol")

# Mode tema
theme_mode = st.sidebar.radio("🎨 Pilih Tema:", ["Light Mode", "Dark Mode"])

# Pilihan kalkulator
calc_type = st.sidebar.selectbox(
    "🧮 Pilih Jenis Kalkulator:",
    [
        "Hukum Ohm (V = I × R)",
        "Hambatan Seri",
        "Hambatan Paralel", 
        "GGL dan Tegangan Jepit",
        "Daya dan Energi Listrik",
        "Hukum Kirchhoff I (KCL)",
        "Hukum Kirchhoff II (KVL)",
        "Analisis DC vs AC"
    ]
)

# Fungsi kalkulator
def ohm_law_calculator():
    st.markdown('<div class="physics-card">', unsafe_allow_html=True)
    st.subheader("⚡ Hukum Ohm Calculator")
    
    # Formula display
    st.markdown("""
    <div class="formula-box">
        <strong>V = I × R</strong><br>
        V = Tegangan (Volt), I = Arus (Ampere), R = Hambatan (Ohm)
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        calc_what = st.radio("Hitung apa?", ["Tegangan (V)", "Arus (I)", "Hambatan (R)"])
        
    with col2:
        if calc_what == "Tegangan (V)":
            I = st.number_input("Arus (A):", value=1.0, step=0.1)
            R = st.number_input("Hambatan (Ω):", value=10.0, step=0.1)
            V = I * R
            result = f"Tegangan = {V:.2f} Volt"
            
        elif calc_what == "Arus (I)":
            V = st.number_input("Tegangan (V):", value=12.0, step=0.1)
            R = st.number_input("Hambatan (Ω):", value=10.0, step=0.1)
            I = V / R if R != 0 else 0
            result = f"Arus = {I:.2f} Ampere"
            
        else:  # Hambatan
            V = st.number_input("Tegangan (V):", value=12.0, step=0.1)
            I = st.number_input("Arus (A):", value=1.0, step=0.1)
            R = V / I if I != 0 else 0
            result = f"Hambatan = {R:.2f} Ohm"
    
    st.markdown(f'<div class="result-box"><h3>{result}</h3></div>', unsafe_allow_html=True)
    
    # Grafik V vs I
    if calc_what == "Tegangan (V)":
        create_vi_graph(R, "ohm")
    
    st.markdown('</div>', unsafe_allow_html=True)

def series_resistance():
    st.markdown('<div class="physics-card">', unsafe_allow_html=True)
    st.subheader("🔗 Hambatan Seri")
    
    st.markdown("""
    <div class="formula-box">
        <strong>R_total = R₁ + R₂ + R₃ + ... + Rₙ</strong>
    </div>
    """, unsafe_allow_html=True)
    
    num_resistors = st.slider("Jumlah Hambatan:", 2, 5, 3)
    resistors = []
    
    cols = st.columns(num_resistors)
    for i in range(num_resistors):
        with cols[i]:
            r = st.number_input(f"R{i+1} (Ω):", value=10.0*(i+1), step=0.1, key=f"series_r{i}")
            resistors.append(r)
    
    R_total = sum(resistors)
    
    st.markdown(f'<div class="result-box"><h3>R_total = {R_total:.2f} Ω</h3></div>', unsafe_allow_html=True)
    
    # Visualisasi rangkaian seri
    create_series_circuit_diagram(resistors)
    
    st.markdown('</div>', unsafe_allow_html=True)

def parallel_resistance():
    st.markdown('<div class="physics-card">', unsafe_allow_html=True)
    st.subheader("⚡ Hambatan Paralel")
    
    st.markdown("""
    <div class="formula-box">
        <strong>1/R_total = 1/R₁ + 1/R₂ + 1/R₃ + ... + 1/Rₙ</strong>
    </div>
    """, unsafe_allow_html=True)
    
    num_resistors = st.slider("Jumlah Hambatan:", 2, 5, 3)
    resistors = []
    
    cols = st.columns(num_resistors)
    for i in range(num_resistors):
        with cols[i]:
            r = st.number_input(f"R{i+1} (Ω):", value=10.0*(i+1), step=0.1, key=f"parallel_r{i}")
            resistors.append(r)
    
    # Perhitungan paralel
    reciprocal_sum = sum(1/r for r in resistors if r != 0)
    R_total = 1/reciprocal_sum if reciprocal_sum != 0 else 0
    
    st.markdown(f'<div class="result-box"><h3>R_total = {R_total:.2f} Ω</h3></div>', unsafe_allow_html=True)
    
    # Visualisasi rangkaian paralel
    create_parallel_circuit_diagram(resistors)
    
    st.markdown('</div>', unsafe_allow_html=True)

def emf_terminal_voltage():
    st.markdown('<div class="physics-card">', unsafe_allow_html=True)
    st.subheader("🔋 GGL dan Tegangan Jepit")
    
    st.markdown("""
    <div class="formula-box">
        <strong>V_terminal = ε - I × r</strong><br>
        ε = GGL (Volt), r = hambatan dalam (Ω), I = Arus (A)
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        emf = st.number_input("GGL - ε (V):", value=12.0, step=0.1)
        internal_r = st.number_input("Hambatan dalam - r (Ω):", value=0.5, step=0.1)
        
    with col2:
        current = st.number_input("Arus - I (A):", value=2.0, step=0.1)
        
    v_terminal = emf - (current * internal_r)
    power_loss = current**2 * internal_r
    efficiency = (v_terminal / emf) * 100 if emf != 0 else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="result-box"><h4>V_terminal<br>{v_terminal:.2f} V</h4></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="result-box"><h4>Rugi Daya<br>{power_loss:.2f} W</h4></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="result-box"><h4>Efisiensi<br>{efficiency:.1f}%</h4></div>', unsafe_allow_html=True)
    
    # Grafik V_terminal vs I
    create_emf_graph(emf, internal_r)
    
    st.markdown('</div>', unsafe_allow_html=True)

def power_energy_calculator():
    st.markdown('<div class="physics-card">', unsafe_allow_html=True)
    st.subheader("⚡ Daya dan Energi Listrik")
    
    st.markdown("""
    <div class="formula-box">
        <strong>P = V × I = I² × R = V²/R</strong><br>
        <strong>W = P × t</strong><br>
        P = Daya (Watt), W = Energi (Joule), t = waktu (detik)
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        V = st.number_input("Tegangan (V):", value=220.0, step=1.0)
        I = st.number_input("Arus (A):", value=5.0, step=0.1)
        
    with col2:
        R = st.number_input("Hambatan (Ω):", value=44.0, step=0.1)
        t_hours = st.number_input("Waktu (jam):", value=1.0, step=0.1)
    
    # Perhitungan daya (3 cara)
    P1 = V * I
    P2 = I**2 * R
    P3 = V**2 / R if R != 0 else 0
    
    # Energi
    t_seconds = t_hours * 3600
    W_joules = P1 * t_seconds
    W_kwh = (P1 * t_hours) / 1000
    
    # Biaya listrik (asumsi Rp 1.500/kWh)
    cost = W_kwh * 1500
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="result-box"><h4>Daya<br>{P1:.1f} W</h4></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="result-box"><h4>Energi<br>{W_kwh:.2f} kWh</h4></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="result-box"><h4>Biaya<br>Rp {cost:.0f}</h4></div>', unsafe_allow_html=True)
    with col4:
        efficiency_rating = "Efisien" if P1 < 100 else "Sedang" if P1 < 500 else "Tinggi"
        st.markdown(f'<div class="result-box"><h4>Rating<br>{efficiency_rating}</h4></div>', unsafe_allow_html=True)
    
    # Grafik konsumsi energi vs waktu
    create_power_time_graph(P1)
    
    st.markdown('</div>', unsafe_allow_html=True)

def kirchhoff_current_law():
    st.markdown('<div class="physics-card">', unsafe_allow_html=True)
    st.subheader("🔄 Hukum Kirchhoff I (KCL)")
    
    st.markdown("""
    <div class="formula-box">
        <strong>ΣI_masuk = ΣI_keluar</strong><br>
        Jumlah arus yang masuk = Jumlah arus yang keluar dari titik cabang
    </div>
    """, unsafe_allow_html=True)
    
    st.write("**Contoh: Titik cabang dengan 3 arus**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        I1 = st.number_input("I₁ masuk (A):", value=5.0, step=0.1)
    with col2:
        I2 = st.number_input("I₂ keluar (A):", value=2.0, step=0.1)
    with col3:
        I3 = st.number_input("I₃ keluar (A):", value=0.0, step=0.1, disabled=True)
    
    # Aplikasi KCL: I1 = I2 + I3
    I3_calculated = I1 - I2
    
    st.markdown(f'<div class="result-box"><h3>I₃ = {I3_calculated:.2f} A</h3></div>', unsafe_allow_html=True)
    
    # Visualisasi titik cabang
    create_kcl_diagram(I1, I2, I3_calculated)
    
    st.markdown('</div>', unsafe_allow_html=True)

def kirchhoff_voltage_law():
    st.markdown('<div class="physics-card">', unsafe_allow_html=True)
    st.subheader("🔄 Hukum Kirchhoff II (KVL)")
    
    st.markdown("""
    <div class="formula-box">
        <strong>ΣV = 0</strong><br>
        Jumlah algebrais tegangan dalam loop tertutup = 0
    </div>
    """, unsafe_allow_html=True)
    
    st.write("**Analisis Loop Sederhana**")
    
    col1, col2 = st.columns(2)
    with col1:
        V_source = st.number_input("Tegangan Sumber (V):", value=12.0, step=0.1)
        R1 = st.number_input("R₁ (Ω):", value=4.0, step=0.1)
        
    with col2:
        R2 = st.number_input("R₂ (Ω):", value=6.0, step=0.1)
        R3 = st.number_input("R₃ (Ω):", value=2.0, step=0.1)
    
    # Analisis loop
    R_total = R1 + R2 + R3
    I_loop = V_source / R_total if R_total != 0 else 0
    
    V1 = I_loop * R1
    V2 = I_loop * R2  
    V3 = I_loop * R3
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="result-box"><h4>Arus Loop<br>{I_loop:.2f} A</h4></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="result-box"><h4>V₁<br>{V1:.2f} V</h4></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="result-box"><h4>V₂<br>{V2:.2f} V</h4></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="result-box"><h4>V₃<br>{V3:.2f} V</h4></div>', unsafe_allow_html=True)
    
    # Verifikasi KVL
    kvl_check = V_source - (V1 + V2 + V3)
    st.write(f"**Verifikasi KVL:** {V_source:.2f} - ({V1:.2f} + {V2:.2f} + {V3:.2f}) = {kvl_check:.3f} ≈ 0 ✓")
    
    # Visualisasi loop
    create_kvl_diagram(V_source, [V1, V2, V3], [R1, R2, R3])
    
    st.markdown('</div>', unsafe_allow_html=True)

def dc_vs_ac_analysis():
    st.markdown('<div class="physics-card">', unsafe_allow_html=True)
    st.subheader("⚡ Analisis DC vs AC")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔋 Arus Searah (DC)")
        st.write("""
        **Karakteristik DC:**
        - Arus konstan, tidak berubah arah
        - Tegangan konstan
        - Frekuensi = 0 Hz
        - Mudah disimpan dalam baterai
        - Cocok untuk elektronik digital
        """)
        
    with col2:
        st.markdown("### ⚡ Arus Bolak-balik (AC)")
        st.write("""
        **Karakteristik AC:**
        - Arus berubah arah secara periodik
        - Tegangan sinusoidal
        - Frekuensi = 50/60 Hz
        - Mudah ditransmisikan jarak jauh
        - Cocok untuk motor dan pemanas
        """)
    
    # Parameter untuk grafik
    frequency = st.slider("Frekuensi AC (Hz):", 1, 100, 50)
    amplitude = st.slider("Amplitudo (V):", 1, 50, 12)
    dc_voltage = st.slider("Tegangan DC (V):", 1, 50, 12)
    
    # Grafik perbandingan DC vs AC
    create_dc_vs_ac_graph(frequency, amplitude, dc_voltage)
    
    # Analisis daya
    st.subheader("📊 Perbandingan Daya")
    col1, col2, col3 = st.columns(3)
    
    rms_voltage = amplitude / math.sqrt(2)
    peak_power_ac = amplitude**2 / 10  # Asumsi R = 10Ω
    avg_power_ac = rms_voltage**2 / 10
    dc_power = dc_voltage**2 / 10
    
    with col1:
        st.markdown(f'<div class="result-box"><h4>Daya DC<br>{dc_power:.1f} W</h4></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="result-box"><h4>Daya AC (RMS)<br>{avg_power_ac:.1f} W</h4></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="result-box"><h4>Daya AC (Peak)<br>{peak_power_ac:.1f} W</h4></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Fungsi untuk membuat grafik
def create_vi_graph(R, type_calc):
    fig = go.Figure()
    
    I_range = np.linspace(0, 5, 100)
    V_range = I_range * R
    
    fig.add_trace(go.Scatter(
        x=I_range, 
        y=V_range,
        mode='lines',
        name=f'V = I × {R}Ω',
        line=dict(color='#2E86AB', width=3)
    ))
    
    fig.update_layout(
        title="📈 Grafik Tegangan vs Arus (Hukum Ohm)",
        xaxis_title="Arus (A)",
        yaxis_title="Tegangan (V)",
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_series_circuit_diagram(resistors):
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # Gambar rangkaian seri sederhana
    y_pos = 0.5
    x_positions = np.linspace(0.1, 0.9, len(resistors))
    
    # Garis penghubung
    ax.plot([0, 1], [y_pos, y_pos], 'k-', linewidth=2)
    ax.plot([0, 0], [0.3, 0.7], 'k-', linewidth=2)
    ax.plot([1, 1], [0.3, 0.7], 'k-', linewidth=2)
    ax.plot([0, 1], [0.3, 0.3], 'k-', linewidth=2)
    ax.plot([0, 1], [0.7, 0.7], 'k-', linewidth=2)
    
    # Hambatan
    for i, (x, r) in enumerate(zip(x_positions, resistors)):
        # Kotak hambatan
        rect = plt.Rectangle((x-0.05, y_pos-0.05), 0.1, 0.1, 
                           fill=True, facecolor='lightblue', edgecolor='blue', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y_pos+0.15, f'R{i+1}\n{r}Ω', ha='center', va='center', fontsize=10, weight='bold')
    
    # Sumber tegangan
    circle = plt.Circle((0.05, 0.5), 0.03, fill=True, facecolor='red', edgecolor='darkred')
    ax.add_patch(circle)
    ax.text(0.05, 0.35, '+', ha='center', va='center', fontsize=12, weight='bold')
    ax.text(0.05, 0.65, '−', ha='center', va='center', fontsize=12, weight='bold')
    
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('🔗 Rangkaian Hambatan Seri', fontsize=14, weight='bold')
    
    st.pyplot(fig)

def create_parallel_circuit_diagram(resistors):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Garis utama
    ax.plot([0.1, 0.9], [0.5, 0.5], 'k-', linewidth=3)  # Garis horizontal utama
    
    # Cabang paralel
    y_positions = np.linspace(0.7, 0.3, len(resistors))
    
    for i, (y, r) in enumerate(zip(y_positions, resistors)):
        # Garis vertikal penghubung
        ax.plot([0.3, 0.3], [0.5, y], 'k-', linewidth=2)
        ax.plot([0.7, 0.7], [0.5, y], 'k-', linewidth=2)
        # Garis horizontal cabang
        ax.plot([0.3, 0.7], [y, y], 'k-', linewidth=2)
        
        # Kotak hambatan
        rect = plt.Rectangle((0.45, y-0.03), 0.1, 0.06, 
                           fill=True, facecolor='lightgreen', edgecolor='green', linewidth=2)
        ax.add_patch(rect)
        ax.text(0.5, y+0.1, f'R{i+1} = {r}Ω', ha='center', va='center', fontsize=10, weight='bold')
    
    # Sumber tegangan
    circle = plt.Circle((0.15, 0.5), 0.04, fill=True, facecolor='red', edgecolor='darkred')
    ax.add_patch(circle)
    ax.text(0.15, 0.45, '+', ha='center', va='center', fontsize=12, weight='bold', color='white')
    ax.text(0.15, 0.55, '−', ha='center', va='center', fontsize=12, weight='bold', color='white')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0.2, 0.8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('⚡ Rangkaian Hambatan Paralel', fontsize=14, weight='bold')
    
    st.pyplot(fig)

def create_emf_graph(emf, internal_r):
    fig = go.Figure()
    
    I_range = np.linspace(0, emf/internal_r, 100)
    V_terminal = emf - (I_range * internal_r)
    
    fig.add_trace(go.Scatter(
        x=I_range,
        y=V_terminal,
        mode='lines',
        name=f'V = {emf} - {internal_r}×I',
        line=dict(color='#A23B72', width=3)
    ))
    
    # Titik operasi
    fig.add_trace(go.Scatter(
        x=[I_range[50]],
        y=[V_terminal[50]], 
        mode='markers',
        name='Titik Operasi',
        marker=dict(size=10, color='red')
    ))
    
    fig.update_layout(
        title="🔋 Karakteristik GGL vs Tegangan Terminal",
        xaxis_title="Arus (A)",
        yaxis_title="Tegangan (V)",
        template="plotly_white",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_power_time_graph(power):
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Konsumsi Energi vs Waktu', 'Estimasi Biaya vs Waktu'),
        vertical_spacing=0.1
    )
    
    time_hours = np.linspace(0, 24, 100)
    energy_kwh = (power * time_hours) / 1000
    cost = energy_kwh * 1500  # Rp/kWh
    
    # Grafik energi
    fig.add_trace(
        go.Scatter(x=time_hours, y=energy_kwh, mode='lines', name='Energi (kWh)',
                  line=dict(color='#2E86AB', width=3)),
        row=1, col=1
    )
    
    # Grafik biaya
    fig.add_trace(
        go.Scatter(x=time_hours, y=cost, mode='lines', name='Biaya (Rp)',
                  line=dict(color='#A23B72', width=3)),
        row=2, col=1
    )
    
    fig.update_layout(
        title="📊 Analisis Konsumsi Energi dan Biaya",
        height=500,
        template="plotly_white"
    )
    
    fig.update_xaxes(title_text="Waktu (jam)", row=2, col=1)
    fig.update_yaxes(title_text="Energi (kWh)", row=1, col=1)
    fig.update_yaxes(title_text="Biaya (Rp)", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)

def create_kcl_diagram(I1, I2, I3):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Titik cabang
    center = (0.5, 0.5)
    ax.plot(center[0], center[1], 'ko', markersize=15)
    ax.text(center[0], center[1]-0.1, 'Node', ha='center', va='top', fontsize=12, weight='bold')
    
    # Arus masuk (I1)
    ax.arrow(0.2, 0.5, 0.25, 0, head_width=0.03, head_length=0.03, fc='green', ec='green', linewidth=3)
    ax.text(0.32, 0.55, f'I₁ = {I1:.1f}A', ha='center', va='bottom', fontsize=11, weight='bold', color='green')
    
    # Arus keluar (I2)
    ax.arrow(0.55, 0.5, 0.25, 0, head_width=0.03, head_length=0.03, fc='red', ec='red', linewidth=3)
    ax.text(0.67, 0.55, f'I₂ = {I2:.1f}A', ha='center', va='bottom', fontsize=11, weight='bold', color='red')
    
    # Arus keluar (I3)
    ax.arrow(0.5, 0.45, 0, -0.25, head_width=0.03, head_length=0.03, fc='blue', ec='blue', linewidth=3)
    ax.text(0.55, 0.32, f'I₃ = {I3:.1f}A', ha='left', va='center', fontsize=11, weight='bold', color='blue')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('🔄 Hukum Kirchhoff I (KCL) - Titik Cabang', fontsize=14, weight='bold')
    
    # Verifikasi KCL
    kcl_text = f'Verifikasi: {I1:.1f} = {I2:.1f} + {I3:.1f} ✓'
    ax.text(0.5, 0.1, kcl_text, ha='center', va='center', fontsize=12, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
    
    st.pyplot(fig)

def create_kvl_diagram(V_source, voltages, resistances):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Kotak untuk representasi loop
    loop_x = [0.2, 0.8, 0.8, 0.2, 0.2]
    loop_y = [0.3, 0.3, 0.7, 0.7, 0.3]
    ax.plot(loop_x, loop_y, 'k-', linewidth=3)
    
    # Sumber tegangan
    ax.add_patch(plt.Circle((0.2, 0.5), 0.05, fill=True, facecolor='red', edgecolor='darkred'))
    ax.text(0.1, 0.5, f'+\n{V_source:.1f}V\n−', ha='center', va='center', fontsize=10, weight='bold')
    
    # Hambatan dan tegangan
    positions = [(0.5, 0.7), (0.8, 0.5), (0.5, 0.3)]
    labels = ['R₁', 'R₂', 'R₃']
    
    for i, ((x, y), label, V, R) in enumerate(zip(positions, labels, voltages, resistances)):
        # Hambatan
        rect = plt.Rectangle((x-0.05, y-0.03), 0.1, 0.06, 
                           fill=True, facecolor='lightblue', edgecolor='blue', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y+0.1, f'{label}\n{R:.1f}Ω', ha='center', va='center', fontsize=10, weight='bold')
        ax.text(x, y-0.1, f'{V:.1f}V', ha='center', va='center', fontsize=10, weight='bold', color='red')
    
    # Panah arah loop
    ax.annotate('', xy=(0.4, 0.6), xytext=(0.35, 0.65),
                arrowprops=dict(arrowstyle='->', lw=2, color='purple'))
    ax.text(0.25, 0.6, 'Arah Loop', ha='center', va='center', fontsize=10, weight='bold', color='purple')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0.1, 0.9)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('🔄 Hukum Kirchhoff II (KVL) - Analisis Loop', fontsize=14, weight='bold')
    
    st.pyplot(fig)

def create_dc_vs_ac_graph(frequency, amplitude, dc_voltage):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Sinyal DC', 'Sinyal AC', 'Perbandingan Amplitudo', 'Spektrum Frekuensi'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Parameter waktu
    t = np.linspace(0, 4/frequency, 1000)
    
    # Sinyal DC
    dc_signal = np.full_like(t, dc_voltage)
    fig.add_trace(
        go.Scatter(x=t, y=dc_signal, mode='lines', name='DC Signal', 
                  line=dict(color='red', width=3)),
        row=1, col=1
    )
    
    # Sinyal AC
    ac_signal = amplitude * np.sin(2 * np.pi * frequency * t)
    fig.add_trace(
        go.Scatter(x=t, y=ac_signal, mode='lines', name='AC Signal',
                  line=dict(color='blue', width=3)),
        row=1, col=2
    )
    
    # Perbandingan pada grafik yang sama
    fig.add_trace(
        go.Scatter(x=t, y=dc_signal, mode='lines', name='DC',
                  line=dict(color='red', width=2, dash='dash')),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=t, y=ac_signal, mode='lines', name='AC',
                  line=dict(color='blue', width=2)),
        row=2, col=1
    )
    
    # Spektrum frekuensi (simplified)
    freqs = [0, frequency]
    dc_spectrum = [dc_voltage, 0]
    ac_spectrum = [0, amplitude/2]
    
    fig.add_trace(
        go.Bar(x=freqs, y=dc_spectrum, name='DC Spectrum', marker_color='red', opacity=0.7),
        row=2, col=2
    )
    fig.add_trace(
        go.Bar(x=freqs, y=ac_spectrum, name='AC Spectrum', marker_color='blue', opacity=0.7),
        row=2, col=2
    )
    
    fig.update_layout(
        title="⚡ Perbandingan Karakteristik DC vs AC",
        height=600,
        template="plotly_white",
        showlegend=True
    )
    
    # Update axes labels
    fig.update_xaxes(title_text="Waktu (s)", row=1, col=1)
    fig.update_xaxes(title_text="Waktu (s)", row=1, col=2)
    fig.update_xaxes(title_text="Waktu (s)", row=2, col=1)
    fig.update_xaxes(title_text="Frekuensi (Hz)", row=2, col=2)
    
    fig.update_yaxes(title_text="Tegangan (V)", row=1, col=1)
    fig.update_yaxes(title_text="Tegangan (V)", row=1, col=2)
    fig.update_yaxes(title_text="Tegangan (V)", row=2, col=1)
    fig.update_yaxes(title_text="Amplitudo (V)", row=2, col=2)
    
    st.plotly_chart(fig, use_container_width=True)

def analyze_circuit_efficiency(power, voltage, current):
    """Analisis efisiensi dan rekomendasi"""
    analysis = {
        "efficiency": "Optimal",
        "recommendation": "Rangkaian bekerja dengan baik",
        "warning": None,
        "color": "green"
    }
    
    if power > 1000:
        analysis["efficiency"] = "Tinggi"
        analysis["recommendation"] = "Pertimbangkan penggunaan komponen dengan rating daya lebih tinggi"
        analysis["warning"] = "⚠️ Konsumsi daya tinggi"
        analysis["color"] = "orange"
    
    if voltage > 240:
        analysis["efficiency"] = "Overload"
        analysis["recommendation"] = "Periksa spesifikasi tegangan maksimum komponen"
        analysis["warning"] = "🚨 Tegangan melebihi batas normal"
        analysis["color"] = "red"
    
    if current > 10:
        analysis["efficiency"] = "Arus Tinggi"
        analysis["recommendation"] = "Gunakan kabel dengan diameter lebih besar"
        analysis["warning"] = "⚠️ Arus tinggi - risiko panas berlebih"
        analysis["color"] = "orange"
    
    return analysis

def download_plot_as_png(fig, filename):
    """Fungsi untuk download grafik sebagai PNG"""
    img_bytes = fig.to_image(format="png", engine="kaleido")
    
    st.download_button(
        label="📥 Download Grafik PNG",
        data=img_bytes,
        file_name=f"{filename}.png",
        mime="image/png"
    )

# Main app logic
def main():
    # Pilihan kalkulator berdasarkan input sidebar
    if calc_type == "Hukum Ohm (V = I × R)":
        ohm_law_calculator()
        
    elif calc_type == "Hambatan Seri":
        series_resistance()
        
    elif calc_type == "Hambatan Paralel":
        parallel_resistance()
        
    elif calc_type == "GGL dan Tegangan Jepit":
        emf_terminal_voltage()
        
    elif calc_type == "Daya dan Energi Listrik":
        power_energy_calculator()
        
    elif calc_type == "Hukum Kirchhoff I (KCL)":
        kirchhoff_current_law()
        
    elif calc_type == "Hukum Kirchhoff II (KVL)":
        kirchhoff_voltage_law()
        
    elif calc_type == "Analisis DC vs AC":
        dc_vs_ac_analysis()
    
    # Panel analisis otomatis
    st.markdown("---")
    st.subheader("🔍 Analisis Otomatis & Rekomendasi")
    
    # Simulasi analisis berdasarkan input terakhir
    if calc_type == "Daya dan Energi Listrik":
        try:
            # Ambil nilai dari session state jika ada
            sample_power = 500  # Default value
            sample_voltage = 220
            sample_current = 2.3
            
            analysis = analyze_circuit_efficiency(sample_power, sample_voltage, sample_current)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="physics-card" style="border-left-color: {analysis['color']};">
                    <h4>📊 Status Efisiensi</h4>
                    <p><strong>Rating:</strong> {analysis['efficiency']}</p>
                    <p><strong>Rekomendasi:</strong> {analysis['recommendation']}</p>
                    {f"<p style='color: {analysis['color']};'>{analysis['warning']}</p>" if analysis['warning'] else ""}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Tips hemat energi
                st.markdown("""
                <div class="physics-card">
                    <h4>💡 Tips Hemat Energi</h4>
                    <ul>
                        <li>Gunakan perangkat dengan efisiensi tinggi</li>
                        <li>Matikan perangkat saat tidak digunakan</li>
                        <li>Periksa isolasi kabel secara berkala</li>
                        <li>Gunakan stabilizer untuk perangkat sensitif</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
        except Exception as e:
            st.info("Masukkan nilai pada kalkulator untuk melihat analisis otomatis")
    
    # Footer dengan informasi tambahan
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="physics-card">
            <h5>📚 Materi Terkait</h5>
            <p>• Hukum Ohm dan Kirchhoff<br>
            • Rangkaian DC<br>
            • Analisis Node dan Loop<br>
            • Daya dan Efisiensi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="physics-card">
            <h5>🎯 Fitur Aplikasi</h5>
            <p>• Kalkulator Interaktif<br>
            • Visualisasi Rangkaian<br>
            • Grafik Real-time<br>
            • Analisis Otomatis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="physics-card">
            <h5>⚡ Aplikasi Praktis</h5>
            <p>• Desain Rangkaian<br>
            • Analisis Efisiensi<br>
            • Troubleshooting<br>
            • Optimasi Daya</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
