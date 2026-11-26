# Rencana deployment Track C

Status: uji lokal selesai. Langkah berikut dijalankan saat sesi AWS Academy tersedia. Gunakan sandbox course dan periksa sisa kredit serta ketentuan End Lab di Canvas terlebih dahulu.

1. Mulai lab melalui Canvas dan buka console dari tombol AWS pada lab aktif. Pilih us-east-1. Periksa identitas di terminal lab dengan `aws sts get-caller-identity` dan cocokkan dengan sesi course. Jika akun berbeda, kembali ke launcher.
2. Gunakan bucket privat khusus demo yang diizinkan lab. Pertahankan Block Public Access. Unggah kedua file di samples/ dengan nama asli di bawah prefix incidents/. Periksa dua key beserta ID di dalam JSON.
3. Pilih execution role bawaan yang dipercaya oleh lambda.amazonaws.com. Untuk GET, cek s3:ListBucket pada bucket serta s3:GetObject pada incidents/*. Identitas deployment perlu izin membuat fungsi dan meneruskan role yang disetujui (iam:PassRole).
4. Di Lambda console, buat fungsi Python 3.12 pada arsitektur default dengan role tersebut. Simpan isi handler.py sebagai handler.py di root paket, atur handler ke handler.lambda_handler dan environment variable INCIDENT_BUCKET ke nama bucket. Deploy kode. Handler memakai boto3 dari runtime.
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
response = requests.get(url, headers=dict(request.headers), timeout=15)
print(response.status_code, response.text)
~~~

7. Uji lulus bila HTTP 200 memuat array items dengan kedua ID yang cocok dengan file contoh. Simpan tangkapan layar konfigurasi AWS_IAM, dua key objek S3, dan output HTTP yang sudah diperiksa di docs/evidence/. Hindari token sesi, kredensial, dan header Authorization. Bila gagal, catat status aktual. Output tes lokal disimpan terpisah dari bukti AWS.
8. Sesudah bukti tersimpan, ikuti instruksi cleanup course untuk resource demo yang dibuat sendiri. Periksa ketentuan persistensi resource dan kredit sebelum End Lab.
