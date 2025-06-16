import streamlit as st
import pandas as pd
import random
import math

# ==============================================================================
# Fungsi-Fungsi Inti untuk Algoritma RSA
# ==============================================================================

def is_prime(n, k=5):
    """
    Test primality using Miller-Rabin algorithm.
    Fungsi untuk mengecek apakah sebuah bilangan adalah bilangan prima menggunakan Miller-Rabin.
    """
    if n < 2:
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if n % p == 0:
            return n == p
    s, d = 0, n - 1
    while d % 2 == 0:
        s, d = s + 1, d // 2
    for _ in range(k):
        x = pow(random.randrange(2, n - 1), d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits=8):
    """
    Generate a random prime number with a specified number of bits.
    Fungsi untuk menghasilkan bilangan prima acak dengan jumlah bit tertentu.
    """
    while True:
        p = random.randrange(2**(bits-1), 2**bits)
        if is_prime(p):
            return p

def gcd(a, b):
    """
    Euclidean algorithm for Greatest Common Divisor.
    Fungsi untuk mencari Faktor Persekutuan Terbesar (FPB).
    """
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """
    Extended Euclidean algorithm for modular inverse.
    Fungsi Pembantu untuk mencari invers modular.
    """
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

def mod_inverse(e, phi):
    """
    Calculate modular inverse of e mod phi.
    Fungsi untuk menghitung invers modular.
    """
    d, x, _ = extended_gcd(e, phi)
    if d != 1:
        return None  # inverse does not exist
    return x % phi

def rsa_encrypt(data, e, n):
    """
    Encrypts a list of numbers using RSA.
    Fungsi untuk mengenkripsi daftar angka.
    """
    return [pow(int(num), e, n) for num in data]

def rsa_decrypt(data, d, n):
    """
    Decrypts a list of numbers using RSA.
    Fungsi untuk mendekripsi daftar angka.
    """
    return [pow(int(num), d, n) for num in data]

# ==============================================================================
# Fungsi-Fungsi Pembantu untuk UI Streamlit
# ==============================================================================

def validate_numeric_csv(df):
    """
    Checks if all data in the dataframe (except header) are integers.
    Fungsi untuk memvalidasi bahwa semua data dalam CSV adalah numerik (bilangan bulat).
    """
    for col in df.columns:
        # Coba konversi ke numerik, error akan menjadi NaN
        series = pd.to_numeric(df[col], errors='coerce')
        # Cek jika ada NaN (bukan angka) atau jika angka tersebut bukan integer
        if series.isnull().any() or not all(series.apply(lambda x: float(x).is_integer())):
            return False
    return True

def get_keys(p, q):
    """
    Generates a list of possible public (e) and private (d) keys.
    Fungsi untuk menghasilkan daftar pasangan kunci publik dan privat yang valid.
    """
    n = p * q
    phi_n = (p - 1) * (q - 1)
    keys = []
    # Kita batasi pencarian untuk efisiensi di aplikasi web
    limit = min(phi_n, 1000) 
    for e in range(2, limit):
        if gcd(e, phi_n) == 1:
            d = mod_inverse(e, phi_n)
            if d is not None:
                keys.append({'e': e, 'd': d})
    return pd.DataFrame(keys)

def reset_state():
    """
    Resets the session state to the beginning.
    Fungsi untuk mereset aplikasi kembali ke halaman awal.
    """
    # Simpan file yang sudah di-upload jika ada
    uploaded_file = st.session_state.get('uploaded_file', None)
    
    # Hapus semua state kecuali file yang di-upload
    for key in list(st.session_state.keys()):
        if key != 'uploaded_file':
            del st.session_state[key]
    
    # Jika file ada, proses ulang
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        try:
            df = pd.read_csv(st.session_state.uploaded_file)
            if validate_numeric_csv(df):
                st.session_state.df_valid = True
                st.session_state.df = df
            else:
                st.session_state.df_valid = False
        except Exception as e:
            st.session_state.df_valid = False


# ==============================================================================
# Tampilan dan Logika Aplikasi Streamlit
# ==============================================================================

st.set_page_config(page_title="CrypterNann-RSA", layout="wide")

st.title("🔒 CrypterNann-RSA")
st.write("Aplikasi untuk Enkripsi dan Dekripsi Kumpulan Data Numerik Menggunakan RSA")
st.markdown("---")


# Inisialisasi session state jika belum ada
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Fungsi untuk mengubah halaman
def set_page(page_name):
    st.session_state.page = page_name

