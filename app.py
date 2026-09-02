import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time
import base64
import os

# Pengaturan Tampilan Layar (Wide Mode)
st.set_page_config(page_title="Rating UPDL Jakarta", page_icon="⚡", layout="wide")

# Fungsi untuk membaca file gambar menjadi kode yang bisa dibaca HTML
def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return "" 

# Memanggil gambar logo
img_danantara = get_image_base64("logo_danantara.png")
img_pln = get_image_base64("Logo_PLN.svg.png")

# INJEKSI CSS KUSTOM
st.markdown("""
<style>
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 1rem !important;
}
.stApp {
    background-color: #f6f8f9;
}
div[data-testid="stFeedback"] {
    transform: scale(4.5); 
    transform-origin: left center;
    margin-left: 10px; 
}
div[data-testid="stVerticalBlock"] > div > div {
    margin-bottom: 45px; 
}

/* --- PERBAIKAN UKURAN TEKS DENGAN !important --- */
.tanya-teks {
    font-size: 30px !important; /* Silakan ubah angka ini jika ingin lebih besar lagi */
    font-weight: 900 !important;
    color: #1a6bb8 !important; 
    margin-bottom: 0px !important;
    line-height: 1.1 !important;
    text-transform: uppercase !important;
    font-family: 'Arial Black', Impact, sans-serif !important;
}

div[data-testid="stButton"] button {
    background-color: #004581 !important; 
    color: white !important;
    font-weight: 900 !important;
    border-radius: 40px !important;
    padding: 10px 30px !important; 
    border: none !important;
    box-shadow: 0 6px 10px rgba(0,0,0,0.15);
    margin-top: 20px !important; 
}
div[data-testid="stButton"] button p {
    font-size: 42px !important; 
    font-family: 'Arial Black', Impact, sans-serif !important; 
}
.header-mockup {
    background-color: #004581; 
    padding: 15px 30px; 
    border-radius: 10px;
    margin-bottom: 40px; 
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
}
.logo-danantara {
    height: 105px; 
    object-fit: contain;
}
.logo-pln {
    height: 70px; 
    object-fit: contain;
}
.header-text {
    text-align: center;
    flex-grow: 1; 
}
.header-text h1 {
    color: white;
    font-size: 42px; 
    font-weight: 900;
    font-family: 'Arial Black', Impact, sans-serif; 
    margin: 0;
    line-height: 1.1;
}

/* --- ANIMASI LINGKARAN LOADING (BARU) --- */
.animasi-loading {
    border: 16px solid #f3f3f3; /* Warna abu muda */
    border-radius: 50%;
    border-top: 16px solid #15a5a5; /* Warna tosca */
    border-bottom: 16px solid #004581; /* Warna biru tua */
    width: 120px;
    height: 120px;
    animation: putar 1.5s linear infinite;
    margin: 0 auto;
}
@keyframes putar {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

layar_utama = st.empty()

# --- FUNGSI BARU: MENAMPILKAN LOADING LALU MENYIMPAN DATA ---
def proses_simpan_data(pelayanan, kebersihan, keramahan):
    # 1. Kosongkan tampilan form rating
    layar_utama.empty()
    
    # 2. Tampilkan layar Loading Animasi
    with layar_utama.container():
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<div class='animasi-loading'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 50px; color: #004581; margin-top: 30px;'>⏳ Sedang Menyimpan Data...</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #666;'>Mohon tunggu sebentar</h3>", unsafe_allow_html=True)
        
    # 3. Lakukan proses komunikasi ke Google Sheets (Secara background)
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_lama = conn.read(ttl=0)
        
        data_baru = pd.DataFrame([{
            "Waktu": pd.Timestamp.now(tz='Asia/Jakarta').strftime('%Y-%m-%d %H:%M:%S'),
            "Pelayanan": pelayanan + 1,
            "Kebersihan": kebersihan + 1,
            "Keramahan Admin": keramahan + 1 
        }])
        
        df_update = pd.concat([df_lama, data_baru], ignore_index=True)
        conn.update(data=df_update)
        
        # 4. Jika Google Sheets sudah selesai menyimpan, pindah ke layar Terima Kasih
        tampilkan_layar_penutup()
        
    except Exception as e:
        # Jika gagal (misal internet putus)
        layar_utama.empty()
        with layar_utama.container():
            st.error(f"⚠️ Gagal menyimpan data. Pastikan koneksi internet stabil. Detail: {e}")
            time.sleep(4)
            st.rerun()

def tampilkan_form():
    with layar_utama.container():
        
        st.markdown(f"""
<div class='header-mockup'>
    <img class="logo-danantara" src="data:image/png;base64,{img_danantara}" alt="Logo Danantara" onerror="this.style.display='none'">
    <div class="header-text">
        <h1>RATING KEPUASAN PESERTA<br>UPDL JAKARTA</h1>
    </div>
    <img class="logo-pln" src="data:image/png;base64,{img_pln}" alt="Logo PLN" onerror="this.style.display='none'">
</div>
        """, unsafe_allow_html=True)
        
        col1_space, col1_kiri, col1_kanan, col1_space2 = st.columns([1, 4, 4.5, 0.5], vertical_alignment="center")
        with col1_kiri:
            st.markdown("<p class='tanya-teks'>BAGAIMANA PELAYANAN KAMI?</p>", unsafe_allow_html=True)
        with col1_kanan:
            pelayanan = st.feedback("stars", key="bintang_pelayanan")
        
        col2_space, col2_kiri, col2_kanan, col2_space2 = st.columns([1, 4, 4.5, 0.5], vertical_alignment="center")
        with col2_kiri:
            st.markdown("<p class='tanya-teks'>BAGAIMANA KEBERSIHAN RUANGAN KAMI?</p>", unsafe_allow_html=True)
        with col2_kanan:
            kebersihan = st.feedback("stars", key="bintang_kebersihan")
        
        col3_space, col3_kiri, col3_kanan, col3_space2 = st.columns([1, 4, 4.5, 0.5], vertical_alignment="center")
        with col3_kiri:
            st.markdown("<p class='tanya-teks'>BAGAIMANA KERAMAHAN ADMIN/FO KAMI?</p>", unsafe_allow_html=True)
        with col3_kanan:
            keramahan = st.feedback("stars", key="bintang_keramahan")
            
        st.write("---")
        
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
        with btn_col2:
            if st.button("SUBMIT", use_container_width=True, type="primary"):
                if pelayanan is None or kebersihan is None or keramahan is None:
                    st.warning("⚠️ Mohon lengkapi semua bintang sebelum mengirim.")
                else:
                    # Panggil fungsi loading yang baru kita buat
                    proses_simpan_data(pelayanan, kebersihan, keramahan)

def tampilkan_layar_penutup():
    layar_utama.empty() 
    
    with layar_utama.container():
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 80px; color: #004581;'>✨ TERIMA KASIH! ✨</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #666;'>Penilaian Anda sangat berarti bagi kami.</h2>", unsafe_allow_html=True)
    
    time.sleep(5)
    
    for key in ['bintang_pelayanan', 'bintang_kebersihan', 'bintang_keramahan']:
        if key in st.session_state:
            del st.session_state[key]
            
    st.rerun()

tampilkan_form()
