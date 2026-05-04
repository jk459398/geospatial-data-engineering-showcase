import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# 1. Symulacja pobrania "surowych" danych (np. z bazy operacyjnej)
surowe_dane = pd.read_csv("../data/raw_lockers.csv")
surowe_dane = surowe_dane.dropna(subset=["lat", "lon"])

# 2. Transformacja: Tworzenie geometrii
geometria = [Point(xy) for xy in zip(surowe_dane['lon'], surowe_dane['lat'])]
gdf_maszyny = gpd.GeoDataFrame(surowe_dane, geometry=geometria)
gdf_maszyny.set_crs(epsg=4326, inplace=True) # EPSG:4326 to standardowy system GPS

# 3. Data Quality (Kontrola Jakości): Czy punkty są w Polsce?
min_lon, max_lon = 14.0, 24.2
min_lat, max_lat = 49.0, 54.9

# Filtrujemy tylko te poprawne
gdf_poprawne = gdf_maszyny.cx[min_lon:max_lon, min_lat:max_lat]

print(f"Odrzucono {len(gdf_maszyny) - len(gdf_poprawne)} maszyn z błędnymi współrzędnymi.")

# 4. Przetwarzanie: Obliczanie strefy zasięgu (Buffer)
# Przekształcamy do lokalnego układu dla Polski (EPSG:2180), który liczy w metrach, a nie stopniach!
gdf_poprawne_metry = gdf_poprawne.to_crs(epsg=2180)
gdf_poprawne_metry['strefa_500m'] = gdf_poprawne_metry.geometry.buffer(500)

gdf_poprawne_metry = gdf_poprawne_metry.set_geometry('strefa_500m')
gdf_poprawne_metry = gdf_poprawne_metry.drop(columns='geometry')  # usuwamy starą geometrię
gdf_poprawne_metry = gdf_poprawne_metry.rename_geometry('geometry')

# (opcjonalnie) wróć do WGS84, żeby GeoJSON był kompatybilny z mapami webowymi
gdf_poprawne_metry = gdf_poprawne_metry.to_crs(epsg=4326)

# 5. Zapis
gdf_poprawne_metry.to_file("../data/processed_zones.geojson", driver="GeoJSON")

print("Zakończono procesowanie danych.")