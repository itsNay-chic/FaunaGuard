/**
 * FaunaGuard - Client-side Interactive Script
 * Menangani pemuatan data modal detail satwa, filter interaktif, 
 * dan konfirmasi aksi hapus database.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Inisialisasi Modal Detail Satwa
    const detailModalEl = document.getElementById('animalDetailModal');
    if (detailModalEl) {
        detailModalEl.addEventListener('show.bs.modal', async (event) => {
            const button = event.relatedTarget;
            const animalId = button.getAttribute('data-animal-id');

            // Ambil elemen modal
            const titleEl = document.getElementById('modalTitle');
            const scientificEl = document.getElementById('modalScientific');
            const statusBadgeEl = document.getElementById('modalStatusBadge');
            const categoryEl = document.getElementById('modalCategory');
            const habitatEl = document.getElementById('modalHabitat');
            const habitatLocationEl = document.getElementById('modalHabitatLocation');
            const ecosystemEl = document.getElementById('modalEcosystem');
            const populationEl = document.getElementById('modalPopulation');
            const descEl = document.getElementById('modalDescription');
            const threatsEl = document.getElementById('modalThreats');
            const imgEl = document.getElementById('modalImage');

            // Reset tampilan ke status loading
            titleEl.textContent = 'Memuat Informasi...';
            scientificEl.textContent = '';
            descEl.textContent = 'Sedang mengambil data dari database MySQL...';
            threatsEl.textContent = '-';

            try {
                const response = await fetch(`/api/animals/${animalId}`);
                if (!response.ok) throw new Error('Data satwa tidak ditemukan');
                const data = await response.json();

                // Isi data ke modal
                titleEl.textContent = data.nama_lokal;
                scientificEl.textContent = data.nama_ilmiah;
                categoryEl.textContent = data.nama_kategori;
                habitatEl.textContent = data.nama_habitat;
                habitatLocationEl.textContent = data.habitat_lokasi;
                ecosystemEl.textContent = data.tipe_ekosistem;
                descEl.textContent = data.deskripsi || 'Belum ada deskripsi profil.';
                threatsEl.textContent = data.ancaman_utama || 'Tidak ada data ancaman khusus.';

                if (data.estimasi_populasi) {
                    populationEl.textContent = `± ${Number(data.estimasi_populasi).toLocaleString('id-ID')} individu di alam liar`;
                } else {
                    populationEl.textContent = 'Tren populasi kritis / data belum terdata pasti';
                }

                // Lencana status IUCN
                statusBadgeEl.textContent = `${data.status_kode} • ${data.nama_status}`;
                statusBadgeEl.style.backgroundColor = data.warna_badge || '#D98327';

                // Gambar
                if (data.foto_url) {
                    imgEl.src = data.foto_url;
                    imgEl.alt = data.nama_lokal;
                } else {
                    imgEl.src = '/static/img/placeholder.svg';
                }
            } catch (err) {
                titleEl.textContent = 'Gagal Memuat';
                descEl.textContent = 'Terjadi kesalahan saat memuat detail informasi satwa.';
                console.error(err);
            }
        });
    }

    // 2. Fallback gambar otomatis jika URL tidak dapat diakses
    document.querySelectorAll('img').forEach(img => {
        img.addEventListener('error', function() {
            this.onerror = null;
            this.src = '/static/img/placeholder.svg';
        });
    });
});

/**
 * Fungsi Konfirmasi Hapus Data Satwa
 */
function confirmDelete(animalName) {
    return confirm(`Apakah Anda yakin ingin menghapus data satwa "${animalName}" dari database MySQL FaunaGuard? Tindakan ini tidak dapat dibatalkan.`);
}
