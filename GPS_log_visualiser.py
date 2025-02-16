import pandas as pd
import folium
import time as t
import os
import keyboard

print("GPS log visualiser")
print("Pro ukončení programu stiskněte CTRL+C")
required_columns = "GPS.lat, GPS.lon a Altitude"

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def load_telemetry(file_path):
    try:
        # Načíst telemetrii do dataframu
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        return None

def create_map(df, output_file="mapa_letu.html"):
    # Načíst šířku a délku z dataframu
    start_lat, start_lon = df.iloc[0][["GPS.lat", "GPS.lon"]]
    for index, row in df.iterrows():
        lat, lon, alt = row["GPS.lat"], row["GPS.lon"], row["Altitude"]
        if not is_numeric(lat) or not is_numeric(lon) or not is_numeric(alt):
            raise ValueError(f"Neplatné hodnoty na řádku {index+1} - GPS.lat: {lat}, GPS.lon: {lon}, Altitude: {alt}")

    # Vytvořit mapu
    flight_map = folium.Map(location=[start_lat, start_lon], zoom_start=14)
    # Začátek AI kódu
    flight_path = [(row['GPS.lat'], row['GPS.lon']) for _, row in df.iterrows()]
    folium.PolyLine(flight_path, color="blue", weight=2.5, opacity=1).add_to(flight_map)

    # Markery pro začátek a konec
    folium.Marker(flight_path[0], popup="Začátek", icon=folium.Icon(color="green")).add_to(flight_map)
    folium.Marker(flight_path[-1], popup="Konec", icon=folium.Icon(color="red")).add_to(flight_map)
    if flight_path[0] == flight_path[-1]:
        folium.Marker(flight_path[-1], popup="Začátek a konec", icon=folium.Icon(color="red")).add_to(flight_map)
    # Konec AI kódu
    # Načte nejvyšší hodnotu sloupce "Altitude"
    top_alt_row = df.loc[df["Altitude"].idxmax()]
    top_alt_lat, top_alt_lon, top_alt = top_alt_row[["GPS.lat", "GPS.lon", "Altitude"]]
    # Marker pro největší výšku
    folium.Marker(
        location=[top_alt_lat, top_alt_lon],
        popup=f"Největší výška: {round(top_alt, 2)}m",
        icon=folium.Icon(color="blue", icon="cloud")
    ).add_to(flight_map)
    # Uložit mapu do HTML souboru
    flight_map.save(output_file)
    print(f"\nMapa uložena do souboru {output_file}")

while True:
    try:
        filename = input("----------\nNázev souboru: ")
        # Kontrola jestli název souboru zahrnuje koncovku .csv
        if not filename.lower().endswith(".csv"):
            filename = filename + ".csv"
        file_path = filename
        if os.path.exists(filename):
            print(f"\nVybrán soubor {filename}")
            telemetry_data = load_telemetry(file_path)
            create_map(telemetry_data)
        else:
            print(f"\nSoubor {file_path} neexistuje")
            continue
    except KeyboardInterrupt:
        # Jen tak pro efekt
        print(f"\nVypínám program.")
        t.sleep(0.8)
        print(f"Vypínám program..")
        t.sleep(0.8)
        print(f"Vypínám program...")
        t.sleep(0.8)
        os._exit(0)
    except pd.errors.EmptyDataError:
        print(f"\nSoubor {file_path} je prázdný")
    except KeyError as ke:
        print(f"\nSoubor {file_path} neobsahuje požadované sloupce.")
        print(f"Požadované sloupce: {required_columns}")
    except ValueError as ve:
        print("\n" + str(ve))
        print(f"Požadované hodnoty ve sloupcích {required_columns} jsou číselné")
    except Exception as e:
        print(f"\nNastala chyba: {e}")