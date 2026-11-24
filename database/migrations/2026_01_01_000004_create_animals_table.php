<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('animals', function (Blueprint $table) {
            $table->id();
            $table->string('nama_lokal', 100)->index();
            $table->string('nama_ilmiah', 100);
            $table->text('deskripsi')->nullable();
            $table->text('ancaman_utama')->nullable();
            $table->integer('estimasi_populasi')->nullable();
            $table->foreignId('category_id')->constrained('categories')->cascadeOnUpdate()->restrictOnDelete();
            $table->foreignId('status_id')->constrained('conservation_statuses')->cascadeOnUpdate()->restrictOnDelete();
            $table->foreignId('habitat_id')->constrained('habitats')->cascadeOnUpdate()->restrictOnDelete();
            $table->mediumText('foto_url')->nullable();
            $table->timestamps();

            $table->index('category_id');
            $table->index('status_id');
            $table->index('habitat_id');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('animals');
    }
};

