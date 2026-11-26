# Rencana deployment Track C

Demo `GET /incidents` lulus di sandbox AWS Academy pada 26 November 2026. Gunakan langkah berikut untuk mengulang deployment pada sesi lab aktif. Periksa sisa kredit dan ketentuan terminasi di Canvas sebelum memulai sesi. [Bukti pengujian](evidence/README.md)

1. Mulai lab melalui Canvas dan buka console dari tombol AWS pada lab aktif. Pilih us-east-1. Periksa identitas di terminal lab dengan `aws sts get-caller-identity` dan cocokkan dengan sesi course. Jika akun berbeda, kembali ke launcher.
2. Gunakan bucket privat khusus demo yang diizinkan lab. Pertahankan Block Public Access. Unggah kedua file di samples/ dengan nama asli di bawah prefix incidents/. Periksa dua key beserta ID di dalam JSON.
3. Pilih execution role bawaan yang dipercaya oleh lambda.amazonaws.com. Untuk GET, cek s3:ListBucket pada bucket serta s3:GetObject pada incidents/*. Identitas deployment perlu izin membuat fungsi dan meneruskan role yang disetujui (iam:PassRole).
4. Buat fungsi `ossa-list-incidents` dengan Python 3.12, arsitektur `x86_64`, memori 128 MB, timeout 15 detik, dan execution role `LabRole`. Simpan `handler.py` di root paket, atur handler ke `handler.lambda_handler`, lalu isi environment variable `INCIDENT_BUCKET` dengan nama bucket. Deploy kode. Handler memakai boto3 dari runtime.
5. Buat Function URL dengan autentikasi AWS_IAM. Pastikan identitas pemanggil mendapat lambda:InvokeFunctionUrl dan lambda:InvokeFunction untuk fungsi ini. Pertahankan autentikasi IAM apabila muncul AccessDenied dan catat aksi yang terhalang.
6. Dari CloudShell, kirim GET bertanda tangan SigV4 ke path /incidents. Untuk contoh Python di bawah, salin URL fungsi ke prompt. Skrip menggunakan kredensial sesi dari rantai kredensial SDK. Pastikan boto3, botocore, dan requests tersedia di terminal.

~~~python
import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

url = input("Function URL: ").strip().rstrip("/") + "/incidents"
credentials = boto3.Session().get_credentials().get_frozen_credentials()
request = AWSRequest(method="GET", url=url)
SigV4Auth(credentials, "lambda", "us-east-1").add_auth(request)
response = requests.get(url, headers=dict(request.headers), timeout=25)
print(response.status_code, response.text)
~~~

7. Periksa bahwa HTTP 200 memuat array `items` dengan kedua ID yang cocok dengan file contoh. Ulangi GET pada URL yang sama tanpa tanda tangan dan periksa HTTP 403. Simpan bukti objek S3, respons Lambda, dan kedua hasil Function URL di `docs/evidence/`. Potong identitas sesi, ARN akun, dan URL lab dari tangkapan layar sebelum memasukkannya ke repo.
8. Simpan bukti di luar sesi lab sebelum terminasi. Dalam sesi proyek ini, bucket dan fungsi harus dibuat ulang setelah lab sebelumnya diterminasi. Ikuti instruksi cleanup course untuk resource demo yang dibuat sendiri.
