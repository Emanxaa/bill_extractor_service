# Bill Extractor

Proyek ini adalah layanan API yang dibuat dengan FastAPI untuk mengekstrak informasi dari file tagihan (bills) menggunakan OCR dan model bahasa (LLM).

## Fitur

*   Ekstraksi teks dari file gambar dan PDF menggunakan Tesseract OCR.
*   Pemrosesan dan normalisasi data yang diekstraksi.
*   Penggunaan Google Gemini untuk mem-parsing informasi keuangan secara cerdas.
*   Endpoint API untuk mengunggah file dan mendapatkan data terstruktur.

## Prasyarat

Sebelum memulai, pastikan Anda telah menginstal perangkat lunak berikut:

*   Python 3.11+
*   Docker & Docker Compose
*   Tesseract OCR

## Instalasi

1.  **Clone repository:**
    ```bash
    git clone https://github.com/username/bill-extractor.git
    cd bill-extractor
    ```

2.  **Buat dan aktifkan virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi Environment Variables:**
    Buat file `.env` di root direktori dan tambahkan variabel berikut. Ganti dengan kunci API Anda.
    ```env
    GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    ```

## Menjalankan Aplikasi

### Secara Lokal

Untuk menjalankan aplikasi secara lokal, gunakan perintah berikut:

```bash
python run.py
```
Aplikasi akan berjalan di `http://localhost:9001`.

### Menggunakan Docker

Anda juga dapat menjalankan aplikasi menggunakan Docker Compose untuk manajemen yang lebih mudah.

1.  **Build dan jalankan container:**
    ```bash
    docker-compose up --build
    ```

2.  Aplikasi akan dapat diakses di `http://localhost:9001`.

Untuk menghentikan aplikasi, tekan `CTRL+C` di terminal dan jalankan:
```bash
docker-compose down
```

## Struktur Proyek

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── extract.py  # API endpoint
│   ├── core/
│   │   └── config.py   # Konfigurasi aplikasi
│   ├── pipelines/
│   │   ├── extraction.py # Logika ekstraksi
│   │   └── mapper.py     # Pemetaan data
│   ├── schemas/
│   │   └── financial.py  # Skema data Pydantic
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── ocr_service.py
│   │   └── parsing_service.py
│   └── main.py         # Entrypoint aplikasi FastAPI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py              # Skrip untuk menjalankan server
```

## API Endpoint

### Ekstrak Informasi Tagihan

*   **URL:** `/api/v1/extract/`
*   **Method:** `POST`
*   **Body:** `multipart/form-data`
    *   `file`: File gambar atau PDF yang akan diunggah.

#### Contoh Penggunaan (cURL)

```bash
curl -X POST "http://localhost:9001/api/v1/extract/" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@/path/to/your/bill.pdf"
```

Dokumentasi API interaktif (Swagger UI) tersedia di `http://localhost:9001/docs`.
