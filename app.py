import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time
import base64
import os

# Pengaturan Tampilan Layar (Wide Mode)
st.set_page_config(page_title="Rating UPDL Jakarta", page_icon="⚡", layout="wide")

# --- INISIALISASI TAHAPAN ---
if 'sesi_id' not in st.session_state:
    st.session_state.sesi_id = 0
if 'tahap' not in st.session_state:
    st.session_state.tahap = 'form'
if 'data_temp' not in st.session_state:
    st.session_state.data_temp = {}

def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return "" 

img_danantara = get_image_base64("logo_danantara.png")
img_pln = get_image_base64("Logo_PLN.svg.png")
img_updl = get_image_base64("logo_updl.png")

# INJEKSI CSS KUSTOM
st.markdown("""
<style>
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 0.5rem !important; /* Ditekan agar bagian bawah lebih lega */
}
.stApp {
    background: #ffffff !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 1) !important; 
    border-radius: 25px !important; 
    border: 1px solid #e0e0e0 !important; 
    padding: 25px 30px !important;
    box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.05) !important; 
}
/* UKURAN BINTANG DIPERBESAR */
div[data-testid="stFeedback"] {
    transform: scale(8.5); 
    transform-origin: left center;
    margin-left: 10px; 
}
/* JARAK ANTAR BARIS DIRAPATKAN AGAR MUAT */
div[data-testid="stVerticalBlock"] > div > div {
    margin-bottom: 10px; 
}
/* UKURAN TEKS DIPERBESAR */
.tanya-teks {
    font-size: 60px !important; 
    font-weight: 900 !important;
    color: #1a6bb8 !important; 
    margin-bottom: 0px !important;
    line-height: 1.1 !important;
    text-transform: uppercase !important;
    font-family: 'Arial Black', Impact, sans-serif !important;
}
/* TOMBOL SUBMIT DITARIK KE ATAS */
div[data-testid="stButton"] button {
    background-color: #004581 !important; 
    color: white !important;
    font-weight: 900 !important;
    border-radius: 40px !important;
    padding: 10px 30px !important; 
    border: none !important;
    box-shadow: 0 6px 10px rgba(0,0,0,0.15);
    margin-top: 6px !important; /* Mengurangi jarak dengan pertanyaan terakhir */
}
div[data-testid="stButton"] button p {
    font-size: 42px !important; 
    font-family: 'Arial Black', Impact, sans-serif !important; 
}
.header-mockup {
    background-color: #004581; 
    padding: 15px 30px; 
    border-radius: 10px;
    margin-bottom: 25px; /* Jarak bawah header sedikit diperkecil */
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
}
.logo-danantara {
    height: 105px; 
    object-fit: contain;
}
.logo-group-right {
    display: flex;
    align-items: center;
    gap: 25px; 
}
.logo-updl {
    height: 100px; 
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
.animasi-loading {
    border: 16px solid #f3f3f3; 
    border-radius: 50%;
    border-top: 16px solid #15a5a5; 
    border-bottom: 16px solid #004581; 
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


# ==========================================
# TAHAP 1: MENAMPILKAN FORM RATING
# ==========================================
if st.session_state.tahap == 'form':
    
    st.markdown(f"""
<div class='header-mockup'>
<img class="logo-danantara" src="data:image/png;base64,{img_danantara}" alt="Logo Danantara" onerror="this.style.display='none'">
<div class="header-text">
<h1>RATING KEPUASAN PESERTA<br>UPDL JAKARTA</h1>
</div>
<div class="logo-group-right">
<img class="logo-updl" src="data:image/png;base64,{img_updl}" alt="Logo UPDL" onerror="this.style.display='none'">
<img class="logo-pln" src="data:image/png;base64,{img_pln}" alt="Logo PLN" onerror="this.style.display='none'">
</div>
</div>
    """, unsafe_allow_html=True)
    
    with st.container(border=True):
        # 1. Security
        col1_space, col1_kiri, col1_kanan, col1_space2 = st.columns([1, 4, 4.5, 0.5], vertical_alignment="center")
        with col1_kiri:
            st.markdown("<p class='tanya-teks'>HOSPITALITY (KERAMAHAN) SECURITY?</p>", unsafe_allow_html=True)
        with col1_kanan:
            sec = st.feedback("stars", key=f"bintang_sec_{st.session_state.sesi_id}")
        
        # 2. Admin Kelas
        col2_space, col2_kiri, col2_kanan, col2_space2 = st.columns([1, 4, 4.5, 0.5], vertical_alignment="center")
        with col2_kiri:
            st.markdown("<p class='tanya-teks'>HOSPITALITY (KERAMAHAN) ADMIN KELAS?</p>", unsafe_allow_html=True)
        with col2_kanan:
            admin = st.feedback("stars", key=f"bintang_admin_{st.session_state.sesi_id}")
        
        # 3. Front Office
        col3_space, col3_kiri, col3_kanan, col3_space2 = st.columns([1, 4, 4.5, 0.5], vertical_alignment="center")
        with col3_kiri:
            st.markdown("<p class='tanya-teks'>HOSPITALITY (KERAMAHAN) FRONT OFFICE?</p>", unsafe_allow_html=True)
        with col3_kanan:
            fo = st.feedback("stars", key=f"bintang_fo_{st.session_state.sesi_id}")
            
        # 4. Kebersihan
        col4_space, col4_kiri, col4_kanan, col4_space2 = st.columns([1, 4, 4.5, 0.5], vertical_alignment="center")
        with col4_kiri:
            st.markdown("<p class='tanya-teks'>KEBERSIHAN RUANGAN DAN FASILITAS?</p>", unsafe_allow_html=True)
        with col4_kanan:
            kebersihan = st.feedback("stars", key=f"bintang_kebersihan_{st.session_state.sesi_id}")
            
        # 5. Pelayanan Keseluruhan
        col5_space, col5_kiri, col5_kanan, col5_space2 = st.columns([1, 4, 4.5, 0.5], vertical_alignment="center")
        with col5_kiri:
            st.markdown("<p class='tanya-teks'>PELAYANAN UPDL KESELURUHAN?</p>", unsafe_allow_html=True)
        with col5_kanan:
            pelayanan = st.feedback("stars", key=f"bintang_pelayanan_{st.session_state.sesi_id}")
        
    # PERUBAHAN: Menghapus st.write("---") yang memakan banyak ruang vertikal
    
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    with btn_col2:
        if st.button("SUBMIT", use_container_width=True, type="primary"):
            if sec is None or admin is None or fo is None or kebersihan is None or pelayanan is None:
                st.warning("⚠️ Mohon lengkapi ke-5 bintang sebelum mengirim.")
            else:
                st.session_state.data_temp = {
                    "sec": sec,
                    "admin": admin,
                    "fo": fo,
                    "kebersihan": kebersihan,
                    "pelayanan": pelayanan
                }
                st.session_state.tahap = 'loading'
                st.rerun()

# ==========================================
# TAHAP 2: PROSES LOADING DAN SIMPAN DATA
# ==========================================
elif st.session_state.tahap == 'loading':
    
    st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<div class='animasi-loading'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 50px; color: #004581; margin-top: 30px;'>⏳ Sedang Menyimpan Data...</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #666;'>Mohon tunggu sebentar</h3>", unsafe_allow_html=True)
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_lama = conn.read(ttl=0)
        
        data_baru = pd.DataFrame([{
            "Waktu": pd.Timestamp.now(tz='Asia/Jakarta').strftime('%Y-%m-%d %H:%M:%S'),
            "Hospitality Security": st.session_state.data_temp["sec"] + 1,
            "Hospitality Admin": st.session_state.data_temp["admin"] + 1,
            "Hospitality FO": st.session_state.data_temp["fo"] + 1,
            "Kebersihan": st.session_state.data_temp["kebersihan"] + 1,
            "Pelayanan Keseluruhan": st.session_state.data_temp["pelayanan"] + 1
        }])
        
        df_update = pd.concat([df_lama, data_baru], ignore_index=True)
        conn.update(data=df_update)
        
        st.session_state.tahap = 'sukses'
        st.rerun()
        
    except Exception as e:
        st.error(f"⚠️ Gagal menyimpan data. Pastikan koneksi internet stabil. Detail: {e}")
        time.sleep(4)
        st.session_state.tahap = 'form'
        st.rerun()


# ==========================================
# TAHAP 3: LAYAR TERIMA KASIH & RESET
# ==========================================
elif st.session_state.tahap == 'sukses':
    
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 80px; color: #004581;'>✨ TERIMA KASIH! ✨</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #666;'>Penilaian Anda sangat berarti bagi kami.</h2>", unsafe_allow_html=True)
    
    time.sleep(5)
    
    st.session_state.sesi_id += 1
    st.session_state.tahap = 'form'
    st.rerun()
