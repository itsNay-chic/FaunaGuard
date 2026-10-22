CREATE DATABASE IF NOT EXISTS faunaguard_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS animals;
DROP TABLE IF EXISTS habitats;
DROP TABLE IF EXISTS conservation_statuses;
DROP TABLE IF EXISTS categories;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_kategori VARCHAR(50) NOT NULL UNIQUE,
    deskripsi TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE conservation_statuses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode VARCHAR(10) NOT NULL UNIQUE,
    nama_status VARCHAR(50) NOT NULL,
    warna_badge VARCHAR(20) DEFAULT '#D98327',
    tingkat_ancaman VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE habitats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_habitat VARCHAR(100) NOT NULL,
    lokasi VARCHAR(100) NOT NULL,
    tipe_ekosistem VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE animals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_lokal VARCHAR(100) NOT NULL,
    nama_ilmiah VARCHAR(100) NOT NULL,
    deskripsi TEXT NULL,
    ancaman_utama TEXT NULL,
    estimasi_populasi INT NULL,
    category_id INT NOT NULL,
    status_id INT NOT NULL,
    habitat_id INT NOT NULL,
    foto_url VARCHAR(500) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_animal_category 
        FOREIGN KEY (category_id) REFERENCES categories (id) 
        ON UPDATE CASCADE ON DELETE RESTRICT,
        
    CONSTRAINT fk_animal_status 
        FOREIGN KEY (status_id) REFERENCES conservation_statuses (id) 
        ON UPDATE CASCADE ON DELETE RESTRICT,
        
    CONSTRAINT fk_animal_habitat 
        FOREIGN KEY (habitat_id) REFERENCES habitats (id) 
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX idx_animals_nama ON animals (nama_lokal);
CREATE INDEX idx_animals_category ON animals (category_id);
CREATE INDEX idx_animals_status ON animals (status_id);
CREATE INDEX idx_animals_habitat ON animals (habitat_id);

INSERT INTO categories (nama_kategori, deskripsi) VALUES
('Mamalia', 'Hewan menyusui bertulang belakang yang berdarah panas, sebagian besar berhabitat di hutan tropis dan sungai Kalimantan.'),
('Aves', 'Kelompok burung dan unggas berbulu yang memiliki peran penting dalam penyebaran biji pohon hutan kanopi Kalimantan.'),
('Reptilia', 'Hewan melata berdarah dingin bersisik, mendiami rawa gambut dan perairan tawar Pulau Borneo.');

INSERT INTO conservation_statuses (kode, nama_status, warna_badge, tingkat_ancaman) VALUES
('CR', 'Critically Endangered (Kritis)', '#D98327', 'Sangat Kritis Menuju Kepunahan'),
('EN', 'Endangered (Terancam)', '#4A943E', 'Risiko Tinggi Kepunahan di Alam Liar'),
('VU', 'Vulnerable (Rentan)', '#186049', 'Menghadapi Risiko Kepunahan Masa Depan');

INSERT INTO habitats (nama_habitat, lokasi, tipe_ekosistem) VALUES
('Taman Nasional Tanjung Puting', 'Kotawaringin Barat, Kalimantan Tengah', 'Hutan Rawa Gambut & Hutan Tropis'),
('Taman Nasional Kutai', 'Kutai Timur & Bontang, Kalimantan Timur', 'Hutan Hujan Dataran Rendah & Bakau'),
('Hutan Lindung Kutai Barat', 'Kutai Barat, Kalimantan Timur', 'Hutan Hujan Tropis Pedalaman'),
('Daerah Aliran Sungai Mahakam', 'Kutai Kartanegara & Samarinda, Kaltim', 'Perairan Air Tawar & Danau Rawa'),
('Taman Nasional Betung Kerihun', 'Kapuas Hulu, Kalimantan Barat', 'Hutan Pegunungan & Perbukitan Batuan');

