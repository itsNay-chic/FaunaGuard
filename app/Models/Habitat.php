<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Habitat extends Model
{
    use HasFactory;

    protected $fillable = [
        'nama_habitat',
        'lokasi',
        'tipe_ekosistem',
    ];

    /**
     * Relasi ke model Satwa (One-to-Many).
     */
    public function animals(): HasMany
    {
        return $this->hasMany(Animal::class, 'habitat_id');
    }
}

