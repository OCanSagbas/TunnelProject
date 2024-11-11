import psycopg2
from datetime import datetime

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

# tasks tablosuna veri ekleme fonksiyonu
def veri_ekle(islem_adi_id, baslangic_zamani, bitis_zamani):
    islem_suresi = bitis_zamani - baslangic_zamani  # İşlem Süresi Hesaplama
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        insert_query = '''
        INSERT INTO tasks (islem_adi_id, baslangic_zamani, bitis_zamani, islem_suresi)
        VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (islem_adi_id, baslangic_zamani, bitis_zamani, islem_suresi))
        conn.commit()
        cursor.close()
        conn.close()
