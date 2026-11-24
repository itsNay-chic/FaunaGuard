<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Animal;
use App\Models\Category;
use App\Models\ConservationStatus;
use App\Models\Habitat;

class HomeController extends Controller
{
    /**
     * Halaman Beranda (Home / Suaka Edukasi Utama)
     */
    public function beranda()
    {
        $stats = [
            'total' => Animal::count(),
            'kritis' => Animal::whereHas('status', function ($query) {
                $query->where('kode', 'CR');
            })->count(),
            'habitat' => Animal::distinct('habitat_id')->count('habitat_id'),
            'kategori' => Category::count(),
        ];

        $featured_animals = Animal::with(['category', 'status', 'habitat'])
            ->orderByRaw("(status_id = 1) DESC")
            ->orderBy('id', 'ASC')
            ->take(3)
            ->get();

        return view('pages.beranda', compact('stats', 'featured_animals'));
    }

    /**
     * Halaman Katalog Satwa (Public Exploration & Search)
     */
    public function katalog(Request $request)
    {
        $categories = Category::orderBy('nama_kategori', 'ASC')->get();
        $statuses = ConservationStatus::orderBy('id', 'ASC')->get();

        $stats = [
            'total' => Animal::count(),
            'kritis' => Animal::whereHas('status', function ($query) {
                $query->where('kode', 'CR');
            })->count(),
            'habitat' => Animal::distinct('habitat_id')->count('habitat_id'),
        ];

        $animals = Animal::with(['category', 'status', 'habitat'])
            ->search($request->input('q'))
            ->filterCategory($request->input('category'))
            ->filterStatus($request->input('status'))
            ->orderBy('id', 'ASC')
            ->get();

        return view('pages.katalog', [
            'animals' => $animals,
            'categories' => $categories,
            'statuses' => $statuses,
            'stats' => $stats,
            'current_q' => $request->input('q', ''),
            'current_category' => $request->input('category', ''),
            'current_status' => $request->input('status', ''),
        ]);
    }

    /**
     * API Endpoint Detail Satwa (JSON untuk modal interaktif)
     */
    public function animalDetail($id)
    {
        $animal = Animal::with(['category', 'status', 'habitat'])->find($id);

        if (!$animal) {
            return response()->json(['error' => 'Satwa tidak ditemukan'], 404);
        }

        return response()->json([
            'id' => $animal->id,
            'nama_lokal' => $animal->nama_lokal,
            'nama_ilmiah' => $animal->nama_ilmiah,
            'deskripsi' => $animal->deskripsi,
            'ancaman_utama' => $animal->ancaman_utama,
            'estimasi_populasi' => $animal->estimasi_populasi,
            'foto_url' => $animal->foto_url,
            'nama_kategori' => $animal->category->nama_kategori ?? '-',
            'status_kode' => $animal->status->kode ?? '-',
            'nama_status' => $animal->status->nama_status ?? '-',
            'warna_badge' => $animal->status->warna_badge ?? '#D98327',
            'tingkat_ancaman' => $animal->status->tingkat_ancaman ?? '-',
            'nama_habitat' => $animal->habitat->nama_habitat ?? '-',
            'habitat_lokasi' => $animal->habitat->lokasi ?? '-',
            'tipe_ekosistem' => $animal->habitat->tipe_ekosistem ?? '-',
        ]);
    }
}