# --- Halaman Awal & Upload Data ---
if st.session_state.page == 'home':
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("Mulai di Sini")
        st.write("Upload file CSV Anda yang berisi data numerik. Pastikan semua nilai adalah bilangan bulat.")
        uploaded_file = st.file_uploader("Pilih file CSV", type="csv", key="file_uploader_key")

        if uploaded_file is not None:
            st.session_state.uploaded_file = uploaded_file
            try:
                df = pd.read_csv(uploaded_file)
                if validate_numeric_csv(df):
                    st.success("File valid! Silakan pilih tindakan di bawah ini.")
                    st.session_state.df_valid = True
                    st.session_state.df = df
                    st.dataframe(df.head())
                else:
                    st.error("File tidak valid. Pastikan semua data (selain header) adalah bilangan bulat.")
                    st.session_state.df_valid = False
            except Exception as e:
                st.error(f"Gagal memproses file: {e}")
                st.session_state.df_valid = False
        
        # Tombol aksi hanya muncul jika file valid
        if st.session_state.get('df_valid', False):
            action_col1, action_col2 = st.columns(2)
            with action_col1:
                if st.button("🔐 Enkripsi Data", use_container_width=True, type="primary"):
                    set_page('encrypt_primes')
                    st.rerun() # Memuat ulang script untuk pindah halaman
            with action_col2:
                if st.button("🔓 Dekripsi Data", use_container_width=True):
                    set_page('decrypt_input')
                    st.rerun()
    
    with col2:
        with st.expander("Petunjuk Pemakaian", expanded=True):
            st.markdown("""
            1.  **Upload File**: Unggah file `.csv` yang berisi data numerik.
            2.  **Pilih Aksi**: Klik tombol "Enkripsi" atau "Dekripsi".
            3.  **Untuk Enkripsi**:
                - Masukkan dua bilangan prima (`p` dan `q`) atau gunakan tombol acak.
                - Pilih salah satu kunci publik (`e`) dari tabel yang ditampilkan.
                - Klik "Encrypt!" untuk melihat hasilnya.
            4.  **Untuk Dekripsi**:
                - Masukkan nilai `n` dan kunci dekripsi privat (`d`).
                - Klik "Decrypt!" untuk melihat hasilnya.
            5.  Gunakan tombol "Kembali" atau "Batal" untuk mengulang langkah.
            """)
        with st.expander("Contoh Pemakaian"):
            st.info("Contoh alur enkripsi:")
            st.markdown("""
            - Anda upload data: `10, 25, 50`.
            - Anda memilih `p=11` dan `q=13`. Maka `n=143` dan `phi(n)=120`.
            - Tabel kunci akan muncul. Anda pilih indeks `e=7` dan `d=103`.
            - Data terenkripsi menjadi: `(10^7) mod 143 = 59`, `(25^7) mod 143 = 60`, `(50^7) mod 143 = 5`.
            """)


# --- Alur Enkripsi ---
elif st.session_state.page == 'encrypt_primes':
    st.header("Langkah 1: Tentukan Bilangan Prima")
    st.info("Masukkan dua bilangan prima berbeda atau biarkan kami yang memilihkan untuk Anda.")

    form = st.form(key="prime_form")
    col1, col2 = form.columns(2)
    with col1:
        p = form.number_input("Masukkan bilangan prima (p)", min_value=2, step=1, format="%d")
    with col2:
        q = form.number_input("Masukkan bilangan prima (q)", min_value=2, step=1, format="%d")
    
    col_b1, col_b2 = form.columns([1,1])
    submitted = col_b1.form_submit_button("Lanjutkan")
    random_clicked = col_b2.form_submit_button("Gunakan Bilangan Prima Acak")
    
    if submitted:
        if p == q:
            st.error("Bilangan p dan q tidak boleh sama.")
        elif not is_prime(p) or not is_prime(q):
            st.error("Salah satu atau kedua bilangan yang Anda masukkan bukan bilangan prima.")
        else:
            st.session_state.p = p
            st.session_state.q = q
            set_page('encrypt_keys')
            st.rerun()

    if random_clicked:
        st.session_state.p = generate_prime(bits=10)
        st.session_state.q = generate_prime(bits=10)
        while st.session_state.p == st.session_state.q:
            st.session_state.q = generate_prime(bits=10)
        set_page('encrypt_keys')
        st.rerun()
    
    if st.button("Kembali ke Halaman Awal"):
        reset_state()
        set_page('home')
        st.rerun()


