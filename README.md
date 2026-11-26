<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/brand/ossa-wordmark-dark.png">
    <img src="docs/brand/ossa-wordmark.png" alt="OSSA" width="280">
  </picture>
</p>

<h1 align="center">Corporate Security Incident Tracker</h1>

<p align="center">Proyek Komputasi Awan Week 12 di AWS Academy</p>

<p align="center">
  <a href="#arsitektur">Arsitektur</a>&emsp;
  <a href="#bukti-pengujian-aws">Bukti AWS</a>&emsp;
  <a href="#kontrak-api">Kontrak API</a>&emsp;
  <a href="#menjalankan-tes">Tes lokal</a>&emsp;
  <a href="docs/deployment.md">Panduan deployment</a>
</p>

OSSA dirancang untuk membantu tim keamanan mencatat dan menindaklanjuti insiden lintas departemen. Pelapor memilih departemen dan kategori dari daftar yang dikelola admin. Analis menggunakan laporan tersebut untuk menetapkan tingkat keparahan, penanggung jawab, dan status kasus.

Demo awal **Track C** memverifikasi `GET /incidents` di sandbox AWS Academy Cloud Foundations. Versi ini membaca dua insiden fiktif dari Amazon S3 melalui AWS Lambda.

## Arsitektur

Operator mengirim permintaan HTTPS bertanda tangan SigV4 dari AWS CloudShell ke Lambda Function URL dengan autentikasi `AWS_IAM`. Fungsi Python berjalan di `us-east-1` dan menggunakan `LabRole` untuk membaca objek JSON dari prefix `incidents/` pada bucket S3 privat.

[![Arsitektur serverless Track C dan hubungan IAM pada OSSA](docs/diagrams/track-c.png)](docs/diagrams/track-c.png)

## Bukti pengujian AWS

Demo dijalankan pada **26 November 2026**. Kedua ID pada respons cocok dengan nama file dan isi data contoh di repo.

| Pemeriksaan | Hasil | Tangkapan layar |
| --- | --- | --- |
| Objek Amazon S3 | Dua file JSON tersedia di `incidents/` | [Daftar objek](docs/evidence/01-s3-objects.png) |
| Tes fungsi Lambda | Handler mengembalikan status `200` dan kedua ID | [Respons Lambda](docs/evidence/02-lambda-test-200.png) |
| Akses melalui Function URL | HTTP `200` dengan SigV4 dan HTTP `403` tanpa tanda tangan | [Output CloudShell](docs/evidence/03-function-url-auth.png) |

[Ringkasan bukti pengujian](docs/evidence/README.md)

## Kontrak API

| Endpoint | Fungsi | HTTP sukses | Status |
| --- | --- | --- | --- |
| `GET /incidents` | Mengembalikan daftar insiden dalam array `items` | `200` | Teruji di AWS Academy |
| `POST /incidents` | Membuat laporan insiden | `201` | Rancangan |
| `PATCH /incidents/{id}` | Memperbarui triase insiden | `200` | Rancangan |
| `DELETE /incidents/{id}` | Menghapus insiden uji | `204` | Rancangan |

## Menjalankan tes

Jalankan perintah ini dari root repo dengan Python 3.11 atau lebih baru.

```bash
python -m unittest discover -s tests -v
```

Tes memakai dua insiden fiktif dan tiruan klien S3. Untuk mengulang demo di sandbox AWS Academy, ikuti [panduan deployment](docs/deployment.md).

## Struktur repositori

| Lokasi | Isi |
| --- | --- |
| [`handler.py`](handler.py) | Handler Lambda untuk `GET /incidents` |
| [`samples/`](samples/) | Dua berkas JSON dengan data insiden fiktif |
| [`tests/`](tests/) | Pengujian lokal handler |
| [`docs/deployment.md`](docs/deployment.md) | Konfigurasi Lambda, S3, dan langkah uji dari CloudShell |

## Rencana pengembangan

Tahap berikutnya melengkapi operasi tulis API serta membuat frontend untuk daftar insiden, formulir laporan, dan triase. Hosting dan autentikasi web bergantung pada izin dan kredit sandbox. Perluasan dengan EC2, ECR, dan RDS MySQL dipertimbangkan setelah pengembangan Track C.
