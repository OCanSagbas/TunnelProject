import streamlit as st
from datetime import datetime
from data_process import veri_ekle
from data_display import sonraki_islemi_hesapla, connect_db
import pandas as pd

# Streamlit arayüzü
st.sidebar.title("Sayfa Seçimi")
sayfa = st.sidebar.radio("Seçim Yapın", ("İşlem Girişi", "Veri Görüntüleme"))

if sayfa == "İşlem Girişi":
    st.title("Tünel İnşaat Projesi - İşlem Girişi")

    with st.form("veri_giris_formu"):
        islem_adi = st.selectbox("İşlem Adı", options=["Kazı", "Tahkimat", "Püskürtme Beton"])
        baslangic_zamani = st.time_input("Başlangıç Zamanı", value=None)
        bitis_zamani = st.time_input("Bitiş Zamanı", value=None)
        submit_button = st.form_submit_button("Kaydet")

    if submit_button:
        islem_adi_id = {"Kazı": 1, "Tahkimat": 2, "Püskürtme Beton": 3}.get(islem_adi, None)
        if baslangic_zamani and bitis_zamani:
            baslangic_datetime = datetime.combine(datetime.today(), baslangic_zamani)
            bitis_datetime = datetime.combine(datetime.today(), bitis_zamani)
            if bitis_datetime <= baslangic_datetime:
                st.error("Hata: Bitiş zamanı, başlangıç zamanından sonra olmalıdır.")
            else:
                veri_ekle(islem_adi_id, baslangic_datetime, bitis_datetime)
                st.success("Veri başarıyla kaydedildi!")
        else:
            st.error("Lütfen başlangıç ve bitiş zamanlarını girin!")

elif sayfa == "Veri Görüntüleme":
    st.title("Tünel İnşaat Projesi - İşlem Bildirimi ve Veri Görüntüleme")

    sonraki_islem, tahmini_baslangic = sonraki_islemi_hesapla()

    if sonraki_islem and tahmini_baslangic:
        st.info(f"Bir sonraki işlem: {sonraki_islem}")
        st.info(f"Tahmini Başlangıç Zamanı: {tahmini_baslangic}")
    else:
        st.warning("Sonraki işlem bilgisi bulunamadı.")

    # Tüm task tablosunu görüntüle
    conn = connect_db()
    if conn:
        df_all = pd.read_sql("SELECT * FROM tasks ORDER BY id DESC LIMIT 100;", conn)
        conn.close()
        st.subheader("Son 100 İşlem Kaydı")
        st.write(df_all)