elif st.session_state.page == 'encrypt_keys':
    p, q = st.session_state.p, st.session_state.q
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    st.header("Langkah 2: Pilih Kunci Enkripsi")
    st.write(f"Parameter Anda: `p = {p}`, `q = {q}`, `n = {n}`, `phi(n) = {phi_n}`")

    with st.spinner("Menghasilkan daftar kunci yang valid..."):
        keys_df = get_keys(p, q)
        st.session_state.keys_df = keys_df

    st.write("Berikut adalah semua kemungkinan kunci publik (e) dan privat (d) yang bisa digunakan.")
    
    # Pagination
    page_size = 25
    total_pages = math.ceil(len(keys_df) / page_size)
    page_num = st.number_input('Halaman', min_value=1, max_value=total_pages, value=1, step=1)
    
    start_idx = (page_num - 1) * page_size
    end_idx = start_idx + page_size
    st.table(keys_df.iloc[start_idx:end_idx])

    st.write("Pilih salah satu kunci untuk mengenkripsi data Anda dengan memasukkan nomor indeksnya.")
    selected_index = st.number_input("Pilih Indeks Kunci", min_value=0, max_value=len(keys_df)-1, step=1)
    
    st.session_state.selected_e = keys_df.iloc[selected_index]['e']
    st.session_state.selected_d = keys_df.iloc[selected_index]['d']
    st.session_state.n = n

    st.info(f"Anda memilih kunci publik `e = {st.session_state.selected_e}`.")

    col1, col2 = st.columns(2)
    if col1.button("🔐 Encrypt!", type="primary"):
        set_page('encrypt_result')
        st.rerun()
    if col2.button("Batalkan & Pilih Ulang Bilangan Prima"):
        set_page('encrypt_primes')
        st.rerun()


elif st.session_state.page == 'encrypt_result':
    st.header("Hasil Enkripsi")
    df = st.session_state.df
    e = st.session_state.selected_e
    d = st.session_state.selected_d
    n = st.session_state.n
    
    encrypted_df = df.copy()
    with st.spinner("Sedang mengenkripsi data..."):
        for col in encrypted_df.columns:
            encrypted_df[col] = rsa_encrypt(encrypted_df[col], e, n)
    
    st.success("Data berhasil dienkripsi!")
    st.write("Data Terenkripsi:")
    st.dataframe(encrypted_df)
    
    st.info(f"**Kunci Publik (e, n):** ({e}, {n})")
    st.warning(f"**Kunci Privat (d, n):** ({d}, {n}) - Simpan kunci ini untuk proses dekripsi!")
    
    if st.button("Kembali ke Halaman Awal"):
        reset_state()
        set_page('home')
        st.rerun()

# --- Alur Dekripsi ---
elif st.session_state.page == 'decrypt_input':
    st.header("Langkah 1: Masukkan Kunci Dekripsi")
    st.info("Masukkan nilai n (hasil p * q) dan kunci privat (d) Anda.")
    
    with st.form(key="decrypt_form"):
        n_decrypt = st.number_input("Masukkan nilai n", min_value=1, step=1, format="%d")
        d_decrypt = st.number_input("Masukkan kunci privat (d)", min_value=1, step=1, format="%d")

        col1, col2 = st.columns(2)
        decrypt_button = col1.form_submit_button("🔓 Dekripsi Data", type="primary")
        cancel_button = col2.form_submit_button("Batalkan")

        if decrypt_button:
            if n_decrypt > 0 and d_decrypt > 0:
                st.session_state.n_decrypt = n_decrypt
                st.session_state.d_decrypt = d_decrypt
                set_page('decrypt_result')
                st.rerun()
            else:
                st.error("Nilai n dan d harus lebih besar dari 0.")
        if cancel_button:
            reset_state()
            set_page('home')
            st.rerun()
            
    if st.button("Kembali ke Halaman Awal"):
        reset_state()
        set_page('home')
        st.rerun()
        

elif st.session_state.page == 'decrypt_result':
    st.header("Hasil Dekripsi")
    df = st.session_state.df
    n = st.session_state.n_decrypt
    d = st.session_state.d_decrypt

    decrypted_df = df.copy()
    try:
        with st.spinner("Sedang mendekripsi data..."):
            for col in decrypted_df.columns:
                decrypted_df[col] = rsa_decrypt(decrypted_df[col], d, n)
        
        st.success("Data berhasil didekripsi!")
        st.write("Data Asli:")
        st.dataframe(decrypted_df)
    except Exception as e:
        st.error(f"Gagal mendekripsi data. Pastikan kunci yang Anda masukkan benar. Error: {e}")

    if st.button("Kembali ke Halaman Awal"):
        reset_state()
        set_page('home')
        st.rerun()
