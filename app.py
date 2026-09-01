import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# 1. Pengaturan Tampilan Layar
st.set_page_config(page_title="Rating UPDL Jakarta", layout="centered")
layar_utama = st.empty()

def tampilkan_form():
    with layar_utama.container():
        st.markdown("<h1 style='text-align: center;'>Rating Ruang Kelas UPDL</h1>", unsafe_allow_html=True)
        st.write("---")
        
        st.markdown("### Pelayanan")
        pelayanan = st.feedback("stars", key="bintang_pelayanan")
        
        st.markdown("### Kebersihan")
        kebersihan = st.feedback("stars", key="bintang_kebersihan")
        
        st.markdown("### Pembelajaran")
        pembelajaran = st.feedback("stars", key="bintang_pembelajaran")
        
        st.write("---")
        
        # Tombol Kirim
        if st.button("Kirim Rating", use_container_width=True, type="primary"):
            if pelayanan is None or kebersihan is None or pembelajaran is None:
                st.warning("⚠️ Mohon isi semua kategori bintang sebelum mengirim.")
            else:
                try:
                    # Menghubungkan ke Google Sheets dengan Secrets
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    df_lama = conn.read()
                    
                    # Membuat baris data baru (+1 karena Streamlit menghitung bintang dari 0)
                    data_baru = pd.DataFrame([{
                        "Waktu": pd.Timestamp.now(tz='Asia/Jakarta').strftime('%Y-%m-%d %H:%M:%S'),
                        "Pelayanan": pelayanan + 1,
                        "Kebersihan": kebersihan + 1,
                        "Pembelajaran": pembelajaran + 1
                    }])
                    
                    # Menyimpan ke Google Sheets
                    df_update = pd.concat([df_lama, data_baru], ignore_index=True)
                    conn.update(data=df_update)
                    
                    # Jika berhasil, panggil layar penutup
                    tampilkan_layar_penutup()
                
                except Exception as e:
                    # Jika gagal (kunci salah/internet putus), tampilkan peringatan
                    st.error(f"⚠️ Gagal menyimpan data. Pastikan konfigurasi rahasia benar. Detail: {e}")

def tampilkan_layar_penutup():
    layar_utama.empty() 
    
    with layar_utama.container():
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 70px;'>⭐ TERIMA KASIH! ⭐</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: gray;'>Penilaian Anda sangat berarti bagi kami.</h2>", unsafe_allow_html=True)
    
    time.sleep(5)
    
    # Menghapus jejak bintang peserta sebelumnya
    for key in ['bintang_pelayanan', 'bintang_kebersihan', 'bintang_pembelajaran']:
        if key in st.session_state:
            del st.session_state[key]
            
    st.rerun()

tampilkan_form()
