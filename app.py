import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# 1. Pengaturan Tampilan Layar Dasar (Menggunakan mode Wide agar lega)
st.set_page_config(page_title="Rating UPDL Jakarta", page_icon="⚡", layout="wide")

# 2. INJEKSI CSS KUSTOM (Menyesuaikan dengan mock-up)
st.markdown("""
    <style>
    /* Background utama */
    .stApp {
        background-color: #f6f8f9;
    }
    
    /* Membesarkan ukuran Bintang */
    div[data-testid="stFeedback"] {
        transform: scale(2.5); /* Memperbesar ukuran bintang 2.5x lipat */
        transform-origin: left center;
        margin-top: 15px;
    }

    /* Styling Teks Pertanyaan */
    .tanya-teks {
        font-size: 32px;
        font-weight: 900;
        color: #128c8c; /* Warna tosca sesuai mock-up */
        margin-bottom: 0px;
        line-height: 1.1;
        text-transform: uppercase;
        font-family: 'Arial Black', Impact, sans-serif;
    }

    /* Styling Tombol Submit */
    div[data-testid="stButton"] button {
        background-color: #15a5a5 !important; /* Warna tosca */
        color: white !important;
        font-weight: 900 !important;
        border-radius: 40px !important;
        padding: 30px 40px !important;
        border: none !important;
        box-shadow: 0 6px 10px rgba(0,0,0,0.15);
    }
    div[data-testid="stButton"] button p {
        font-size: 38px !important; /* Ukuran teks SUBMIT */
    }

    /* Styling Header Custom (Pengganti Sementara Gambar Header) */
    .header-mockup {
        background-color: #15a5a5;
        padding: 25px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 60px;
        margin-top: -30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-mockup h1 {
        color: white;
        font-size: 50px;
        font-weight: 900;
        margin: 0;
        line-height: 1.1;
    }
    </style>
""", unsafe_allow_html=True)

layar_utama = st.empty()

def tampilkan_form():
    with layar_utama.container():
        # --- BAGIAN HEADER ---
        # Catatan: Jika Anda memiliki potongan gambar header aslinya, 
        # hapus st.markdown ini dan ganti dengan: st.image("nama_gambar.png", use_column_width=True)
        st.markdown("""
            <div class='header-mockup'>
                <h1>RATING KEPUASAN PESERTA<br>UPDL JAKARTA</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # --- BAGIAN PERTANYAAN (Layout 2 Kolom) ---
        # Kolom kiri (ukuran 3) untuk teks, kolom kanan (ukuran 2) untuk bintang
        col_kiri, col_kanan = st.columns([3, 2], gap="large")
        
        with col_kiri:
            st.markdown("<p class='tanya-teks'>BAGAIMANA PELAYANAN KAMI?</p>", unsafe_allow_html=True)
            st.write("<br><br>", unsafe_allow_html=True) # Jarak antar pertanyaan
            
            st.markdown("<p class='tanya-teks'>BAGAIMANA KEBERSIHAN RUANGAN KAMI?</p>", unsafe_allow_html=True)
            st.write("<br><br>", unsafe_allow_html=True)
            
            st.markdown("<p class='tanya-teks'>BAGAIMANA KERAMAHAN ADMIN/FO KAMI?</p>", unsafe_allow_html=True)
            st.write("<br><br>", unsafe_allow_html=True)
            
        with col_kanan:
            pelayanan = st.feedback("stars", key="bintang_pelayanan")
            st.write("<br><br><br>", unsafe_allow_html=True)
            
            kebersihan = st.feedback("stars", key="bintang_kebersihan")
            st.write("<br><br><br>", unsafe_allow_html=True)
            
            keramahan = st.feedback("stars", key="bintang_keramahan")
            st.write("<br><br><br>", unsafe_allow_html=True)
            
        st.write("---")
        
        # --- BAGIAN TOMBOL ---
        # Tombol ditaruh di tengah menggunakan trik 3 kolom
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
                            "Keramahan Admin": keramahan + 1 # Sesuaikan dengan nama kolom di Sheets!
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
