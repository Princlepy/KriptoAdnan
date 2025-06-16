# 🔒 CrypterNann-RSA

**CrypterNann-RSA** adalah sebuah aplikasi web interaktif yang dirancang untuk mendemonstrasikan proses enkripsi dan dekripsi data numerik menggunakan algoritma kriptografi RSA. Aplikasi ini dibangun dengan Streamlit, memberikan antarmuka yang ramah pengguna untuk mengamankan kumpulan data yang tersimpan dalam format file `.csv`.

[![Tampilan Aplikasi CrypterNann-RSA](https://placehold.co/800x450/2E3B4E/FFFFFF?text=Tampilan+Aplikasi+CrypterNann-RSA)](https://github.com/username/crypternann-rsa)
*Gambar: Tampilan antarmuka aplikasi CrypterNann-RSA.*

---

## ✨ Fitur Utama

-   **Enkripsi Data**: Mengenkripsi seluruh data numerik dalam file CSV yang diunggah.
-   **Dekripsi Data**: Mendekripsi data yang sebelumnya dienkripsi menggunakan kunci privat yang sesuai.
-   **Pembuatan Kunci Fleksibel**:
    -   **Manual**: Pengguna dapat memasukkan dua bilangan prima (`p` dan `q`) secara manual.
    -   **Otomatis**: Aplikasi dapat menghasilkan pasangan bilangan prima acak secara otomatis.
-   **Pemilihan Kunci Interaktif**: Menampilkan daftar kunci publik (`e`) dan kunci privat (`d`) yang valid dalam format tabel yang mudah dibaca dan dilengkapi paginasi.
-   **Validasi Input**: Secara otomatis memeriksa apakah file yang diunggah berisi data numerik yang valid sebelum melanjutkan proses.
-   **Antarmuka Pengguna Intuitif**: Dilengkapi dengan petunjuk pemakaian, contoh, dan alur kerja yang jelas untuk setiap langkah.
-   **Edukasi**: Memberikan pemahaman praktis tentang cara kerja algoritma RSA dalam mengamankan data.

---

## 🚀 Instalasi dan Menjalankan Aplikasi

Untuk menjalankan aplikasi ini di lingkungan lokal Anda, ikuti langkah-langkah berikut:

**1. Clone Repositori**

```bash
git clone [https://github.com/username/crypternann-rsa.git](https://github.com/username/crypternann-rsa.git) # Ganti dengan URL repo Anda
cd crypternann-rsa
```

**2. Instal Dependensi**

Pastikan Anda memiliki Python 3.7+ terinstal. Kemudian instal library yang dibutuhkan.

```bash
pip install streamlit pandas
```
*(Opsional: Anda bisa membuat file `requirements.txt` yang berisi `streamlit` dan `pandas`, lalu jalankan `pip install -r requirements.txt`)*

**3. Jalankan Aplikasi Streamlit**

Buka terminal Anda, arahkan ke direktori proyek, dan jalankan perintah berikut:

```bash
streamlit run app.py
```

Aplikasi akan otomatis terbuka di browser default Anda.

---

## 📝 Cara Penggunaan

Aplikasi ini memiliki dua alur kerja utama: Enkripsi dan Dekripsi.

### 🔐 Alur Enkripsi

1.  **Upload File**: Pada halaman utama, klik area "Pilih file CSV" untuk mengunggah file `.csv` yang berisi data numerik Anda. Aplikasi akan memvalidasi file tersebut.
2.  **Mulai Enkripsi**: Setelah file terverifikasi, klik tombol **"Enkripsi Data"**.
3.  **Tentukan Bilangan Prima**:
    -   **Manual**: Masukkan dua bilangan prima `p` dan `q` yang berbeda, lalu klik "Lanjutkan".
    -   **Otomatis**: Klik tombol **"Gunakan Bilangan Prima Acak"** untuk menghasilkan `p` dan `q` secara otomatis.
4.  **Pilih Kunci Publik**: Aplikasi akan menampilkan tabel berisi pasangan kunci publik (`e`) dan privat (`d`) yang valid. Pilih salah satu kunci dengan memasukkan nomor **indeks** yang diinginkan.
5.  **Proses Enkripsi**: Klik tombol **"Encrypt!"**.
6.  **Lihat Hasil**: Aplikasi akan menampilkan tabel berisi data yang sudah terenkripsi.
7.  **Simpan Kunci!**: **PENTING!** Catat dan simpan **Kunci Privat (`d`)** dan nilai **`n`** yang ditampilkan. Anda akan membutuhkan kedua nilai ini untuk proses dekripsi.

### 🔓 Alur Dekripsi

1.  **Upload File**: Unggah file `.csv` yang berisi data yang sudah terenkripsi.
2.  **Mulai Dekripsi**: Klik tombol **"Dekripsi Data"**.
3.  **Masukkan Kunci Privat**: Masukkan nilai `n` dan kunci privat `d` yang telah Anda simpan dari proses enkripsi.
4.  **Proses Dekripsi**: Klik tombol **"Decrypt!"**.
5.  **Lihat Hasil**: Aplikasi akan menampilkan data asli Anda yang telah berhasil didekripsi.

---

## 🛠️ Dibangun Dengan

-   **Python**: Bahasa pemrograman utama.
-   **Streamlit**: Framework untuk membangun aplikasi web interaktif.
-   **Pandas**: Untuk manipulasi dan pengolahan data dari file CSV.
-   **Algoritma RSA**: Implementasi dasar dari algoritma kriptografi kunci publik RSA.

---

Dibuat dengan cinta untuk keamanan data. ❤️
