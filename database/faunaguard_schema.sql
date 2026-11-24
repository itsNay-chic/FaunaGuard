-- =============================================================================
-- FaunaGuard: Database Relasional MySQL Konservasi Satwa Dilindungi Kalimantan
-- File ini diperbarui secara OTOMATIS saat data diubah melalui aplikasi web.
-- =============================================================================

CREATE DATABASE IF NOT EXISTS faunaguard_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE faunaguard_db;

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
    foto_url MEDIUMTEXT NULL,
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

INSERT INTO categories (id, nama_kategori, deskripsi) VALUES
(1, 'Mamalia', 'Hewan menyusui bertulang belakang yang berdarah panas, sebagian besar berhabitat di hutan tropis dan sungai Kalimantan.'),
(2, 'Aves', 'Kelompok burung dan unggas berbulu yang memiliki peran penting dalam penyebaran biji pohon hutan kanopi Kalimantan.'),
(3, 'Reptilia', 'Hewan melata berdarah dingin bersisik, mendiami rawa gambut dan perairan tawar Pulau Borneo.'),
(4, 'Sphyrnidae', 'Kelompok hiu martil (Chondrichthyes) bertulang rawan dengan struktur kepala khas (cephalofoil), mendiami perairan pesisir dan terumbu karang tropis.');

INSERT INTO conservation_statuses (id, kode, nama_status, warna_badge, tingkat_ancaman) VALUES
(1, 'CR', 'Critically Endangered (Kritis)', '#D98327', 'Sangat Kritis Menuju Kepunahan'),
(2, 'EN', 'Endangered (Terancam)', '#4A943E', 'Risiko Tinggi Kepunahan di Alam Liar'),
(3, 'VU', 'Vulnerable (Rentan)', '#186049', 'Menghadapi Risiko Kepunahan Masa Depan');

INSERT INTO habitats (id, nama_habitat, lokasi, tipe_ekosistem) VALUES
(1, 'Taman Nasional Tanjung Puting', 'Kotawaringin Barat, Kalimantan Tengah', 'Hutan Rawa Gambut & Hutan Tropis'),
(2, 'Taman Nasional Kutai', 'Kutai Timur & Bontang, Kalimantan Timur', 'Hutan Hujan Dataran Rendah & Bakau'),
(3, 'Hutan Lindung Kutai Barat', 'Kutai Barat, Kalimantan Timur', 'Hutan Hujan Tropis Pedalaman'),
(4, 'Taman Nasional Kayan Mentarang', 'Kalimantan Utara, Malinau', 'Hutan Hujan Pegunungan Dataran Tinggi'),
(5, 'Taman Nasional Betung Kerihun', 'Kapuas Hulu, Kalimantan Barat', 'Hutan Pegunungan & Perbukitan Batuan'),
(6, 'Taman Nasional Danau Sentarum', 'Kapuas Hulu, Kalimantan Barat', 'Lahan Basah & Hutan Rawa Gambut');

