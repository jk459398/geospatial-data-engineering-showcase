-- 1. Tworzenie tabel z kolumną na dane przestrzenne (GEOMETRY)
CREATE TABLE automaty_paczkowe (
    id VARCHAR(10) PRIMARY KEY,
    lokalizacja GEOMETRY(Point, 4326) -- 4326 to identyfikator systemu GPS (WGS84)
);

CREATE TABLE adresy_klientow (
    id_klienta INT PRIMARY KEY,
    adres_geometria GEOMETRY(Point, 4326)
);

-- 2. Dodanie indeksów przestrzennych 
CREATE INDEX idx_automaty_geom ON automaty_paczkowe USING GIST (lokalizacja);
CREATE INDEX idx_adresy_geom ON adresy_klientow USING GIST (adres_geometria);

-- 3. Wrzucenie przykładowych danych
INSERT INTO automaty_paczkowe (id, lokalizacja) VALUES 
('WAW01', ST_SetSRID(ST_MakePoint(21.0122, 52.2297), 4326)),
('WAW02', ST_SetSRID(ST_MakePoint(21.0200, 52.2300), 4326)),
('KRK01', ST_SetSRID(ST_MakePoint(19.9450, 50.0647), 4326));

INSERT INTO adresy_klientow (id_klienta, adres_geometria) VALUES 
(1001, ST_SetSRID(ST_MakePoint(21.0150, 52.2290), 4326)); -- Adres w Warszawie

-- 4. ZAPYTANIE GŁÓWNE: Znajdź 2 najbliższe automaty dla klienta nr 1001
SELECT 
    a.id AS maszyna_id,
    ROUND(ST_Distance(
        k.adres_geometria::geography, 
        a.lokalizacja::geography
    )::numeric, 2) AS odleglosc_w_metrach
FROM 
    adresy_klientow k
JOIN LATERAL (
    SELECT *
    FROM automaty_paczkowe
    ORDER BY k.adres_geometria <-> lokalizacja
    LIMIT 5   
) a ON TRUE
WHERE 
    k.id_klienta = 1001
ORDER BY 
    odleglosc_w_metrach
LIMIT 2;