INSERT INTO animals (
    nama_lokal, 
    nama_ilmiah, 
    deskripsi, 
    ancaman_utama, 
    estimasi_populasi, 
    category_id, 
    status_id, 
    habitat_id, 
    foto_url
) VALUES
(
    'Orangutan Kalimantan',
    'Pongo pygmaeus',
    'Primata besar berbulu oranye kecokelatan yang menghabiskan 90% hidupnya di kanopi pohon. Merupakan "petani hutan" sejati karena perannya yang vital dalam menyebarkan biji-bijian pohon hutan hujan Kalimantan.',
    'Deforestasi masif akibat alih fungsi lahan sawit, kebakaran lahan gambut, serta fragmentasi habitat oleh jalur logistik tambang.',
    57000,
    1, 
    1, 
    1, 
    'https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Orang_Utan%2C_Semenggok_Forest_Reserve%2C_Sarawak%2C_Borneo%2C_Malaysia.JPG/640px-Orang_Utan%2C_Semenggok_Forest_Reserve%2C_Sarawak%2C_Borneo%2C_Malaysia.JPG'
),
(
    'Bekantan',
    'Nasalis larvatus',
    'Monyet endemik Pulau Borneo dengan ciri khas hidung panjang menggantung dan perut buncit. Mampu berenang dengan sangat baik melintasi rawa dan sungai karena memiliki selaput di sela-sela jarinya.',
    'Konversi hutan mangrove dan nipah pesisir menjadi tambak udang komersial, pencemaran air muara, serta perburuan liar sporadis.',
    16000,
    1, 
    2, 
    2, 
    'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Proboscis_monkey_%28Nasalis_larvatus%29_male_Labuk_Bay.jpg/640px-Proboscis_monkey_%28Nasalis_larvatus%29_male_Labuk_Bay.jpg'
),
(
    'Badak Kalimantan',
    'Dicerorhinus sumatrensis harrissoni',
    'Subspesies badak terkecil di dunia yang sangat pemalu dan soliter. Memiliki dua cula kecil dan tubuh berbulu kasar kemerahan. Merupakan mamalia darat paling langka di Kalimantan.',
    'Populasi yang sangat kecil dan terisolasi menyulitkan perkembangbiakan alami, ancaman jerat pemburu babi hutan, serta hilangnya koridor hutan jelajah.',
    15,
    1, -- Mamalia
    1, -- CR (Critically Endangered)
    3, -- Hutan Lindung Kutai Barat
    'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Dicerorhinus_sumatrensis.jpg/640px-Dicerorhinus_sumatrensis.jpg'
),
(
    'Pesut Mahakam',
    'Orcaella brevirostris',
    'Mamalia air tawar unik lumba-lumba sungai berkepala bulat tanpa paruh moncong. Hidup di perairan tawar Sungai Mahakam dan bernapas menghirup udara setiap beberapa menit sekali.',
    'Terjerat jaring insang nelayan (rengge), pencemaran limbah cair industri sawit dan tambang batubara, serta kebisingan lambung kapal ponton batubara.',
    67,
    1, -- Mamalia
    1, -- CR (Critically Endangered)
    4, -- DAS Sungai Mahakam
    'https://upload.wikimedia.org/wikipedia/commons/thumb/e/ee/Irrawaddy_dolphin.jpg/640px-Irrawaddy_dolphin.jpg'
),
(
    'Enggang Gading',
    'Rhinoplax vigil',
    'Burung berukuran megah dengan bentang sayap hampir 2 meter dan helm/balung kepala padat berwarna merah menyala. Memiliki suara panggilan tawa khas yang menggema di seluruh hutan pedalaman Borneo.',
    'Perburuan liar brutal untuk mengambil balung padatnya (dijuluki gading merah bernilai tinggi di pasar gelap) serta penebangan pohon beringin/ara raksasa tempat bersarang.',
    NULL,
    2, -- Aves
    1, -- CR (Critically Endangered)
    5, -- TN Betung Kerihun
    'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Helmeted_hornbill_%28Rhinoplax_vigil%29_-_Flickr_-_gregthebusker_%281%29.jpg/640px-Helmeted_hornbill_%28Rhinoplax_vigil%29_-_Flickr_-_gregthebusker_%281%29.jpg'
);

-- =============================================================================
-- 6. Query Pengujian untuk Verifikasi Langsung di MySQL Workbench
-- =============================================================================

-- Query Uji: Tampilkan semua satwa lengkap dengan kategori, status, dan habitatnya
SELECT 
    a.id,
    a.nama_lokal,
    a.nama_ilmiah,
    c.nama_kategori,
    s.kode AS status_iucn,
    s.nama_status,
    s.tingkat_ancaman,
    h.nama_habitat,
    h.lokasi AS habitat_lokasi,
    a.estimasi_populasi,
    a.ancaman_utama
FROM animals a
JOIN categories c ON a.category_id = c.id
JOIN conservation_statuses s ON a.status_id = s.id
JOIN habitats h ON a.habitat_id = h.id
ORDER BY a.id ASC;
