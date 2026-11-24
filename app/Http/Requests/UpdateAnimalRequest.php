<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdateAnimalRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'nama_lokal' => 'required|string|max:100',
            'nama_ilmiah' => 'required|string|max:100',
            'category_id' => 'required|exists:categories,id',
            'status_id' => 'required|exists:conservation_statuses,id',
            'habitat_id' => 'required|exists:habitats,id',
            'estimasi_populasi' => 'nullable|integer|min:0',
            'deskripsi' => 'nullable|string',
            'ancaman_utama' => 'nullable|string',
            'foto_url' => 'nullable|string',
            'foto_file' => 'nullable|image|mimes:jpeg,png,jpg,webp,gif|max:16384',
        ];
    }

    public function messages(): array
    {
        return [
            'nama_lokal.required' => 'Nama lokal satwa wajib diisi.',
            'nama_ilmiah.required' => 'Nama ilmiah satwa wajib diisi.',
            'category_id.required' => 'Pilih kategori taksonomi satwa.',
            'status_id.required' => 'Pilih status keterancaman IUCN.',
            'habitat_id.required' => 'Pilih kawasan habitat perlindungan.',
            'foto_file.image' => 'File yang diunggah harus berupa gambar.',
            'foto_file.max' => 'Ukuran gambar maksimal adalah 16 MB.',
        ];
    }
}

