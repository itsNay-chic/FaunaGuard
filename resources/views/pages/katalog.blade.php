@extends('layouts.app')

@section('title', 'Katalog Satwa Dilindungi Kalimantan — FaunaGuard')

@section('content')
<!-- 1. Hero Section Katalog -->
<section class="fg-hero">
    <div class="container">
        <div class="row align-items-center gy-4">
            <div class="col-lg-7">
                <nav aria-label="breadcrumb" class="mb-2">
                    <ol class="breadcrumb mb-0">
                        <li class="breadcrumb-item"><a href="{{ route('beranda') }}" class="text-white text-decoration-none opacity-75"><i class="bi bi-house-door me-1"></i>Beranda</a></li>
                        <li class="breadcrumb-item active text-warning" aria-current="page">Katalog Satwa</li>
                    </ol>
                </nav>
                <span class="badge px-3 py-2 rounded-pill mb-3" style="background-color: var(--fg-secondary); color: #fff;">
                    <i class="bi bi-grid-fill me-1"></i> Katalog & Eksplorasi Hayati
                </span>
                <h1 class="display-5 text-white mb-3">
                    Eksplorasi Satwa Unik & Dilindungi Kalimantan
                </h1>
                <p class="lead mb-4">
                    Jelajahi keanekaragaman fauna endemik Pulau Borneo. Gunakan bilah pencarian dan saringan taksonomi di bawah untuk menemukan profil spesies beserta status keterancaman IUCN berbasis Eloquent ORM.
                </p>
                <div class="d-flex flex-wrap gap-2">
                    <a href="#katalog" class="btn btn-fg-amber px-4 py-2 rounded-pill shadow-sm">
                        <i class="bi bi-search me-1"></i> Mulai Saring Satwa
                    </a>
                    <a href="{{ route('beranda') }}" class="btn btn-outline-light px-4 py-2 rounded-pill">
                        <i class="bi bi-info-circle me-1"></i> Tentang FaunaGuard
                    </a>
                </div>
            </div>
            
            <!-- Statistik Ringkas -->
            <div class="col-lg-5">
                <div class="row g-3">
                    <div class="col-6">
                        <div class="stat-pill text-center">
                            <div class="number">{{ $stats['total'] }}</div>
                            <div class="label mt-1">Spesies Tercatat</div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="stat-pill text-center" style="border-color: var(--fg-amber);">
                            <div class="number" style="color: var(--fg-amber);">{{ $stats['kritis'] }}</div>
                            <div class="label mt-1">Status Kritis (CR)</div>
                        </div>
                    </div>
                    <div class="col-12">
                        <div class="stat-pill d-flex align-items-center justify-content-between">
                            <div>
                                <div class="label">Kawasan Konservasi & Habitat</div>
                                <div class="number mt-1">{{ $stats['habitat'] }}</div>
                            </div>
                            <i class="bi bi-geo-alt-fill text-warning fs-1 opacity-75"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- 2. Bilah Pencarian & Filter Interaktif -->
<section class="container my-4" id="katalog">
    <div class="filter-card">
        <form method="GET" action="{{ route('katalog') }}#katalog" class="row g-3 align-items-end">
            <!-- Input Cari Nama -->
            <div class="col-md-5">
                <label class="form-label small fw-bold text-muted mb-1">
                    <i class="bi bi-search me-1"></i> Cari Satwa Kalimantan
                </label>
                <input 
                    type="text" 
                    name="q" 
                    class="form-control" 
                    placeholder="Contoh: Orangutan, Bekantan, Badak..." 
                    value="{{ $current_q }}"
                >
            </div>

            <!-- Filter Kategori -->
            <div class="col-md-3">
                <label class="form-label small fw-bold text-muted mb-1">
                    <i class="bi bi-tag-fill me-1"></i> Kategori Satwa
                </label>
                <select name="category" class="form-select">
                    <option value="">Semua Kategori</option>
                    @foreach($categories as $cat)
                        <option value="{{ $cat->id }}" {{ (string)$current_category === (string)$cat->id ? 'selected' : '' }}>
                            {{ $cat->nama_kategori }}
                        </option>
                    @endforeach
                </select>
            </div>

            <!-- Filter Status Konservasi -->
            <div class="col-md-2">
                <label class="form-label small fw-bold text-muted mb-1">
                    <i class="bi bi-shield-exclamation me-1"></i> Status IUCN
                </label>
                <select name="status" class="form-select">
                    <option value="">Semua Status</option>
                    @foreach($statuses as $st)
                        <option value="{{ $st->id }}" {{ (string)$current_status === (string)$st->id ? 'selected' : '' }}>
                            {{ $st->kode }} - {{ $st->nama_status }}
                        </option>
                    @endforeach
                </select>
            </div>

            <!-- Tombol Submit & Reset -->
            <div class="col-md-2 d-flex gap-2">
                <button type="submit" class="btn btn-fg-primary w-100">
                    <i class="bi bi-filter"></i> Saring
                </button>
                @if($current_q || $current_category || $current_status)
                    <a href="{{ route('katalog') }}#katalog" class="btn btn-outline-secondary" title="Reset Filter">
                        <i class="bi bi-arrow-counterclockwise"></i>
                    </a>
                @endif
            </div>
        </form>
    </div>