INSERT INTO animals (
    id, nama_lokal, nama_ilmiah, deskripsi, ancaman_utama,
    estimasi_populasi, category_id, status_id, habitat_id, foto_url
) VALUES
(
    1,
    'Orangutan Kalimantan',
    'Pongo pygmaeus',
    'Primata besar berbulu oranye kecokelatan yang menghabiskan 90% hidupnya di kanopi pohon. Merupakan "petani hutan" sejati karena perannya yang vital dalam menyebarkan biji-bijian pohon hutan hujan Kalimantan.',
    'Deforestasi masif akibat alih fungsi lahan sawit, kebakaran lahan gambut, serta fragmentasi habitat oleh jalur logistik tambang.',
    57000,
    1,
    1,
    1,
    'https://assets.promediateknologi.id/crop/0x0:0x0/1200x0/webp/photo/p1/776/2023/09/04/Orangutan-Kalimantan-2916502849.jpg'
),
(
    2,
    'Bekantan',
    'Nasalis larvatus',
    'Monyet endemik Pulau Borneo dengan ciri khas hidung panjang menggantung dan perut buncit. Mampu berenang dengan sangat baik melintasi rawa dan sungai karena memiliki selaput di sela-sela jarinya.',
    'Konversi hutan mangrove dan nipah pesisir menjadi tambak udang komersial, pencemaran air muara, serta perburuan liar sporadis.',
    16000,
    1,
    2,
    2,
    'https://img.freepik.com/premium-photo/bekantan-nasalis-larvatus_1013208-580.jpg'
),
(
    3,
    'Badak Kalimantan',
    'Dicerorhinus sumatrensis harrissoni',
    'Subspesies badak terkecil di dunia yang sangat pemalu dan soliter. Memiliki dua cula kecil dan tubuh berbulu kasar kemerahan. Merupakan mamalia darat paling langka di Kalimantan.',
    'Populasi yang sangat kecil dan terisolasi menyulitkan perkembangbiakan alami, ancaman jerat pemburu babi hutan, serta hilangnya koridor hutan jelajah.',
    15,
    1,
    1,
    3,
    'https://nomorsatukaltim.disway.id/upload/3a7ae0b37e9e91ef60222f829a1a3e4a.png'
),
(
    4,
    'Kucing Merah Kalimantan',
    'Catopuma badia',
    'Spesies kucing liar endemik Pulau Kalimantan yang sangat langka dan elusif, hingga sering dijuluki sebagai "hantu hutan" oleh para peneliti. Memiliki tubuh yang ramping dengan panjang sekitar 60–70 cm dan berat berkisar antara 3–4 kg.',
    'Deforestasi dan fragmentasi habitat, jerat liar, perburuan dan perdagangan ilegal, serta kepadatan populasi alami yang sangat rendah.',
    2200,
    1,
    2,
    4,
    'https://1001indonesia.net/asset/2021/03/Kucing-Merah-Kalimantan.jpg'
),
(
    5,
    'Enggang Gading',
    'Rhinoplax vigil',
    'Burung berukuran megah dengan bentang sayap hampir 2 meter dan helm/balung kepala padat berwarna merah menyala. Memiliki suara panggilan tawa khas yang menggema di seluruh hutan pedalaman Borneo.',
    'Perburuan liar brutal untuk mengambil balung padatnya (dijuluki gading merah bernilai tinggi di pasar gelap) serta penebangan pohon beringin/ara raksasa tempat bersarang.',
    4000,
    2,
    1,
    5,
    'https://tse3.mm.bing.net/th/id/OIP.LYLz50B9LE-9g4NSWSnH4gHaEK?r=0&rs=1&pid=ImgDetMain&o=7&rm=3'
),
(
    6,
    'Penyu Sisik',
    'Eretmochelys imbricata',
    'Memakan ubur-ubur supaya tidak overpopulasi',
    'Populasinya terus menurun akibat perburuan liar, eksploitasi cangkang, serta perusakan habitat',
    400,
    3,
    1,
    1,
    'https://th.bing.com/th/id/OIP.GXVve9prX2s_wgkyBAEEAQHaFN?w=235&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
),
(
    7,
    'Binturong',
    'Arctictis binturong penicillatus',
    'Berperan sebagai penyebar biji alami, pendukung keberlangsungan pohon ara (Ficus), penjaga dinamika tajuk hutan, bagian dari rantai ekologi hutan tropis, indikator kesehatan ekosistem, penopang keanekaragaman hayati.',
    'Hilangnya habitat',
    NULL,
    1,
    3,
    1,
    'https://th.bing.com/th/id/OIP.lH-4Ht6GAoFQkGHH-UiuegHaE8?w=248&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
),
(
    8,
    'Kuau Raja',
    'Argusianus argus',
    'penghuni lantai hutan dataran rendah yang menyebarkan biji, mengendalikan serangga tanah, membuka petak tanah lewat arena tarinya, dan menandakan hutan masih sehat.',
    'deforestasi dan fragmentasi hutan (akibat pembukaan perkebunan, pertambangan, dan kebakaran hutan) yang merusak habitatnya, serta perburuan liar menggunakan jerat untuk diambil daging, bulu sayap, maupun diperdagangkan secara ilegal.',
    NULL,
    2,
    3,
    4,
    'https://th.bing.com/th/id/OIP.wYzeZXraA3LOuHjFmIyFcgHaEK?w=320&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
),
(
    9,
    'Buaya Senyulong',
    'Tomistoma schlegelii',
    'buaya air tawar bermoncong ramping penghuni rawa gambut dan sungai pedalaman yang berperan sebagai predator puncak pengendali populasi ikan dan satwa semi-akuatik, insinyur ekosistem yang menjaga struktur dasar rawa lewat kubangan dan sarangnya, serta bioindikator alami kesehatan ekosistem gambut.',
    'kerusakan dan hilangnya habitat rawa gambut (akibat pembukaan perkebunan kelapa sawit, pengeringan lahan gambut, dan kebakaran hutan), pencemaran serta pendangkalan sungai dari aktivitas pertambangan dan penebangan liar, terjerat alat tangkap ikan (bycatch) seperti jaring insang dan pancing nelayan, serta perburuan liar untuk diambil telur, daging, maupun diperdagangkan secara ilegal.',
    25000,
    3,
    2,
    6,
    'https://image.idntimes.com/post/20260408/1000067314_6682a4da-3387-4850-9550-a5700ff14b53.jpg'
);

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
