import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# 1. Pengaturan Tampilan Layar Dasar
st.set_page_config(page_title="Rating UPDL Jakarta", page_icon="🌟", layout="centered")

# 2. INJEKSI CSS KUSTOM (Untuk Mempercantik Tampilan)
st.markdown("""
    <style>
    /* Mengubah warna latar belakang aplikasi menjadi abu-abu sangat muda */
    .stApp {
        background-color: #f4f7f6;
    }
    /* Desain Banner/Header Utama */
    .header-box {
        background: linear-gradient(135deg, #0052D4, #4364F7, #6FB1FC);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        margin-bottom: 40px;
        margin-top: 20px;
    }
    /* Desain Teks Pertanyaan */
    .kategori-teks {
        font-size: 22px;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: -15px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Membuat "kanvas" kosong untuk transisi layar
layar_utama = st.empty()

def tampilkan_form():
    with layar_utama.container():
        # Menampilkan Banner Header
        st.markdown("""
            <div class='header-box'>
                <h1 style='color: white; margin-bottom: 5px; font-size: 36px;'>🏢 Penilaian Ruang Kelas</h1>
                <p style='font-size: 18px; margin-top: 0px;'>UPDL Jakarta</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Menggunakan kolom agar form berada di tengah layar
        # Angka [1, 4, 1] berarti sisi kiri-kanan lebih kecil, tengah lebih besar
        col1, col2, col3 = st.columns([1, 4, 1])
        
        with col2:
            st.markdown("<p class='kategori-teks'>👨‍💼 Bagaimana Pelayanan kami?</p>", unsafe_allow_html=True)
            pelayanan = st.feedback("stars", key="bintang_pelayanan")
            st.write("") # Spasi kosong
            
            st.markdown("<p class='kategori-teks'>🧹 Bagaimana Kebersihan ruangan?</p>", unsafe_allow_html=True)
            kebersihan = st.feedback("stars", key="bintang_kebersihan")
            st.write("")
            
            st.markdown("<p class='kategori-teks'>📚 Bagaimana Kualitas Pembelajaran?</p>", unsafe_allow_html=True)
            pembelajaran = st.feedback("stars", key="bintang_pembelajaran")
            
            st.write("---")
            
            # Tombol Kirim yang lebih menarik
            if st.button("Kirim Penilaian 🚀", use_container_width=True, type="primary"):
                if pelayanan is None or kebersihan is None or pembelajaran is None:
                    st.warning("⚠️ Mohon lengkapi semua bintang sebelum mengirim.")
                else:
                    try:
                        conn = st.connection("gsheets", type=GSheetsConnection)
                        df_lama = conn.read()
                        
                        data_baru = pd.DataFrame([{
                            "Waktu": pd.Timestamp.now(tz='Asia/Jakarta').strftime('%Y-%m-%d %H:%M:%S'),
                            "Pelayanan": pelayanan + 1,
                            "Kebersihan": kebersihan + 1,
                            "Pembelajaran": pembelajaran + 1
                        }])
                        
                        df_update = pd.concat([df_lama, data_baru], ignore_index=True)
                        conn.update(data=df_update)
                        
                        tampilkan_layar_penutup()
                    
                    except Exception as e:
                        st.error(f"⚠️ Gagal menyimpan data. Detail: {e}")

def tampilkan_layar_penutup():
    layar_utama.empty() 
    
    with layar_utama.container():
        # Memberikan spasi kosong ke bawah agar teks berada di tengah layar
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 80px;'>✨ TERIMA KASIH! ✨</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #4364F7;'>Penilaian Anda membantu kami meningkatkan kualitas UPDL Jakarta.</h3>", unsafe_allow_html=True)
    
    time.sleep(5)
    
    for key in ['bintang_pelayanan', 'bintang_kebersihan', 'bintang_pembelajaran']:
        if key in st.session_state:
            del st.session_state[key]
            
    st.rerun()

# Memulai aplikasi
tampilkan_form()
