<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreAnimalRequest;
use App\Http\Requests\UpdateAnimalRequest;
use App\Models\Animal;
use App\Models\Category;
use App\Models\ConservationStatus;
use App\Models\Habitat;
use App\Services\DatabaseSyncService;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class AnimalController extends Controller
{
    /**
     * Halaman Tabel Kelola Data Satwa (CRUD View)
     */
    public function index()
    {
        $animals = Animal::with(['category', 'status', 'habitat'])
            ->orderBy('id', 'ASC')
            ->get();

        return view('pages.manage', compact('animals'));
    }

    /**
     * Tampilkan formulir tambah satwa baru
     */
    public function create()
    {
        $categories = Category::orderBy('nama_kategori', 'ASC')->get();
        $statuses = ConservationStatus::orderBy('id', 'ASC')->get();
        $habitats = Habitat::orderBy('nama_habitat', 'ASC')->get();

        return view('pages.create', compact('categories', 'statuses', 'habitats'));
    }

    /**
     * Simpan data satwa baru ke database
     */
    public function store(StoreAnimalRequest $request)
    {
        $data = $request->validated();

        // 1. Tangani Upload File Gambar jika ada
        if ($request->hasFile('foto_file') && $request->file('foto_file')->isValid()) {
            $file = $request->file('foto_file');
            $filename = Str::random(8).'_'.time().'.'.$file->getClientOriginalExtension();
            $file->move(public_path('uploads'), $filename);
            $data['foto_url'] = '/uploads/'.$filename;
        }

        unset($data['foto_file']);

        // Pastikan urutan ID selalu rapi tanpa celah nomor
        self::resequenceIds();
        $nextId = (Animal::max('id') ?? 0) + 1;
        $data['id'] = $nextId;

        $animal = Animal::create($data);

        try {
            DB::statement('ALTER TABLE animals AUTO_INCREMENT = '.($nextId + 1));
        } catch (\Throwable $e) {
            // Abaikan jika non-MySQL
        }

        // Sinkronisasi otomatis ke faunaguard_schema.sql & GitHub
        DatabaseSyncService::syncToGitHub("feat(satwa): tambah satwa '{$animal->nama_lokal}' otomatis via Laravel");

        return redirect()->route('animals.manage')
            ->with('success', "Data satwa '{$animal->nama_lokal}' berhasil ditambahkan ke database!");
    }

    /**
     * Tampilkan formulir ubah data satwa
     */
    public function edit(Animal $animal)
    {
        $categories = Category::orderBy('nama_kategori', 'ASC')->get();
        $statuses = ConservationStatus::orderBy('id', 'ASC')->get();
        $habitats = Habitat::orderBy('nama_habitat', 'ASC')->get();

        return view('pages.edit', compact('animal', 'categories', 'statuses', 'habitats'));
    }

    /**
     * Perbarui data satwa di database
     */
    public function update(UpdateAnimalRequest $request, Animal $animal)
    {
        $data = $request->validated();

        // Tangani Upload File Gambar jika ada file baru diunggah
        if ($request->hasFile('foto_file') && $request->file('foto_file')->isValid()) {
            $file = $request->file('foto_file');
            $filename = Str::random(8).'_'.time().'.'.$file->getClientOriginalExtension();
            $file->move(public_path('uploads'), $filename);
            $data['foto_url'] = '/uploads/'.$filename;
        } elseif (empty($data['foto_url'])) {
            // Pertahankan foto lama jika URL dikosongkan dan tidak ada file baru
            $data['foto_url'] = $animal->foto_url;
        }

        unset($data['foto_file']);

        $animal->update($data);

        // Sinkronisasi otomatis ke faunaguard_schema.sql & GitHub
        DatabaseSyncService::syncToGitHub("feat(satwa): perbarui satwa '{$animal->nama_lokal}' otomatis via Laravel");

        return redirect()->route('animals.manage')
            ->with('success', "Data satwa '{$animal->nama_lokal}' berhasil diperbarui!");
    }

    /**
     * Hapus data satwa dari database
     */
    public function destroy(Animal $animal)
    {
        $nama = $animal->nama_lokal;
        $animal->delete();

        // Susun ulang ID satwa yang tersisa agar tetap berurutan (1, 2, 3, ...)
        self::resequenceIds();

        // Sinkronisasi otomatis ke faunaguard_schema.sql & GitHub
        DatabaseSyncService::syncToGitHub("feat(satwa): hapus satwa '{$nama}' otomatis via Laravel");

        return redirect()->route('animals.manage')
            ->with('info', "Data satwa '{$nama}' berhasil dihapus dari database.");
    }

    /**
     * Menyusun ulang ID satwa agar selalu berurutan (1, 2, 3, ...) tanpa celah nomor.
     */
    public static function resequenceIds(): void
    {
        $animals = Animal::orderBy('id', 'ASC')->get();
        $counter = 1;
        foreach ($animals as $item) {
            if ($item->id !== $counter) {
                Animal::where('id', $item->id)->update(['id' => $counter]);
            }
            $counter++;
        }

        try {
            DB::statement("ALTER TABLE animals AUTO_INCREMENT = {$counter}");
        } catch (\Throwable $e) {
            // Abaikan jika non-MySQL
        }
    }
}
