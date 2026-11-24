<?php

namespace App\Http\Controllers;

use App\Models\Animal;
use App\Models\Category;
use App\Models\ConservationStatus;
use App\Models\Habitat;
use App\Http\Requests\StoreAnimalRequest;
use App\Http\Requests\UpdateAnimalRequest;
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
            $filename = Str::random(8) . '_' . time() . '.' . $file->getClientOriginalExtension();
            $file->move(public_path('uploads'), $filename);
            $data['foto_url'] = '/uploads/' . $filename;
        }

        unset($data['foto_file']);

        $animal = Animal::create($data);

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
            $filename = Str::random(8) . '_' . time() . '.' . $file->getClientOriginalExtension();
            $file->move(public_path('uploads'), $filename);
            $data['foto_url'] = '/uploads/' . $filename;
        } elseif (empty($data['foto_url'])) {
            // Pertahankan foto lama jika URL dikosongkan dan tidak ada file baru
            $data['foto_url'] = $animal->foto_url;
        }

        unset($data['foto_file']);

        $animal->update($data);

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

        return redirect()->route('animals.manage')
            ->with('info', "Data satwa '{$nama}' berhasil dihapus dari database.");
    }
}