</section>

<!-- 3. Grid Kartu Informasi Satwa (Animal Cards) -->
<section class="container mb-5">
    <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="fw-bold mb-0" style="color: var(--fg-primary);">
            <i class="bi bi-collection-fill me-2"></i>Katalog Informasi Satwa
        </h4>
        <span class="badge text-bg-light border px-3 py-2 text-muted">
            Menampilkan <strong>{{ $animals->count() }}</strong> satwa
        </span>
    </div>

    @if($animals->count() > 0)
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
            @foreach($animals as $animal)
                <div class="col">
                    <div class="animal-card">
                        <!-- Wrapper Gambar Satwa & Lencana Status -->
                        <div class="animal-img-wrapper">
                            <span class="status-badge-overlay" style="background-color: {{ $animal->status->warna_badge ?? '#D98327' }};">
                                {{ $animal->status->kode ?? '-' }} • {{ $animal->status->nama_status ?? '-' }}
                            </span>
                            <img 
                                src="{{ $animal->foto_url ?: asset('img/placeholder.svg') }}" 
                                alt="{{ $animal->nama_lokal }}"
                                loading="lazy"
                                referrerpolicy="no-referrer"
                                onerror="this.onerror=null; this.src='{{ asset('img/placeholder.svg') }}';"
                            >
                        </div>

                        <!-- Isi Informasi Satwa -->
                        <div class="p-3 d-flex flex-column flex-grow-1">
                            <div class="d-flex justify-content-between align-items-center mb-1">
                                <span class="category-tag">
                                    <i class="bi bi-tag-fill me-1"></i>{{ $animal->category->nama_kategori ?? '-' }}
                                </span>
                                @if($animal->estimasi_populasi)
                                    <span class="small text-muted fw-bold">
                                        <i class="bi bi-people-fill me-1"></i>±{{ number_format($animal->estimasi_populasi, 0, ',', '.') }}
                                    </span>
                                @endif
                            </div>

                            <h5 class="animal-title">{{ $animal->nama_lokal }}</h5>
                            <div class="animal-scientific mb-2">{{ $animal->nama_ilmiah }}</div>

                            <p class="animal-desc mb-3">
                                {{ $animal->deskripsi ?: 'Belum ada deskripsi profil ekologis.' }}
                            </p>

                            <!-- Lokasi Kawasan Habitat -->
                            <div class="habitat-info mb-3 mt-auto">
                                <div class="fw-bold text-dark">
                                    <i class="bi bi-geo-alt-fill text-success me-1"></i>{{ $animal->habitat->nama_habitat ?? '-' }}
                                </div>
                                <div class="small text-muted">{{ $animal->habitat->lokasi ?? '-' }}</div>
                            </div>

                            <!-- Tombol Pop-up Detail Satwa -->
                            <button 
                                type="button" 
                                class="btn btn-fg-outline w-100 rounded-pill btn-sm py-2"
                                data-bs-toggle="modal" 
                                data-bs-target="#animalDetailModal" 
                                data-animal-id="{{ $animal->id }}"
                            >
                                <i class="bi bi-info-circle-fill me-1"></i> Pelajari Selengkapnya
                            </button>
                        </div>
                    </div>
                </div>
            @endforeach
        </div>
    @else
        <!-- Keadaan Kosong (Empty State Filter) -->
        <div class="card p-5 text-center border-0 shadow-sm rounded-4 my-4">
            <div class="mb-3">
                <i class="bi bi-search text-muted opacity-50" style="font-size: 3rem;"></i>
            </div>
            <h5 class="fw-bold text-dark">Tidak Ada Satwa yang Sesuai</h5>
            <p class="text-muted small mb-3">
                Tidak ditemukan satwa dengan kata kunci atau saringan kategori yang Anda pilih.
            </p>
            <div>
                <a href="{{ route('katalog') }}" class="btn btn-fg-primary rounded-pill px-4 btn-sm">
                    <i class="bi bi-arrow-counterclockwise me-1"></i> Muat Ulang Katalog
                </a>
            </div>
        </div>
    @endif
