# Bukti pengujian OSSA Track C

Demo dijalankan pada 26 November 2026 di sandbox AWS Academy Cloud Foundations, region `us-east-1`. Fungsi `ossa-list-incidents` membaca dua objek JSON yang berisi data fiktif.

| Pemeriksaan | Hasil | Bukti |
| --- | --- | --- |
| Objek contoh di Amazon S3 | Dua file JSON tersedia di `ossa-incidents-482731/incidents/` | [Daftar objek S3](01-s3-objects.png) |
| Pemanggilan dari tab Test AWS Lambda | Eksekusi berhasil, handler mengembalikan `statusCode: 200` dan dua ID | [Respons Lambda](02-lambda-test-200.png) |
| `GET /incidents` melalui Function URL `AWS_IAM` | HTTP 200 dengan SigV4, HTTP 403 tanpa tanda tangan | [Hasil pengujian CloudShell](03-function-url-auth.png) |

Kedua ID yang muncul pada respons sama dengan ID pada nama objek dan berkas contoh di repo.

- `00000000-0000-4000-8000-000000000001`
- `00000000-0000-4000-8000-000000000002`

Tangkapan layar dipotong untuk menampilkan bagian yang mendukung hasil uji dan mengeluarkan identitas sesi, nomor akun, serta alamat Function URL.
