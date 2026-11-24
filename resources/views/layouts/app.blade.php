<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <!-- Mencegah pemblokiran hotlinking gambar dari Wikimedia / portal berita -->
    <meta name="referrer" content="no-referrer">
    <title>@yield('title', 'FaunaGuard — Suaka Informasi Satwa Dilindungi Kalimantan')</title>
    
    <!-- Bootstrap 5 CSS CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Bootstrap Icons CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
    <!-- FaunaGuard Custom Borneo Rainforest CSS -->
    <link rel="stylesheet" href="{{ asset('css/style.css') }}">
</head>
<body>

    <!-- 1. Navbar Utama -->
    <nav class="navbar navbar-expand-lg fg-navbar sticky-top">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center gap-2" href="{{ route('beranda') }}">
                <i class="bi bi-shield-shaded text-warning fs-3"></i>
                <span>Fauna</span>Guard
            </a>
            
            <button class="navbar-toggler text-white border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu">
                <i class="bi bi-list fs-2"></i>
            </button>

            <div class="collapse navbar-collapse" id="navMenu">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0 align-items-lg-center gap-2">
                    <li class="nav-item">
                        <a class="nav-link {{ request()->routeIs('beranda') ? 'active' : '' }}" href="{{ route('beranda') }}">
                            <i class="bi bi-house-door-fill me-1"></i> Beranda
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {{ request()->routeIs('katalog') ? 'active' : '' }}" href="{{ route('katalog') }}">
                            <i class="bi bi-grid-fill me-1"></i> Katalog Satwa
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {{ request()->routeIs('animals.*') ? 'active' : '' }}" href="{{ route('animals.manage') }}">
                            <i class="bi bi-database-fill-gear me-1"></i> Kelola Database (CRUD)
                        </a>
                    </li>

                    @auth
                        <li class="nav-item ms-lg-2 dropdown">
                            <a class="btn btn-outline-light btn-sm px-3 py-2 rounded-pill dropdown-toggle d-inline-flex align-items-center gap-2" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <i class="bi bi-person-circle text-warning"></i>
                                <span>{{ Auth::user()->name }}</span>
                            </a>
                            <ul class="dropdown-menu dropdown-menu-end shadow border-0 mt-2">
                                <li>
                                    <span class="dropdown-item-text small text-muted">Masuk sebagai: <strong>{{ Auth::user()->email }}</strong></span>
                                </li>
                                <li><hr class="dropdown-divider"></li>
                                <li>
                                    <a class="dropdown-item" href="{{ route('animals.create') }}">
                                        <i class="bi bi-plus-circle me-1 text-success"></i> Tambah Satwa Baru
                                    </a>
                                </li>
                                <li>
                                    <form action="{{ route('logout') }}" method="POST" class="d-inline">
                                        @csrf
                                        <button type="submit" class="dropdown-item text-danger">
                                            <i class="bi bi-box-arrow-right me-1"></i> Keluar (Logout)
                                        </button>
                                    </form>
                                </li>
                            </ul>
                        </li>
                    @else
                        <li class="nav-item ms-lg-2">
                            <a class="btn btn-outline-light btn-sm px-3 py-2 rounded-pill d-inline-flex align-items-center gap-1" href="{{ route('login') }}">
                                <i class="bi bi-lock-fill"></i> Login Admin
                            </a>
                        </li>
                    @endauth

                    <li class="nav-item ms-lg-2">
                        <a class="btn btn-fg-amber btn-sm px-3 py-2 rounded-pill d-inline-flex align-items-center gap-1 shadow-sm" href="{{ route('animals.create') }}">
                            <i class="bi bi-plus-circle-fill"></i> Tambah Satwa
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- 2. Flash Messages Alert -->
    <div class="container mt-3">
        @if(session('success'))
            <div class="alert alert-success alert-dismissible fade show shadow-sm" role="alert">
                <i class="bi bi-check-circle-fill me-2"></i> {{ session('success') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        @endif

        @if(session('info'))
            <div class="alert alert-info alert-dismissible fade show shadow-sm" role="alert">
                <i class="bi bi-info-circle-fill me-2"></i> {{ session('info') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        @endif

        @if(session('warning'))
            <div class="alert alert-warning alert-dismissible fade show shadow-sm" role="alert">
                <i class="bi bi-exclamation-triangle-fill me-2"></i> {{ session('warning') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        @endif

        @if(session('danger') || session('error'))
            <div class="alert alert-danger alert-dismissible fade show shadow-sm" role="alert">
                <i class="bi bi-x-circle-fill me-2"></i> {{ session('danger') ?? session('error') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        @endif
    </div>

    <!-- 3. Konten Utama Dinamis -->
    <main class="flex-grow-1">
        @yield('content')
    </main>

    <!-- 4. Footer Web -->
    <footer class="fg-footer">
        <div class="container">
            <div class="row gy-4 align-items-center">
                <div class="col-md-6 text-center text-md-start">
                    <h5 class="fw-bold mb-1 text-white">
                        <i class="bi bi-shield-shaded text-warning me-1"></i> FaunaGuard
                    </h5>
                    <p class="small mb-0 text-light opacity-75">
                        Portal Edukasi & Suaka Informasi Konservasi Satwa Dilindungi Kalimantan.
                    </p>
                </div>
                <div class="col-md-6 text-center text-md-end">
                    <div class="d-flex flex-wrap justify-content-center justify-content-md-end gap-3 small">
                        <a href="{{ route('beranda') }}">Beranda</a>
                        <span class="opacity-50 text-white">•</span>
                        <a href="{{ route('katalog') }}">Katalog Satwa</a>
                        <span class="opacity-50 text-white">•</span>
                        <a href="{{ route('animals.manage') }}">Kelola Database</a>
                    </div>
                </div>
            </div>
        </div>
    </footer>

    <!-- Bootstrap 5 JS Bundle CDN -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <!-- Custom Interactive JS -->
    <script src="{{ asset('js/main.js') }}"></script>
    @stack('scripts')
</body>
</html>

