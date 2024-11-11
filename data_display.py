import psycopg2
import pandas as pd
from datetime import timedelta

# Veritabanına bağlanma fonksiyonu
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="Tunnel Project",
            user="postgres",
            password="DataRandomAccess123",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        print("Veritabanına bağlanırken hata oluştu:", e)
        return None

# İşlem sürelerini sabit olarak tanımlama
islem_sureleri = {
    "Kazı": timedelta(hours=2),
    "Tahkimat": timedelta(hours=4),
    "Püskürtme Beton": timedelta(hours=3)
}

# Son girilen işlemi ve bir sonraki işlemi hesaplama fonksiyonu
def sonraki_islemi_hesapla():
    conn = connect_db()
    if conn:
        query = "SELECT * FROM tasks ORDER BY id DESC LIMIT 1;"  # Son işlem
        df = pd.read_sql(query, conn)
        conn.close()

        if not df.empty:
            son_islem = df.iloc[0]
            baslangic_zamani = son_islem['bitis_zamani']
            islem_adi = son_islem['islem_adi_id']

            if islem_adi == 1:
                sonraki_islem = "Tahkimat"
                tahmini_baslangic = baslangic_zamani + islem_sureleri["Kazı"]
            elif islem_adi == 2:
                sonraki_islem = "Püskürtme Beton"
                tahmini_baslangic = baslangic_zamani + islem_sureleri["Tahkimat"]
            elif islem_adi == 3:
                sonraki_islem = "Kazı"
                tahmini_baslangic = baslangic_zamani + islem_sureleri["Püskürtme Beton"]
            else:
                sonraki_islem = "Bilinmiyor"
                tahmini_baslangic = None

            return sonraki_islem, tahmini_baslangic
    return None, None
