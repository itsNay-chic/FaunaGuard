<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Builder;

class Animal extends Model
{
    use HasFactory;

    protected $fillable = [
        'nama_lokal',
        'nama_ilmiah',
        'deskripsi',
        'ancaman_utama',
        'estimasi_populasi',
        'category_id',
        'status_id',
        'habitat_id',
        'foto_url',
    ];

    /**
     * Relasi ke model Category (Many-to-One).
     */
    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class, 'category_id');
    }

    /**
     * Relasi ke model ConservationStatus (Many-to-One).
     */
    public function status(): BelongsTo
    {
        return $this->belongsTo(ConservationStatus::class, 'status_id');
    }

    /**
     * Relasi ke model Habitat (Many-to-One).
     */
    public function habitat(): BelongsTo
    {
        return $this->belongsTo(Habitat::class, 'habitat_id');
    }

    /**
     * Scope Pencarian Berdasarkan Kata Kunci (Nama lokal, nama ilmiah, deskripsi).
     */
    public function scopeSearch(Builder $query, ?string $keyword): Builder
    {
        if (empty($keyword)) {
            return $query;
        }

        return $query->where(function ($q) use ($keyword) {
            $q->where('nama_lokal', 'LIKE', "%{$keyword}%")
              ->orWhere('nama_ilmiah', 'LIKE', "%{$keyword}%")
              ->orWhere('deskripsi', 'LIKE', "%{$keyword}%");
        });
    }

    /**
     * Scope Filter Kategori Satwa.
     */
    public function scopeFilterCategory(Builder $query, $categoryId): Builder
    {
        if (!empty($categoryId) && is_numeric($categoryId)) {
            return $query->where('category_id', $categoryId);
        }
        return $query;
    }

    /**
     * Scope Filter Status Konservasi IUCN.
     */
    public function scopeFilterStatus(Builder $query, $statusId): Builder
    {
        if (!empty($statusId) && is_numeric($statusId)) {
            return $query->where('status_id', $statusId);
        }
        return $query;
    }
}

