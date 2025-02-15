import pandas as pd
import folium
def load_telemetry(file_path):
    # Nacist telemetrii do dataframu
    df = pd.read_csv(file_path)
    return df

def create_map(df, output_file="mapa_letu.html"):
    # Nacist sirku a delku z dataframu
    start_lat, start_lon = df.iloc[0][["GPS.lat", "GPS.lon"]]
    
    # Vytvori mapu 
    flight_map = folium.Map(location=[start_lat, start_lon], zoom_start=14)
    # Zacatek AI kdu
    flight_path = [(row['GPS.lat'], row['GPS.lon']) for _, row in df.iterrows()]
    folium.PolyLine(flight_path, color="blue", weight=2.5, opacity=1).add_to(flight_map)
    
    # Markery pro zacatek a konec
    folium.Marker(flight_path[0], popup="Začátek", icon=folium.Icon(color="green")).add_to(flight_map)
    folium.Marker(flight_path[-1], popup="Konec", icon=folium.Icon(color="red")).add_to(flight_map)
    # Konec AI kodu
    # Nacte nejvyssi hodnotu sloupce "Altitude"
    top_alt_row = df.loc[df["Altitude"].idxmax()]
    top_alt_lat, top_alt_lon, top_alt = top_alt_row[["GPS.lat", "GPS.lon", "Altitude"]]
    # Marker pro nejvetsi vysku
    folium.Marker(
        location=[top_alt_lat, top_alt_lon],
        popup=f"Nejvetsi vyska: {round(top_alt, 2)}m",
        icon=folium.Icon(color="blue", icon="cloud")
        ).add_to(flight_map)
    # Ulozit mapu do HTML souboru
    flight_map.save(output_file)
    print(f"Mapa ulozena do souboru {output_file}")

while True:
    filename = input("Nazev souboru: ")
    # Kontrola jestli nazev souboru zahrnuje koncovku .csv
    if ".csv" not in filename:
        filename = filename + ".csv"
    print(filename)
    file_path = filename
    telemetry_data = load_telemetry(file_path)
    create_map(telemetry_data)
