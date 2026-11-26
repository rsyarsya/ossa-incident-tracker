# OSSA | Corporate Security Incident Tracker

OSSA membantu tim keamanan mencatat dan menindaklanjuti insiden lintas departemen. Departemen dan kategori dipilih dari daftar yang dikelola admin. Analis menetapkan tingkat keparahan, penanggung jawab, dan status kasus.

## Arsitektur Track C

Operator memakai CloudShell untuk memanggil Lambda Function URL melalui HTTPS dengan SigV4. Identitas sesi memerlukan izin invoke. Lambda menggunakan `LabRole` untuk membaca objek JSON di prefix `incidents/` pada bucket S3 privat. Demo dijalankan di `us-east-1`.

![Arsitektur Track C dan izin IAM](docs/diagrams/track-c.png)

## Kontrak API

| Endpoint | Fungsi | HTTP sukses | Tahap |
| --- | --- | --- | --- |
| GET /incidents | Daftar insiden dalam array items | 200 | Teruji di AWS Academy |
| POST /incidents | Buat laporan | 201 | Rancangan |
| PATCH /incidents/{id} | Perbarui triase | 200 | Rancangan |
| DELETE /incidents/{id} | Hapus record uji | 204 | Rancangan |

## Menjalankan tes

Dari root repo, jalankan `python -m unittest discover -s tests -v` dengan Python 3.11 atau lebih baru. Tes memakai dua insiden fiktif dan tiruan klien S3 sehingga dapat dijalankan tanpa kredensial AWS.

## Demo lab

Demo `GET /incidents` berhasil di sandbox AWS Academy. Tes Lambda mengembalikan status 200 dan kedua insiden contoh. Function URL dengan `AWS_IAM` mengembalikan HTTP 200 untuk permintaan bertanda tangan SigV4 dan HTTP 403 untuk permintaan tanpa tanda tangan. [Bukti pengujian](docs/evidence/README.md)

Konfigurasi lab dan langkah untuk mengulang demo tersedia di [panduan deployment](docs/deployment.md). Perluasan dengan EC2, ECR, dan RDS MySQL masih bergantung pada akses sandbox.
