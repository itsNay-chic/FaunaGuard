<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Category extends Model
{
    use HasFactory;

    protected $fillable = [
        'nama_kategori',
        'deskripsi',
    ];

    /**
     * Relasi ke model Satwa (One-to-Many).
     */
    public function animals(): HasMany
    {
        return $this->hasMany(Animal::class, 'category_id');
    }
}

