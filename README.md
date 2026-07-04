# Bike Sharing Demand Analysis Dashboard

Submission ini menggunakan **Bike Sharing Dataset** untuk menganalisis pola penyewaan sepeda pada periode 2011-2012. Analisis utama mencakup pengaruh musim, cuaca, tipe hari, jam penggunaan, tren bulanan, serta segmentasi demand menggunakan manual clustering berbasis binning kuantil.

## Struktur Folder

```text
submission
├── dashboard
│   ├── dashboard.py
│   └── main_data.csv
├── data
│   ├── day.csv
│   ├── hour.csv
│   └── Readme.txt
├── Proyek_Analisis_Data.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Pertanyaan Bisnis

1. Selama periode 2011-2012, musim dan kondisi cuaca mana yang menghasilkan rata-rata penyewaan sepeda harian tertinggi dan terendah, sehingga operator dapat menentukan prioritas redistribusi dan kesiapan armada?
2. Selama periode 2011-2012, pada jam berapa permintaan penyewaan sepeda paling tinggi pada hari kerja dibandingkan non-hari kerja, sehingga operator dapat mengoptimalkan ketersediaan sepeda pada jam puncak?
3. Bagaimana pertumbuhan total penyewaan sepeda secara bulanan dari 2011 ke 2012, sehingga operator dapat menilai periode dengan peluang ekspansi atau promosi terbesar?

## Teknik Analisis Lanjutan

Submission ini menerapkan **manual clustering dengan binning kuantil** terhadap jumlah penyewaan (`cnt`). Data dikelompokkan menjadi `Low`, `Medium`, `High`, dan `Very High` demand. Teknik ini relevan karena dataset tidak memiliki `customer_id` untuk RFM analysis dan tidak memiliki koordinat lokasi untuk geospatial analysis.

## Setup Environment

Gunakan Python 3.11 atau versi yang lebih baru.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Menjalankan Notebook

```bash
jupyter notebook Proyek_Analisis_Data.ipynb
```

Notebook sudah dijalankan dan berisi output tabel serta visualisasi.

## Menjalankan Dashboard Streamlit

```bash
streamlit run dashboard/dashboard.py
```

Dashboard membaca data dari `dashboard/main_data.csv`.

## Deployment Streamlit Cloud

Untuk mendapatkan nilai maksimal, deploy dashboard ke Streamlit Community Cloud dengan entry point:

```text
dashboard/dashboard.py
```

Setelah deploy berhasil, simpan tautan dashboard pada file `url.txt`.
