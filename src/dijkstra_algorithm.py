import heapq

def find_shortest_path(graph, start_node, end_node):
    # Başlangıç mesafelerini ayarla
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start_node] = 0
    
    # Rota takibi için sözlük
    previous_nodes = {node: None for node in graph.nodes()}
    
    # Priority Queue: (mesafe, düğüm)
    priority_queue = [(0, start_node)]
    
    print(f"\n--- [ALGORİTMA BAŞLATILDI] ---")
    print(f"Başlangıç: {start_node} -> Hedef: {end_node}")

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # ADIM ADIM İZLEME (Logging)
        print(f"\n[ZİYARET] Şu an {current_node} havalimanındayım. Güncel maliyet: {current_distance:.2f} km")

        if current_node == end_node:
            print(f"--- [HEDEF BULUNDU] {end_node} noktasına ulaşıldı! ---")
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.neighbors(current_node):
            # Arkadaşının kodunda 'weight' olarak tanımlanan mesafeyi alıyoruz
            weight = graph[current_node][neighbor].get('weight', 0)
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
                
                # ADIM ADIM İZLEME (Güncelleme mesajı)
                print(f"   -> Güncelleme: {neighbor} için daha kısa bir rota bulundu! Yeni mesafe: {distance:.2f} km")

    # Rota Geri Dönüşü (Path Reconstruction)
    path = []
    current = end_node
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    return path, distances[end_node]