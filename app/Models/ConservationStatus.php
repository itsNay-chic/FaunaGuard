<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class ConservationStatus extends Model
{
    use HasFactory;

    protected $fillable = [
        'kode',
        'nama_status',
        'warna_badge',
        'tingkat_ancaman',
    ];

    /**
     * Relasi ke model Satwa (One-to-Many).
     */
    public function animals(): HasMany
    {
        return $this->hasMany(Animal::class, 'status_id');
    }
}

