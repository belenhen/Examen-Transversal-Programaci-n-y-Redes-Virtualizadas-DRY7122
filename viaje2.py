import math
import datetime

def obtener_coordenadas(ciudad):
    ciudades = {
        "Santiago": (-33.4489, -70.6693),
        "Buenos Aires": (-34.6037, -58.3816),
        "Valparaíso": (-33.0472, -71.6127),
        "Mendoza": (-32.8895, -68.8458)
    }
    return ciudades.get(ciudad)

def haversine(coord1, coord2):
    R = 6371  
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distancia_km = R * c
    distancia_millas = distancia_km * 0.621371  
    
    return distancia_km, distancia_millas

def calcular_duracion(distancia_km, medio_transporte):
    if medio_transporte == 'auto':
        velocidad = 80  
    elif medio_transporte == 'avion':
        velocidad = 800  
    else:
        velocidad = 5  

    duracion_horas = distancia_km / velocidad
    return datetime.timedelta(hours=duracion_horas)

def main():
    while True:
        print("Ingrese 's' para salir en cualquier momento.")
        
        origen = input("Ciudad de Origen: ").strip()
        if origen.lower() == 's':
            break
        
        destino = input("Ciudad de Destino: ").strip()
        if destino.lower() == 's':
            break
        
        coord_origen = obtener_coordenadas(origen)
        coord_destino = obtener_coordenadas(destino)
        
        if not coord_origen or not coord_destino:
            print("Una o ambas ciudades no están disponibles. Intente nuevamente.")
            continue
        
        distancia_km, distancia_millas = haversine(coord_origen, coord_destino)
        
        print("Elija el medio de transporte (auto, avion, caminando):")
        medio_transporte = input().strip().lower()
        if medio_transporte.lower() == 's':
            break
        
        duracion = calcular_duracion(distancia_km, medio_transporte)
        
        print(f"\nLa distancia entre {origen} y {destino} es de:")
        print(f"{distancia_km:.2f} kilómetros")
        print(f"{distancia_millas:.2f} millas")
        print(f"La duración del viaje es aproximadamente: {duracion}")
        print(f"Viaje desde {origen} hasta {destino} en {medio_transporte}\n")

if __name__ == "__main__":
    main()
