import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#create_monthly_rental() digunakan untuk menyiapkan monthly_rental
def create_monthly_rental(df):
    monthly_rental = df.resample(rule='M', on='dteday').agg({
        "casual" : "sum",
        "registered" : "sum",
        "cnt": "sum"
    })
    monthly_rental = monthly_rental.reset_index()

    return monthly_rental

#create_byseason() digunakan untuk menyiapkan byseason
def create_byseason(df):
    byseason = df.groupby(by="season").cnt.sum().reset_index()
    
    return byseason

#create_sum_rent_hour() bertanggung jawab untuk menyiapkan sum_rent_hour
def create_sum_rent_hour(df):
    sum_rent_hour = hour.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    
    return sum_rent_hour

#load data
day = pd.read_csv("https://github.com/rizkifitria/Bike-Sharing/blob/04dc9d144e9304643acebf4adb6608a376716835/data/day.csv")
hour = pd.read_csv("https://github.com/rizkifitria/Bike-Sharing/blob/04dc9d144e9304643acebf4adb6608a376716835/data/hour.csv")

#Kolom dteday akan menjadi kunci dalam pembuatan filter. Untuk ini, kita perlu mengurutkan DataFrame berdasarkan dteday serta memastikan kedua kolom tersebut bertipe datetime
datetime_columns = ["dteday"]
day.sort_values(by="dteday", inplace=True)
day.reset_index(inplace=True)
hour.sort_values(by="dteday", inplace=True)
hour.reset_index(inplace=True)

for column in datetime_columns:
    day[column] = pd.to_datetime(day[column])
    hour[column] = pd.to_datetime(hour[column])
    
#Membuat Komponen Filter    
min_date = day["dteday"].min()
max_date = hour["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_day = day[(day["dteday"] >= str(start_date)) & 
                (day["dteday"] <= str(end_date))]
main_hour = hour[(day["dteday"] >= str(start_date)) & 
                (hour["dteday"] <= str(end_date))]

#Mengubah nilai kolom season menjadi string
season_desc = {
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
}
day['season'] = day['season'].map(season_desc)

monthly_rental = create_monthly_rental(main_day)
byseason = create_byseason(main_day)
sum_rent_hour = create_sum_rent_hour(main_hour)

#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Dashboard Penyewaan Sepeda :sparkles:')

#Informasi total sewa dari setiap jenis penyewa
st.subheader('Total Sewa Setiap Bulan') #monthly rental

col1, col2, col3 = st.columns(3)
 
with col1:
    casual_rent = monthly_rental.casual.sum()
    st.metric("Penyewa Umum", value=casual_rent)

with col2:
    registered_rent = monthly_rental.registered.sum()
    st.metric("Penyewa Terdaftar", value=registered_rent)

with col3:
    total_rent = monthly_rental.cnt.sum()
    st.metric("Total Penyewa", value=total_rent)
    
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_rental["dteday"],
    monthly_rental["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

#Informasi tentang jumlah penyewaan sepeda berdasarkan musim
st.subheader("Jumlah Penyewaan Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(35, 15))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="season", 
    y="cnt",
    data=byseason.sort_values(by="cnt", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by Season", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

#Informasi tentang performa waktu penyewaan, kita akan menampilkan 5 waktu ketika penyewaan paling tinggi dan paling rendah melalui sebuah visualisasi data
st.subheader("Waktu dengan Penyewaan Tertinggi dan Terendah")
 
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="hr", y="cnt", data=sum_rent_hour.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Penyewaan Tertinggi ", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="hr", y="cnt", data=sum_rent_hour.sort_values(by="hr", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Penyewaan Terendah", loc="center", fontsize=50)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)
 
st.caption('Copyright (c) Fitria 2024')
