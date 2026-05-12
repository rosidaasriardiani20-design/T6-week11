# Tugas-5 Week 11 - Post Manager (Threading & REST API)

Aplikasi desktop berbasis Python (Tkinter) untuk mengelola data postingan menggunakan layanan REST API. Aplikasi ini menerapkan konsep multi-threading untuk memastikan UI tetap responsif (tidak freeze) saat melakukan permintaan jaringan.

## Identitas Mahasiswa
- **Nama**: Rosida Asri Ardiani
- **NIM**: F1D02410142
- **Kelas**: Pemrograman Visual C

## Fitur Utama
Aplikasi ini telah memenuhi kriteria rubrik penilaian sebagai berikut:
1. **CRUD Lengkap**: Implementasi metode HTTP GET (tampil data), POST (tambah), PUT (edit), dan DELETE (hapus).
2. **Multi-threading**: Semua aktivitas network request berjalan di thread terpisah menggunakan kelas `ApiWorker`.
3. **State & Error Handling**: Menampilkan status loading ("Processing request") dan menangani error (seperti Server 503 atau duplikasi slug) tanpa membuat aplikasi crash.
4. **UI Responsif**: Menggunakan elemen `Treeview` untuk tabel dan form input yang dinamis.

## Hasil Screenshot Aplikasi

### 1. Tampilan Utama (GET Data)
Menampilkan daftar postingan yang diambil dari API ke dalam tabel.
![Tampilan Utama](screenshots/main_display.png)

### 2. Form Input & Tambah Data (POST)
Proses pengisian data lengkap (Title, Author, Slug, Status, Body) sebelum dikirim ke server.
![Form Input](screenshots/post_data.png)

### 3. Konfirmasi Hapus (DELETE)
Fitur dialog konfirmasi untuk mencegah penghapusan data secara tidak sengaja (Cascade Delete).
![Konfirmasi Hapus](screenshots/delete_confirm.png)

### 4. Fitur Edit Data (PUT)
Melakukan perubahan pada data yang sudah ada di server dengan memilih baris pada tabel terlebih dahulu.
![Edit Data](screenshots/put_data.png)

## Cara Menjalankan
1. Pastikan Python sudah terinstal.
2. Instal library yang dibutuhkan:
   ```bash
   pip install requests