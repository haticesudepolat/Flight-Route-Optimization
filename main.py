from src.graph_builder import build_real_graph
from dijkstra_algorithm import find_shortest_path 
from src.gui import FlightGUI

def main():
    # 1. Grafı Oluştur
    print("Havalimanı verileri yükleniyor ve graf yapısı kuruluyor...")
    G = build_real_graph()

    print(f"Başarılı! Toplam Düğüm: {G.number_of_nodes()}, Toplam Bağlantı: {G.number_of_edges()}")

    # 2. Kullanıcıdan Girdi Al
    print("\n--- Uçuş Rotası Hesaplama ---")
    start_node = input("Başlangıç Havalimanı Kodu (örn: IST): ").upper()
    end_node = input("Varış Havalimanı Kodu (örn: JFK): ").upper()

    # 3. Şehirlerin Graf İçinde Olup Olmadığını Kontrol Et
    if start_node not in G or end_node not in G:
        print(f"Hata: Girdiğiniz kodlar ({start_node} veya {end_node}) veri setinde bulunamadı!")
        return

    # 4. Algoritmayı Çalıştır
    try:
        path, total_distance = find_shortest_path(G, start_node, end_node)

        # 5. Sonuçları Yazdır
        if total_distance == float('inf'):
            print(f"\nÜzgünüz, {start_node} ile {end_node} arasında bir rota bulunamadı.")
        else:
            print("\n" + "="*40)
            print(f"HESAPLANAN EN KISA ROTA:")
            print(" -> ".join(path))
            print(f"\nTOPLAM MESAFE: {total_distance:.2f} km")
            print("="*40)

            # 6. GUI / Görselleştirmeyi Başlat (EKLEDİĞİMİZ KISIM)
            print("\nHarita simülasyonu hazırlanıyor, lütfen bekleyin...")
            # Senin algoritman tarafından bulunan 'path' verisini İrem'in arayüzüne gönderiyoruz
            app = FlightGUI(G, path)
            app.run()

    except Exception as e:
        print(f"Algoritma çalışırken veya GUI başlatılırken bir hata oluştu: {e}")

if __name__ == "__main__":
    main()