import sys
import os
import tkinter as tk
from tkinter import ttk
import tkintermapview
from PIL import Image, ImageTk
import pandas as pd
import time
import math

# --- BAĞLANTILAR VE DİZİN AYARI ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path: sys.path.append(project_root)
os.chdir(project_root)

from src.dijkstra_algorithm import find_shortest_path
from src.graph_builder import build_real_graph

# --- VERİ YÜKLEME ---
def load_airport_data():
    try:
        df = pd.read_csv('data/airports.dat', header=None)
        data = {}
        for _, row in df.iterrows():
            name = f"{row[1]} ({row[2]})"
            iata = str(row[4]) if pd.notnull(row[4]) and row[4] != "\\N" else str(row[0])
            data[name] = (float(row[6]), float(row[7]), iata)
        return data
    except Exception as e:
        print(f"Veri hatası: {e}"); return {}

airport_lookup = load_airport_data()
airport_names = sorted(list(airport_lookup.keys()))
G = build_real_graph() 

# --- ARAYÜZ ---
root = tk.Tk()
root.geometry("1100x905")
root.title("Dinamik Uçuş Simülasyonu ve Rota Optimizasyonu")
root.configure(bg="#f0f2f5")

info_frame = tk.Frame(root, bg="#1a237e")
info_frame.pack(side="top", fill="x")
cost_label = tk.Label(info_frame, text="Toplam Maliyet: 0.00 km", fg="#ffca28", bg="#1a237e", font=("Arial", 12, "bold"))
cost_label.pack(pady=5)

input_panel = tk.Frame(root, bg="white", pady=10)
input_panel.pack(side="top", fill="x", padx=20, pady=5)
start_combo = ttk.Combobox(input_panel, width=40, values=airport_names)
start_combo.grid(row=0, column=1, padx=5); start_combo.set("Nereden?")
end_combo = ttk.Combobox(input_panel, width=40, values=airport_names)
end_combo.grid(row=0, column=3, padx=5); end_combo.set("Nereye?")

map_widget = tkintermapview.TkinterMapView(root, width=1100, height=650)
map_widget.pack(fill="both", expand=True, padx=10, pady=10)
map_widget.set_position(40.0, 15.0)
map_widget.set_zoom(3)

current_marker = None
current_paths = [] 

try:
    # Uçak ikonunu bir kez yükle
    plane_img = Image.open("src/plane_icon.png").resize((35, 30))
    plane_photo = ImageTk.PhotoImage(plane_img)
except: 
    plane_photo = None

# --- BÜYÜK DAİRE (KAVİSLİ ROTA) HESAPLAMA ---
def get_intermediate_point(start_lat, start_lon, end_lat, end_lon, fraction):
    diff = end_lon - start_lon
    if diff > 180: end_lon -= 360
    elif diff < -180: end_lon += 360

    lat1, lon1 = math.radians(start_lat), math.radians(start_lon)
    lat2, lon2 = math.radians(end_lat), math.radians(end_lon)

    d = 2 * math.asin(math.sqrt(math.sin((lat1 - lat2) / 2)**2 + 
                                math.cos(lat1) * math.cos(lat2) * math.sin((lon1 - lon2) / 2)**2))
    if d == 0: return start_lat, start_lon

    A = math.sin((1 - fraction) * d) / math.sin(d)
    B = math.sin(fraction * d) / math.sin(d)

    x = A * math.cos(lat1) * math.cos(lon1) + B * math.cos(lat2) * math.cos(lon2)
    y = A * math.cos(lat1) * math.sin(lon1) + B * math.cos(lat2) * math.sin(lon2)
    z = A * math.sin(lat1) + B * math.sin(lat2)

    lat_res = math.atan2(z, math.sqrt(x**2 + y**2))
    lon_res = math.atan2(y, x)

    final_lon = math.degrees(lon_res)
    if final_lon > 180: final_lon -= 360
    if final_lon < -180: final_lon += 360
    return math.degrees(lat_res), final_lon

# --- ANA FONKSİYON ---
def find_route_action():
    global current_marker, current_paths
    
    # 1. TEMİZLİK
    for p in current_paths: p.delete()
    current_paths = []
    map_widget.delete_all_marker()
    if current_marker:
        current_marker.delete()
        current_marker = None
    
    s_val, e_val = start_combo.get(), end_combo.get()
    
    if s_val in airport_lookup and e_val in airport_lookup:
        start_code = airport_lookup[s_val][2]
        end_code = airport_lookup[e_val][2]
        
        try:
            result = find_shortest_path(G, start_node=start_code, end_node=end_code)
            path, total_dist = (result[0], result[1]) if isinstance(result, tuple) else (result, 0.0)

            if not path or len(path) < 2:
                cost_label.config(text="HATA: Rota bulunamadı!", fg="red")
                return

            coord_map = {str(v[2]): (v[0], v[1]) for v in airport_lookup.values()}
            name_map = {str(v[2]): k for k, v in airport_lookup.items()}
            
            all_flight_points = []
            segment = []

            # 2. ROTA HESAPLAMA VE ÇİZİM
            for i in range(len(path) - 1):
                s_node, e_node = str(path[i]), str(path[i+1])
                if s_node in coord_map and e_node in coord_map:
                    s_pos, e_pos = coord_map[s_node], coord_map[e_node]
                    map_widget.set_marker(s_pos[0], s_pos[1], text=name_map.get(s_node, ""))
                    
                    # Mesafe arttıkça adım sayısını artırarak akıcılığı sağla
                    steps = max(60, int(total_dist / 100))
                    for s in range(steps + 1):
                        p = get_intermediate_point(s_pos[0], s_pos[1], e_pos[0], e_pos[1], s/steps)
                        
                        if segment and abs(p[1] - segment[-1][1]) > 180:
                            current_paths.append(map_widget.set_path(segment, color="#3498db", width=2.5))
                            segment = []
                        
                        segment.append(p)
                        all_flight_points.append(p)
            
            # Son varış noktası işareti ve rotanın son parçası
            map_widget.set_marker(coord_map[str(path[-1])][0], coord_map[str(path[-1])][1], text=name_map.get(str(path[-1]), ""))
            if segment:
                current_paths.append(map_widget.set_path(segment, color="#3498db", width=2.5))

            # 3. YAĞ GİBİ AKAN ANİMASYON (Sıfır Titreme)
            if all_flight_points:
                # Markeri bir kere oluştur
                current_marker = map_widget.set_marker(all_flight_points[0][0], all_flight_points[0][1], icon=plane_photo)
                
                for pt in all_flight_points:
                    # Silip yeniden yapmak yerine SADECE POZİSYONU GÜNCELLE
                    current_marker.set_position(pt[0], pt[1])
                    
                    # Gereksiz tüm ekranı değil sadece bekleyen görsel işleri güncelle
                    root.update_idletasks()
                    time.sleep(0.007) # Hız dengesi

            cost_label.config(text=f"Toplam Mesafe: {total_dist:.2f} km", fg="#ffca28")

        except Exception as e:
            print(f"Hata: {e}")

tk.Button(input_panel, text="ROTAYI ÇİZ ✈", command=find_route_action, bg="#28a745", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=4, padx=15)
root.mainloop()