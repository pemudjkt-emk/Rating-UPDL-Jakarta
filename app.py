import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# 1. Pengaturan Tampilan Layar
st.set_page_config(page_title="Rating UPDL Jakarta", layout="centered")

# Membuat "kanvas" kosong agar kita bisa mengganti/menghapus tampilan layar
layar_utama = st.empty()

# Fungsi untuk menampilkan halaman form penilaian
def tampilkan_form():
    with layar_utama.container():
        st.markdown("<h1 style='text-align: center;'>Rating Ruang Kelas UPDL</h1>", unsafe_allow_html=True)
        st.write("---")
        
        # Input bintang murni (tanpa teks angka)
        st.markdown("### Pelayanan")
        pelayanan = st.feedback("stars", key="bintang_pelayanan")
        
        st.markdown("### Kebersihan")
        kebersihan = st.feedback("stars", key="bintang_kebersihan")
        
        st.markdown("### Pembelajaran")
        pembelajaran = st.feedback("stars", key="bintang_pembelajaran")
        
        st.write("---")
        
        # Tombol Kirim
        if st.button("Kirim Rating", use_container_width=True, type="primary"):
            # Memastikan semua bintang sudah diklik (st.feedback bernilai None jika belum diisi)
            if pelayanan is None or kebersihan is None or pembelajaran is None:
                st.warning("⚠️ Mohon isi semua kategori bintang sebelum mengirim.")
            else:
                # Blok try-except ini digunakan agar Anda bisa mencoba tampilan (UI)
                # meskipun Kunci Rahasia Google Sheets belum kita atur
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    df_lama = conn.read()
                    
                    # st.feedback menghitung bintang dari 0 (bintang 1) hingga 4 (bintang 5)
                    # Sehingga kita harus menambahkan + 1 agar datanya benar di Google Sheets
                    data_baru = pd.DataFrame([{
                        "Waktu": pd.Timestamp.now(tz='Asia/Jakarta').strftime('%Y-%m-%d %H:%M:%S'),
                        "Pelayanan": pelayanan + 1,
                        "Kebersihan": kebersihan + 1,
                        "Pembelajaran": pembelajaran + 1
                    }])
                    
                    df_update = pd.concat([df_lama, data_baru], ignore_index=True)
                    conn.update(data=df_update)
                except:
                    pass # Abaikan error koneksi Google untuk sementara
                
                # Memanggil layar terima kasih
                tampilkan_layar_penutup()

# Fungsi untuk menampilkan layar transisi "Terima Kasih"
def tampilkan_layar_penutup():
    # 2. Hapus seluruh form pertanyaan dari layar
    layar_utama.empty() 
    
    # Ganti dengan teks raksasa di tengah layar
    with layar_utama.container():
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; font-size: 70px;'>⭐ TERIMA KASIH! ⭐</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: gray;'>Penilaian Anda sangat berarti bagi kami.</h2>", unsafe_allow_html=True)
    
    # Tahan layar ucapan terima kasih selama 5 detik
    time.sleep(5)
    
    # 3. Hapus ingatan memori bintang peserta sebelumnya
    for key in ['bintang_pelayanan', 'bintang_kebersihan', 'bintang_pembelajaran']:
        if key in st.session_state:
            del st.session_state[key]
            
    # Muat ulang (reload) halaman secara otomatis ke awal
    st.rerun()

# Menjalankan aplikasi
tampilkan_form()
