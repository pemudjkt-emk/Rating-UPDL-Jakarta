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
    return "" # Kembalikan kosong jika file gambar belum diupload

# Memanggil gambar logo
img_danantara = get_image_base64("logo_danantara.png")
img_pln = get_image_base64("logo_pln.png")

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
        transform: scale(3.0); 
        transform-origin: left center;
        margin-left: 50px; 
    }
    div[data-testid="stVerticalBlock"] > div > div {
        margin-bottom: 15px;
    }
    .tanya-teks {
        font-size: 38px; 
        font-weight: 900;
        color: #128c8c; 
        margin-bottom: 0px;
        line-height: 1.1;
        text-transform: uppercase;
        font-family: 'Arial Black', Impact, sans-serif;
    }
    div[data-testid="stButton"] button {
        background-color: #15a5a5 !important; 
        color: white !important;
        font-weight: 900 !important;
        border-radius: 40px !important;
        padding: 10px 30px !important; 
        border: none !important;
        box-shadow: 0 6px 10px rgba(0,0,0,0.15);
        margin-top: 10px !important; 
    }
    div[data-testid="stButton"] button p {
        font-size: 42px !important; 
        font-family: 'Arial Black', Impact, sans-serif !important; 
    }
    
    /* -----------------------------------------------------
       PERUBAHAN DESAIN HEADER: FLEXBOX UNTUK POSISI LOGO 
       ----------------------------------------------------- */
    .header-mockup {
        background-color: #15a5a5;
        padding: 15px 30px; /* Padding kiri-kanan sedikit dilebarkan */
        border-radius: 10px;
        margin-bottom: 30px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        display: flex; /* Mengaktifkan mode sejajar */
        justify-content: space-between; /* Mendorong elemen ke ujung kiri dan kanan */
        align-items: center; /* Memastikan semuanya berada di tengah secara vertikal */
    }
    .header-mockup img {
        height: 70px; /* Tinggi maksimal logo, otomatis menyesuaikan lebarnya */
        object-fit: contain;
    }
    .header-text {
        text-align: center;
        flex-grow: 1; /* Membuat teks mengambil ruang sisa di tengah */
    }
    .header-text h1 {
        color: white;
        font-size: 42px; 
        font-weight: 900;
        font-family: 'Arial Black', Impact, sans-serif; 
        margin: 0;
        line-height: 1.1;
    }
    </style>
""", unsafe_allow_html=True)

layar_utama = st.empty()

def tampilkan_form():
    with layar_utama.container():
        
        # MEMASUKKAN GAMBAR KE DALAM HTML HEADER
        st.markdown(f"""
            <div class='header-mockup'>
                <!-- Logo Kiri -->
                <img src="data:image/png;base64,{img_danantara}" alt="Logo Danantara" onerror="this.style.display='none'">
                
                <!-- Teks Tengah -->
                <div class="header-text">
                    <h1>RATING KEPUASAN PESERTA<br>UPDL JAKARTA</h1>
                </div>
                
                <!-- Logo Kanan -->
                <img src="data:image/png;base64,{img_pln}" alt="Logo PLN" onerror="this.style.display='none'">
            </div>
        """, unsafe_allow_html=True)
        
        # --- BARIS PERTANYAAN 1 ---
        col1_kiri, col1_kanan = st.columns([3, 2], gap="large", vertical_alignment="center")
        with col1_kiri:
            st.markdown("<p class='tanya-teks'>BAGAIMANA PELAYANAN KAMI?</p>", unsafe_allow_html=True)
        with col1_kanan:
            pelayanan = st.feedback("stars", key="bintang_pelayanan")
        
        # --- BARIS PERTANYAAN 2 ---
        col2_kiri, col2_kanan = st.columns([3, 2], gap="large", vertical_alignment="center")
        with col2_kiri:
            st.markdown("<p class='tanya-teks'>BAGAIMANA KEBERSIHAN RUANGAN KAMI?</p>", unsafe_allow_html=True)
        with col2_kanan:
            kebersihan = st.feedback("stars", key="bintang_kebersihan")
        
        # --- BARIS PERTANYAAN 3 ---
        col3_kiri, col3_kanan = st.columns([3, 2], gap="large", vertical_alignment="center")
        with col3_kiri:
            st.markdown("<p class='tanya-teks'>BAGAIMANA KERAMAHAN ADMIN/FO KAMI?</p>", unsafe_allow_html=True)
        with col3_kanan:
            keramahan = st.feedback("stars", key="bintang_keramahan")
            
        st.write("---")
        
        # --- BAGIAN TOMBOL SUBMIT ---
        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
        with btn_col2:
            if st.button("SUBMIT", use_container_width=True, type="primary"):
                if pelayanan is None or kebersihan is None or keramahan is None:
                    st.warning("⚠️ Mohon lengkapi semua bintang sebelum mengirim.")
                else:
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
                        
                        tampilkan_layar_penutup()
                    
                    except Exception as e:
                        st.error(f"⚠️ Gagal menyimpan data. Detail: {e}")

def tampilkan_layar_penutup():
    layar_utama.empty() 
    
    with layar_utama.container():
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 80px; color: #128c8c;'>✨ TERIMA KASIH! ✨</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #666;'>Penilaian Anda sangat berarti bagi kami.</h2>", unsafe_allow_html=True)
    
    time.sleep(5)
    
    for key in ['bintang_pelayanan', 'bintang_kebersihan', 'bintang_keramahan']:
        if key in st.session_state:
            del st.session_state[key]
            
    st.rerun()

tampilkan_form()
