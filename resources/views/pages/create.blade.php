@extends('layouts.app')

@section('title', 'Tambah Satwa Baru — FaunaGuard')

@section('content')
<div class="container my-5">
    <div class="row justify-content-center">
        <div class="col-lg-9">
            <!-- Navigasi Balik -->
            <div class="mb-3">
                <a href="{{ route('animals.manage') }}" class="text-decoration-none text-muted small">
                    <i class="bi bi-arrow-left me-1"></i> Kembali ke Tabel Kelola
                </a>
            </div>

            <!-- Kartu Form Tambah Satwa -->
            <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
                <div class="card-header text-white p-4" style="background-color: var(--fg-primary);">
                    <div class="d-flex align-items-center gap-2">
                        <i class="bi bi-plus-circle-fill text-warning fs-3"></i>
                        <div>
                            <h4 class="fw-bold mb-0">Input Data Satwa Baru</h4>
                            <small class="text-light opacity-75">
                                Menambahkan baris baru ke tabel <code>animals</code> via Laravel Eloquent ORM.
                            </small>
                        </div>
                    </div>
                </div>

                <div class="card-body p-4 p-md-5">
                    @if ($errors->any())
                        <div class="alert alert-danger mb-4 shadow-sm">
                            <h6 class="fw-bold mb-2"><i class="bi bi-exclamation-triangle-fill me-1"></i> Terjadi Kesalahan Input:</h6>
                            <ul class="mb-0 small ps-3">
                                @foreach ($errors->all() as $error)
                                    <li>{{ $error }}</li>
                                @endforeach
                            </ul>
                        </div>
                    @endif

                    <form method="POST" action="{{ route('animals.store') }}" enctype="multipart/form-data">
                        @csrf

                        <!-- Baris 1: Nama Satwa -->
                        <div class="row g-3 mb-3">
                            <div class="col-md-6">
                                <label class="form-label fw-bold text-dark">
                                    Nama Lokal / Populer <span class="text-danger">*</span>
                                </label>
                                <input type="text" name="nama_lokal" class="form-control @error('nama_lokal') is-invalid @enderror" placeholder="Contoh: Orangutan Kalimantan" value="{{ old('nama_lokal') }}" required>
                                @error('nama_lokal')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                            <div class="col-md-6">
                                <label class="form-label fw-bold text-dark">
                                    Nama Ilmiah (Latin) <span class="text-danger">*</span>
                                </label>
                                <input type="text" name="nama_ilmiah" class="form-control fst-italic @error('nama_ilmiah') is-invalid @enderror" placeholder="Contoh: Pongo pygmaeus" value="{{ old('nama_ilmiah') }}" required>
                                @error('nama_ilmiah')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                        </div>

                        <!-- Baris 2: Relasi Foreign Key (Categories, Status, Habitat) -->
                        <div class="p-3 rounded-3 mb-3" style="background-color: #f7f6ec; border: 1px dashed var(--fg-card-border);">
                            <h6 class="fw-bold mb-3" style="color: var(--fg-primary);">
                                <i class="bi bi-diagram-3-fill me-1"></i> Relasi Tabel Master (Foreign Keys)
                            </h6>
                            <div class="row g-3">
                                <!-- Kategori -->
                                <div class="col-md-4">
                                    <label class="form-label small fw-bold text-dark">
                                        Kategori (category_id) <span class="text-danger">*</span>
                                    </label>
                                    <select name="category_id" class="form-select @error('category_id') is-invalid @enderror" required>
                                        <option value="">-- Pilih Kategori --</option>
                                        @foreach($categories as $c)
                                            <option value="{{ $c->id }}" {{ old('category_id') == $c->id ? 'selected' : '' }}>
                                                {{ $c->nama_kategori }}
                                            </option>
                                        @endforeach
                                    </select>
                                    @error('category_id')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>

                                <!-- Status Konservasi -->
                                <div class="col-md-4">
                                    <label class="form-label small fw-bold text-dark">
                                        Status IUCN (status_id) <span class="text-danger">*</span>
                                    </label>
                                    <select name="status_id" class="form-select @error('status_id') is-invalid @enderror" required>
                                        <option value="">-- Pilih Status --</option>
                                        @foreach($statuses as $s)
                                            <option value="{{ $s->id }}" {{ old('status_id') == $s->id ? 'selected' : '' }}>
                                                {{ $s->kode }} - {{ $s->nama_status }}
                                            </option>
                                        @endforeach
                                    </select>
                                    @error('status_id')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>

                                <!-- Habitat -->
                                <div class="col-md-4">
                                    <label class="form-label small fw-bold text-dark">
                                        Kawasan Habitat (habitat_id) <span class="text-danger">*</span>
                                    </label>
                                    <select name="habitat_id" class="form-select @error('habitat_id') is-invalid @enderror" required>
                                        <option value="">-- Pilih Habitat --</option>
                                        @foreach($habitats as $h)
                                            <option value="{{ $h->id }}" {{ old('habitat_id') == $h->id ? 'selected' : '' }}>
                                                {{ $h->nama_habitat }}
                                            </option>
                                        @endforeach
                                    </select>
                                    @error('habitat_id')
                                        <div class="invalid-feedback">{{ $message }}</div>
                                    @enderror
                                </div>
                            </div>
                        </div>

                        <!-- Baris 3: Estimasi Populasi -->
                        <div class="row g-3 mb-3">
                            <div class="col-md-6">
                                <label class="form-label fw-bold text-dark">Estimasi Populasi di Alam</label>
                                <div class="input-group">
                                    <span class="input-group-text"><i class="bi bi-people"></i></span>
                                    <input type="number" name="estimasi_populasi" class="form-control @error('estimasi_populasi') is-invalid @enderror" placeholder="Contoh: 57000 (kosongkan jika tidak pasti)" value="{{ old('estimasi_populasi') }}">
                                </div>
                                <small class="text-muted">Masukkan angka bulat tanpa tanda baca.</small>
                                @error('estimasi_populasi')
                                    <div class="invalid-feedback d-block">{{ $message }}</div>
                                @enderror
                            </div>
                        </div>

                        <!-- Section Foto Satwa: Pilihan Upload atau URL dengan Live Preview -->
                        <div class="p-3 rounded-3 mb-3 border bg-light">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <label class="form-label fw-bold text-dark mb-0">
                                    <i class="bi bi-camera-fill text-success me-1"></i> Foto Satwa
                                </label>
                                <span class="badge bg-secondary-subtle text-secondary small">Upload File ATAU Tautan URL</span>
                            </div>
                            
                            <div class="row g-3 align-items-start">
                                <div class="col-lg-8">
                                    <!-- Pilihan 1: Upload File Langsung -->
                                    <div class="mb-3">
                                        <label class="form-label small fw-bold text-secondary mb-1">
                                            <i class="bi bi-upload me-1"></i> Opsi 1: Unggah Gambar dari Komputer / HP
                                        </label>
                                        <input type="file" name="foto_file" id="fotoFileInput" class="form-control @error('foto_file') is-invalid @enderror" accept="image/png, image/jpeg, image/jpg, image/webp, image/gif">
                                        <small class="text-muted d-block mt-1">Mendukung format JPG, PNG, WEBP, GIF (maks 16MB).</small>
                                        @error('foto_file')
                                            <div class="invalid-feedback">{{ $message }}</div>
                                        @enderror
                                    </div>

                                    <!-- Pilihan 2: URL Link -->
                                    <div class="mb-2">
                                        <label class="form-label small fw-bold text-secondary mb-1">
                                            <i class="bi bi-link-45deg me-1"></i> Opsi 2: Atau Masukkan Link / URL Gambar
                                        </label>
                                        <div class="input-group">
                                            <span class="input-group-text"><i class="bi bi-image"></i></span>
                                            <input type="text" name="foto_url" id="fotoUrlInput" class="form-control" placeholder="https://... (contoh: link gambar .jpg / .png)" value="{{ old('foto_url') }}">
                                        </div>
                                        <div class="alert alert-info py-2 px-3 mt-2 mb-0 small">
                                            <i class="bi bi-info-circle-fill me-1"></i> <strong>Tips Gambar Online:</strong> Jika mengambil dari internet/Google/berita, klik kanan pada gambar lalu pilih <em>"Salin Alamat Gambar" (Copy Image Address)</em>, bukan alamat halaman webnya.
                                        </div>
                                    </div>
                                </div>

                                <!-- Kolom Pratinjau Foto -->
                                <div class="col-lg-4 text-center">
                                    <label class="form-label small fw-bold text-muted mb-1">Pratinjau Foto</label>
                                    <div class="border rounded-3 overflow-hidden bg-white shadow-sm position-relative d-flex align-items-center justify-content-center" style="height: 180px;">
                                        <img id="imagePreview" src="{{ asset('img/placeholder.svg') }}" alt="Pratinjau Foto" class="img-fluid w-100 h-100" style="object-fit: cover;" referrerpolicy="no-referrer">
                                    </div>
                                    <small id="previewStatus" class="text-muted d-block mt-1">Belum ada foto dipilih</small>
                                </div>
                            </div>
                        </div>

                        <!-- Baris 4: Deskripsi & Ancaman Utama -->
                        <div class="mb-3">
                            <label class="form-label fw-bold text-dark">Peran & Profil Ekologis</label>
                            <textarea name="deskripsi" class="form-control" rows="3" placeholder="Jelaskan karakteristik unik satwa, peran dalam rantai makanan, atau perilaku alaminya di hutan Borneo...">{{ old('deskripsi') }}</textarea>
                        </div>

                        <div class="mb-4">
                            <label class="form-label fw-bold text-dark">
                                <i class="bi bi-exclamation-triangle-fill text-danger me-1"></i> Ancaman Utama Terhadap Kelangsungan Hidup
                            </label>
                            <textarea name="ancaman_utama" class="form-control" rows="2" placeholder="Sebutkan faktor utama pemicu penurunan populasi (misal: deforestasi sawit, perburuan liar, kebakaran gambut)...">{{ old('ancaman_utama') }}</textarea>
                        </div>

                        <!-- Tombol Aksi Submit -->
                        <div class="d-flex justify-content-end gap-2 pt-3 border-top">
                            <a href="{{ route('animals.manage') }}" class="btn btn-outline-secondary rounded-pill px-4">
                                Batal
                            </a>
                            <button type="submit" class="btn btn-fg-amber rounded-pill px-5 shadow-sm">
                                <i class="bi bi-cloud-arrow-up-fill me-1"></i> Simpan ke Database
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection

@push('scripts')
<script>
    // Live Image Preview Handler
    const urlInput = document.getElementById('fotoUrlInput');
    const fileInput = document.getElementById('fotoFileInput');
    const previewImg = document.getElementById('imagePreview');
    const statusText = document.getElementById('previewStatus');

    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    previewImg.src = event.target.result;
                    statusText.textContent = `File terpilih: ${file.name}`;
                };
                reader.readAsDataURL(file);
                if (urlInput) urlInput.value = '';
            }
        });
    }

    if (urlInput) {
        urlInput.addEventListener('input', function() {
            const url = this.value.trim();
            if (url) {
                previewImg.src = url;
                statusText.textContent = 'Memuat dari URL...';
                if (fileInput) fileInput.value = '';
            } else {
                previewImg.src = '{{ asset('img/placeholder.svg') }}';
                statusText.textContent = 'Belum ada foto dipilih';
            }
        });
    }
</script>
@endpush

