# ✈️ Dinamik Uçuş Simülasyonu ve Rota Optimizasyonu

Bu proje, gerçek dünya havaalanı verilerini kullanarak iki nokta arasındaki en kısa uçuş rotasını bulan ve bu rotayı bir dünya haritası üzerinde dinamik, kavisli bir animasyonla görselleştiren bir masaüstü uygulamasıdır.

## 🌟 Öne Çıkan Özellikler

* **Dijkstra Algoritması:** Havaalanları arasındaki rotaları gerçek mesafe verilerine dayanarak optimize eder.
* **Büyük Daire (Great Circle) Rotaları:** Dünyanın eğriliğini hesaba katarak (Slerp interpolasyonu) kavisli ve gerçekçi uçuş yolları çizer.
* **Antimeridyen Geçiş Desteği:** Pasifik Okyanusu üzerinden (Amerika - Avustralya gibi) yapılan uçuşlarda harita üzerindeki "boylam sıçramalarını" ve yatay çizgi hatalarını engelleyen akıllı rota bölme mantığı.
* **Smooth (Sarsıntısız) Animasyon:** `set_position` metodu ve `update_idletasks` optimizasyonu ile titreme (flickering) yapmayan yağ gibi akan uçak animasyonu.
* **Gerçek Zamanlı Maliyet Hesaplama:** Toplam uçuş mesafesini kilometre cinsinden dinamik olarak gösterir.

## 🛠️ Kullanılan Teknolojiler

* **Python 3.x**
* **Tkinter:** GUI (Arayüz) geliştirme.
* **tkintermapview:** İnteraktif dünya haritası entegrasyonu.
* **Pandas:** Havaalanı veri setlerinin işlenmesi.
* **Pillow (PIL):** Uçak ikonları ve görsel işleme.
* **Math Library:** Küresel trigonometrik hesaplamalar (Haversine & Slerp).

## 🚀 Kurulum ve Çalıştırma

1.  **Depoyu klonlayın:**
    ```bash
    git clone [https://github.com/kullaniciadin/flight-simulation-optimization.git](https://github.com/kullaniciadin/flight-simulation-optimization.git)
    cd flight-simulation-optimization
    ```

2.  **Gerekli kütüphaneleri yükleyin:**
    ```bash
    pip install tkintermapview pandas pillow
    ```

3.  **Uygulamayı başlatın:**
    ```bash
    python src/main.py
    ```

## 📂 Proje Yapısı

```text
├── data/
│   └── airports.dat          # Havaalanı koordinat ve IATA bilgileri
├── src/
│   ├── main.py               # Ana GUI ve animasyon kontrolcü
│   ├── dijkstra_algorithm.py  # Rota hesaplama mantığı
│   ├── graph_builder.py      # Veri setinden grafik yapısı oluşturma
│   └── plane_icon.png        # Animasyon için kullanılan uçak görseli
└── README.md