</section>

<!-- 4. Modal Pop-up: Detail Edukatif Satwa -->
<div class="modal fade" id="animalDetailModal" tabindex="-1" aria-labelledby="modalTitle" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content border-0 shadow-lg overflow-hidden">
            <!-- Modal Header -->
            <div class="modal-header text-white" style="background-color: var(--fg-primary);">
                <div class="d-flex align-items-center gap-2">
                    <i class="bi bi-shield-check text-warning fs-4"></i>
                    <div>
                        <h5 class="modal-title fw-bold mb-0" id="modalTitle">Detail Satwa</h5>
                        <small id="modalScientific" class="fst-italic opacity-75"></small>
                    </div>
                </div>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>

            <!-- Modal Body -->
            <div class="modal-body p-4">
                <div class="row g-4">
                    <!-- Foto Satwa Besar -->
                    <div class="col-md-5">
                        <div class="rounded-3 overflow-hidden shadow-sm mb-3">
                            <img id="modalImage" src="" alt="" class="img-fluid w-100" style="height: 240px; object-fit: cover;" referrerpolicy="no-referrer" onerror="this.onerror=null; this.src='{{ asset('img/placeholder.svg') }}';">
                        </div>
                        <div class="d-flex flex-column gap-2">
                            <span id="modalStatusBadge" class="badge py-2 px-3 text-white text-center fw-bold"></span>
                            <div class="p-2 rounded bg-light border text-center">
                                <small class="text-muted d-block">Sisa Estimasi Populasi</small>
                                <span id="modalPopulation" class="fw-bold text-dark"></span>
                            </div>
                        </div>
                    </div>

                    <!-- Informasi Detail & Ancaman -->
                    <div class="col-md-7">
                        <div class="mb-3">
                            <h6 class="fw-bold text-muted small text-uppercase mb-1">
                                <i class="bi bi-tag-fill me-1 text-success"></i> Kelompok Taksonomi
                            </h6>
                            <p id="modalCategory" class="fw-bold text-dark mb-0"></p>
                        </div>

                        <div class="mb-3">
                            <h6 class="fw-bold text-muted small text-uppercase mb-1">
                                <i class="bi bi-journal-text me-1 text-success"></i> Peran & Profil Ekologis
                            </h6>
                            <p id="modalDescription" class="text-secondary small mb-0 lh-base"></p>
                        </div>

                        <!-- Kotak Peringatan Ancaman Utama -->
                        <div class="p-3 rounded-3 mb-3" style="background-color: #fff6eb; border-left: 4px solid var(--fg-amber);">
                            <h6 class="fw-bold text-danger small text-uppercase mb-1">
                                <i class="bi bi-exclamation-triangle-fill me-1"></i> Ancaman Utama Kepunahan
                            </h6>
                            <p id="modalThreats" class="text-dark small mb-0 lh-base"></p>
                        </div>

                        <div>
                            <h6 class="fw-bold text-muted small text-uppercase mb-1">
                                <i class="bi bi-geo-alt-fill me-1 text-success"></i> Kawasan Konservasi & Habitat
                            </h6>
                            <div class="p-2 rounded bg-light border small">
                                <strong id="modalHabitat" class="text-dark d-block"></strong>
                                <span id="modalHabitatLocation" class="text-muted d-block"></span>
                                <span id="modalEcosystem" class="badge bg-secondary-subtle text-secondary-emphasis mt-1"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Modal Footer -->
            <div class="modal-footer bg-light py-2">
                <button type="button" class="btn btn-secondary rounded-pill btn-sm px-4" data-bs-dismiss="modal">
                    Tutup
                </button>
            </div>
        </div>
    </div>
</div>
@endsection

