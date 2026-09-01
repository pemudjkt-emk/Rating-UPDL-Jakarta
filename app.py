import streamlit as st
import sqlite3
import time

# 1. Konfigurasi Database SQLite
conn = sqlite3.connect('rating_updl.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS ratings
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              pelayanan INTEGER,
              kebersihan INTEGER,
              pembelajaran INTEGER,
              waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# 2. Pengaturan Tampilan Layar (UI)
st.set_page_config(page_title="Rating UPDL Jakarta", layout="centered")
st.markdown("<h1 style='text-align: center;'>Rating Ruang Kelas UPDL</h1>", unsafe_allow_html=True)
st.write("---")

# Fungsi untuk mengubah angka menjadi deretan emoji bintang
def format_stars(val):
    return "⭐" * val

# 3. Input Bintang menggunakan fitur bawaan Streamlit
st.subheader("Pelayanan")
pelayanan = st.radio("Pelayanan", options=[1, 2, 3, 4, 5], index=None, format_func=format_stars, horizontal=True, label_visibility="collapsed")

st.subheader("Kebersihan")
kebersihan = st.radio("Kebersihan", options=[1, 2, 3, 4, 5], index=None, format_func=format_stars, horizontal=True, label_visibility="collapsed")

st.subheader("Pembelajaran")
pembelajaran = st.radio("Pembelajaran", options=[1, 2, 3, 4, 5], index=None, format_func=format_stars, horizontal=True, label_visibility="collapsed")

st.write("---")

# 4. Logika Tombol Kirim & Auto-Reload
if st.button("Kirim Rating", use_container_width=True, type="primary"):
    if pelayanan is None or kebersihan is None or pembelajaran is None:
        st.warning("⚠️ Mohon isi semua rating sebelum mengirim.")
    else:
        # Simpan data ke database
        c.execute("INSERT INTO ratings (pelayanan, kebersihan, pembelajaran) VALUES (?, ?, ?)",
                  (pelayanan, kebersihan, pembelajaran))
        conn.commit()
        
        # Tampilkan pesan sukses lalu auto-reload
        st.success("✅ Terima kasih atas penilaian Anda! Data berhasil disimpan.")
        time.sleep(2)  # Jeda 2 detik
        st.rerun()     # Me-reset tampilan ke awal