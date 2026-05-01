import sys
import os
import tkinter as tk
from tkinter import ttk
import tkintermapview
from PIL import Image, ImageTk
import pandas as pd
import time

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
            # IATA kodu yoksa ID'yi yedek olarak kullanıyoruz
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

# Maliyet Göstergesi İçin Etiket
info_frame = tk.Frame(root, bg="#1a237e")
info_frame.pack(side="top", fill="x")
cost_label = tk.Label(info_frame, text="Toplam Maliyet: 0.00 km", fg="#ffca28", bg="#1a237e", font=("Arial", 12, "bold"))
cost_label.pack(pady=5)

# Kombobox ve Harita (Standart Kurulum)
input_panel = tk.Frame(root, bg="white", pady=10)
input_panel.pack(side="top", fill="x", padx=20, pady=5)
start_combo = ttk.Combobox(input_panel, width=40, values=airport_names)
start_combo.grid(row=0, column=1, padx=5); start_combo.set("Nereden?")
end_combo = ttk.Combobox(input_panel, width=40, values=airport_names)
end_combo.grid(row=0, column=3, padx=5); end_combo.set("Nereye?")

map_widget = tkintermapview.TkinterMapView(root, width=1100, height=650)
map_widget.pack(fill="both", expand=True, padx=10, pady=10)

map_widget.set_position(40.0, 15.0) # Merkezi İtalya civarına aldım ki İspanya ve Türkiye aynı anda görünsün
map_widget.set_zoom(5) # Kadrajı genişletmek için zoom'u 5 yaptım

current_marker = None
current_path = None
try:
    plane_photo = ImageTk.PhotoImage(Image.open("src/plane_icon.png").resize((35, 30)))
except: plane_photo = None

# --- GELİŞMİŞ ROTA VE MALİYET HESAPLAMA ---
def find_route_action():
    global current_marker, current_path
    s_val, e_val = start_combo.get(), end_combo.get()
    
    if s_val in airport_lookup and e_val in airport_lookup:
        start_code = airport_lookup[s_val][2]
        end_code = airport_lookup[e_val][2]
        
        try:
            result = find_shortest_path(G, start_node=start_code, end_node=end_code)
            
            if isinstance(result, tuple):
                path, total_dist = result[0], result[1]
            else:
                path, total_dist = result, 0.0

            if not path or len(path) < 2:
                cost_label.config(text="HATA: Uçuş rotası bulunamadı!", fg="red")
                return

            if path and isinstance(path, list):
                if current_path: current_path.delete()
                map_widget.delete_all_marker()

                coord_map = {str(v[2]): (v[0], v[1]) for v in airport_lookup.values()}
                name_map = {str(v[2]): k for k, v in airport_lookup.items()}
                
                path_coords = []
                for node in path:
                    clean_node = str(node[0] if isinstance(node, list) else node)
                    if clean_node in coord_map:
                        coord = coord_map[clean_node]
                        path_coords.append(coord)
                        map_widget.set_marker(coord[0], coord[1], text=name_map.get(clean_node, ""))

                if path_coords:
                    current_path = map_widget.set_path(path_coords, color="#3498db", width=2)
                    cost_label.config(text=f"Toplam Maliyet: {total_dist:.2f} km", fg="#ffca28")
                    
                    for i in range(len(path_coords) - 1):
                        start_pos, end_pos = path_coords[i], path_coords[i+1]
                        dist = ((start_pos[0]-end_pos[0])**2 + (start_pos[1]-end_pos[1])**2)**0.5
                        
                        # --- HIZ AYARLARI ---
                        # steps: dist çarpanını 25'e düşürerek uzun yolları hızlandırdık.
                        # max(40, ...): Kısa yollarda minimum 40 adım atarak "tık diye bitmesini" önledik.
                        steps = max(40, int(dist * 25)) 
                        
                        for s in range(steps):
                            curr_lat = start_pos[0] + (end_pos[0] - start_pos[0]) * (s / steps)
                            curr_lon = start_pos[1] + (end_pos[1] - start_pos[1]) * (s / steps)
                            
                            old_marker = current_marker
                            current_marker = map_widget.set_marker(curr_lat, curr_lon, icon=plane_photo)
                            
                            if old_marker: old_marker.delete()
                            
                            root.update_idletasks()
                            root.update()
                            # Bekleme süresini 0.005 yaptık (Gözle görülür bir hızlanma)
                            time.sleep(0.005) 
                else:
                    cost_label.config(text="Hata: Koordinat verisi eksik!", fg="red")
        except Exception as e:
            print(f"Hata: {e}")
tk.Button(input_panel, text="ROTAYI ÇİZ ✈", command=find_route_action, bg="#28a745", fg="white", font=("Arial", 9, "bold")).grid(row=0, column=4, padx=15)
root.mainloop()