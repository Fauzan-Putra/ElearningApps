# Aksanta - E-Learning Platform

## Overview
Aksanta adalah platform e-learning yang dirancang untuk memfasilitasi aktivitas pendidikan antara guru dan siswa. Platform ini memungkinkan guru untuk mengelola artikel dan kuis, sementara siswa dapat bergabung dengan kelas, membaca artikel, mengikuti kuis, dan meninjau kemajuan mereka. Aplikasi ini dibangun menggunakan Python dengan antarmuka pengguna grafis (GUI) yang didukung oleh Tkinter, dan menggunakan file CSV untuk penyimpanan data.

## Features
- **Autentikasi Pengguna**:
  - Pendaftaran untuk guru dan siswa.
  - Sistem login dengan hashing kata sandi.
- **Manajemen Kelas**:
  - Guru membuat kelas dengan kode unik.
  - Siswa bergabung dengan kelas menggunakan kode tersebut.
- **Manajemen Artikel**:
  - Guru dapat membuat, mengedit, dan menghapus artikel.
  - Artikel mendukung konten teks dan gambar.
- **Manajemen Kuis**:
  - Guru dapat membuat paket kuis dengan beberapa pertanyaan.
  - Setiap kuis memiliki pengatur waktu total.
  - Pertanyaan memiliki pilihan ganda, jawaban benar, dan penjelasan.
- **Aktivitas Siswa**:
  - Membaca artikel dengan konten yang kaya.
  - Mengikuti kuis dengan batas waktu.
  - Meninjau riwayat kuis dengan umpan balik terperinci.
- **Pelacakan Kemajuan**:
  - Pencatatan percobaan kuis dan skor.
  - Guru dapat melihat statistik seperti skor rata-rata dan tingkat penyelesaian kuis.

## Installation

### Prerequisites
- Python 3.6 atau yang lebih baru
- Pustaka Python yang diperlukan:
  - `tkinter` (biasanya disertakan dengan Python)
  - `pillow` (untuk penanganan gambar)
  - `matplotlib` (untuk grafik statistik)

Instal pustaka yang diperlukan menggunakan pip:
```bash
pip install pillow matplotlib
