@extends('layouts.app')

@section('title', 'Login Admin — FaunaGuard')

@section('content')
<div class="container my-5">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <!-- Kartu Login Admin -->
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden">
                <div class="card-header text-white text-center p-4" style="background-color: var(--fg-primary);">
                    <i class="bi bi-shield-lock-fill text-warning fs-1 mb-2 d-inline-block"></i>
                    <h4 class="fw-bold mb-1">Masuk Pengelola FaunaGuard</h4>
                    <p class="small text-light opacity-75 mb-0">Autentikasi Admin untuk Manajemen Data Satwa</p>
                </div>

                <div class="card-body p-4 p-md-5">
                    <!-- Petunjuk Akun Demo untuk Penguji / Dosen -->
                    <div class="alert alert-info py-2 px-3 mb-4 rounded-3 small">
                        <i class="bi bi-info-circle-fill me-1"></i> <strong>Akun Admin Default:</strong><br>
                        Email: <code>admin@faunaguard.org</code><br>
                        Sandi: <code>admin123</code>
                    </div>

                    @if ($errors->any())
                        <div class="alert alert-danger py-2 px-3 mb-4 rounded-3 small">
                            <i class="bi bi-exclamation-triangle-fill me-1"></i>
                            {{ $errors->first() }}
                        </div>
                    @endif

                    <form method="POST" action="{{ route('login.perform') }}">
                        @csrf

                        <!-- Input Email -->
                        <div class="mb-3">
                            <label class="form-label small fw-bold text-dark">Alamat Email</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-envelope"></i></span>
                                <input 
                                    type="email" 
                                    name="email" 
                                    class="form-control @error('email') is-invalid @enderror" 
                                    placeholder="nama@email.com" 
                                    value="{{ old('email', 'admin@faunaguard.org') }}" 
                                    required 
                                    autofocus
                                >
                            </div>
                            @error('email')
                                <div class="invalid-feedback d-block">{{ $message }}</div>
                            @enderror
                        </div>

                        <!-- Input Password -->
                        <div class="mb-3">
                            <label class="form-label small fw-bold text-dark">Kata Sandi</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="bi bi-key"></i></span>
                                <input 
                                    type="password" 
                                    name="password" 
                                    class="form-control @error('password') is-invalid @enderror" 
                                    placeholder="••••••••" 
                                    value="admin123" 
                                    required
                                >
                            </div>
                            @error('password')
                                <div class="invalid-feedback d-block">{{ $message }}</div>
                            @enderror
                        </div>

                        <!-- Remember Me -->
                        <div class="mb-4 form-check">
                            <input type="checkbox" name="remember" class="form-check-input" id="rememberMe" checked>
                            <label class="form-check-label small text-muted" for="rememberMe">
                                Ingat sesi saya di perangkat ini
                            </label>
                        </div>

                        <!-- Tombol Submit -->
                        <button type="submit" class="btn btn-fg-primary w-100 rounded-pill py-2 shadow-sm fw-bold">
                            <i class="bi bi-box-arrow-in-right me-1"></i> Masuk Sekarang
                        </button>
                    </form>
                </div>

                <div class="card-footer bg-light text-center py-3 border-0">
                    <small class="text-muted">
                        Kembali ke <a href="{{ route('beranda') }}" class="text-decoration-none fw-bold" style="color: var(--fg-secondary);">Halaman Beranda</a>
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection

