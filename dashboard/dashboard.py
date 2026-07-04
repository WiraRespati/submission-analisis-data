from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Bike Sharing Demand Dashboard",
    layout="wide",
)


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "main_data.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH, parse_dates=["dteday"])
    data["date"] = data["dteday"].dt.date
    return data


df = load_data()

season_order = ["Spring", "Summer", "Fall", "Winter"]
weather_order = [
    "Clear / Partly Cloudy",
    "Mist / Cloudy",
    "Light Snow / Light Rain",
    "Heavy Rain / Snow Fog",
]
demand_order = ["Low", "Medium", "High", "Very High"]

st.title("Bike Sharing Demand Dashboard")
st.caption(
    "Analisis interaktif permintaan bike sharing berdasarkan musim, cuaca, tipe hari, dan jam penggunaan pada periode 2011-2012."
)

with st.sidebar:
    st.header("Filter Data")

    min_date = df["date"].min()
    max_date = df["date"].max()
    selected_dates = st.date_input(
        "Rentang tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date, end_date = min_date, max_date

    selected_seasons = st.multiselect(
        "Musim",
        options=season_order,
        default=season_order,
    )
    selected_weather = st.multiselect(
        "Kondisi cuaca",
        options=weather_order,
        default=weather_order,
    )
    selected_day_type = st.multiselect(
        "Tipe hari",
        options=sorted(df["day_type"].unique()),
        default=sorted(df["day_type"].unique()),
    )

filtered_df = df[
    (df["date"] >= start_date)
    & (df["date"] <= end_date)
    & (df["season_label"].isin(selected_seasons))
    & (df["weather_label"].isin(selected_weather))
    & (df["day_type"].isin(selected_day_type))
]

if filtered_df.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    st.stop()

total_rentals = int(filtered_df["cnt"].sum())
avg_hourly_rentals = filtered_df["cnt"].mean()
total_casual = int(filtered_df["casual"].sum())
total_registered = int(filtered_df["registered"].sum())
peak_hour = int(filtered_df.groupby("hr")["cnt"].mean().idxmax())

metric_cols = st.columns(5)
metric_cols[0].metric("Total Rentals", f"{total_rentals:,}")
metric_cols[1].metric("Avg Hourly Rentals", f"{avg_hourly_rentals:,.1f}")
metric_cols[2].metric("Casual Users", f"{total_casual:,}")
metric_cols[3].metric("Registered Users", f"{total_registered:,}")
metric_cols[4].metric("Peak Hour", f"{peak_hour:02d}:00")

st.divider()

monthly = (
    filtered_df.groupby(["year", "month", "month_name"], observed=False)["cnt"]
    .sum()
    .reset_index()
    .sort_values(["year", "month"])
)
monthly["year"] = monthly["year"].astype(str)

fig_monthly = px.line(
    monthly,
    x="month",
    y="cnt",
    color="year",
    markers=True,
    labels={"month": "Bulan", "cnt": "Total Penyewaan", "year": "Tahun"},
    title="Tren Total Penyewaan Bulanan",
)
fig_monthly.update_xaxes(
    tickmode="array",
    tickvals=list(range(1, 13)),
    ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
)
fig_monthly.update_layout(legend_title_text="Tahun", hovermode="x unified")
st.plotly_chart(fig_monthly, use_container_width=True)

left_col, right_col = st.columns(2)

with left_col:
    season_summary = (
        filtered_df.groupby("season_label", observed=False)["cnt"]
        .mean()
        .reindex(season_order)
        .dropna()
        .reset_index()
    )
    fig_season = px.bar(
        season_summary,
        x="season_label",
        y="cnt",
        color="season_label",
        text_auto=".0f",
        labels={"season_label": "Musim", "cnt": "Rata-rata Penyewaan per Jam"},
        title="Rata-rata Penyewaan Berdasarkan Musim",
    )
    fig_season.update_layout(showlegend=False)
    st.plotly_chart(fig_season, use_container_width=True)

with right_col:
    weather_summary = (
        filtered_df.groupby("weather_label", observed=False)["cnt"]
        .mean()
        .reindex(weather_order)
        .dropna()
        .reset_index()
    )
    fig_weather = px.bar(
        weather_summary,
        y="weather_label",
        x="cnt",
        color="weather_label",
        text_auto=".0f",
        labels={"weather_label": "Cuaca", "cnt": "Rata-rata Penyewaan per Jam"},
        title="Rata-rata Penyewaan Berdasarkan Cuaca",
    )
    fig_weather.update_layout(showlegend=False)
    st.plotly_chart(fig_weather, use_container_width=True)

hourly_pattern = (
    filtered_df.groupby(["day_type", "hr"], observed=False)["cnt"]
    .mean()
    .reset_index()
)
fig_hour = px.line(
    hourly_pattern,
    x="hr",
    y="cnt",
    color="day_type",
    markers=True,
    labels={"hr": "Jam", "cnt": "Rata-rata Penyewaan", "day_type": "Tipe Hari"},
    title="Pola Jam Sibuk: Hari Kerja vs Non-Hari Kerja",
)
fig_hour.update_xaxes(tickmode="linear", dtick=1)
fig_hour.update_layout(hovermode="x unified")
st.plotly_chart(fig_hour, use_container_width=True)

segment_cols = st.columns([1.2, 1])

with segment_cols[0]:
    segment_summary = (
        filtered_df.groupby("demand_segment", observed=False)
        .agg(
            records=("cnt", "count"),
            avg_rentals=("cnt", "mean"),
            avg_temp_celsius=("temp_celsius", "mean"),
            avg_humidity_percent=("humidity_percent", "mean"),
        )
        .reindex(demand_order)
        .dropna()
        .reset_index()
    )
    fig_segment = px.bar(
        segment_summary,
        x="demand_segment",
        y="avg_rentals",
        color="demand_segment",
        text_auto=".0f",
        labels={"demand_segment": "Segmen Demand", "avg_rentals": "Rata-rata Penyewaan"},
        title="Manual Clustering Demand dengan Binning Kuantil",
    )
    fig_segment.update_layout(showlegend=False)
    st.plotly_chart(fig_segment, use_container_width=True)

with segment_cols[1]:
    st.subheader("Insight Utama")
    st.write(
        "Musim dan cuaca memengaruhi pola permintaan. Kondisi cerah dan musim dengan suhu nyaman cenderung menghasilkan permintaan lebih tinggi."
    )
    st.write(
        "Hari kerja memiliki puncak permintaan yang lebih kuat pada jam komuter, sedangkan non-hari kerja cenderung terkonsentrasi pada siang hingga sore."
    )
    st.write(
        "Segmen Very High Demand dapat digunakan sebagai sinyal operasional untuk menambah armada dan petugas redistribusi."
    )

st.subheader("Rekomendasi Action Item")
st.markdown(
    """
    - Prioritaskan redistribusi sepeda pada jam puncak hari kerja, terutama sebelum jam berangkat dan pulang kerja.
    - Siapkan armada tambahan pada musim dan kondisi cuaca dengan rata-rata penyewaan tertinggi.
    - Gunakan segmentasi demand sebagai aturan operasional sederhana untuk menentukan jadwal inspeksi dan kesiapan sepeda cadangan.
    - Jalankan promosi pada periode permintaan rendah agar utilisasi armada tetap stabil.
    """
)

with st.expander("Lihat data terfilter"):
    st.dataframe(filtered_df, use_container_width=True)
