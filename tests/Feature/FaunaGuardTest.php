<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\Animal;
use App\Models\Category;
use App\Models\ConservationStatus;
use App\Models\Habitat;
use App\Models\User;

class FaunaGuardTest extends TestCase
{
    /**
     * Test halaman Beranda dapat diakses.
     */
    public function test_beranda_page_is_accessible(): void
    {
        $response = $this->get('/');
        $response->assertStatus(200);
        $response->assertSee('FaunaGuard');
        $response->assertSee('Jelajahi Katalog Satwa');
    }

    /**
     * Test halaman Katalog Satwa dan list satwa.
     */
    public function test_katalog_page_is_accessible_and_lists_animals(): void
    {
        $response = $this->get('/katalog');
        $response->assertStatus(200);
        $response->assertSee('Orangutan Kalimantan');
        $response->assertSee('Bekantan');
    }

    /**
     * Test API Detail Satwa untuk modal pop-up.
     */
    public function test_animal_detail_api_returns_json(): void
    {
        $animal = Animal::first();
        $this->assertNotNull($animal);

        $response = $this->getJson('/api/animals/' . $animal->id);
        $response->assertStatus(200);
        $response->assertJsonFragment([
            'nama_lokal' => $animal->nama_lokal,
        ]);
    }

    /**
     * Test halaman Kelola Database (CRUD).
     */
    public function test_manage_page_is_accessible(): void
    {
        $response = $this->get('/manage');
        $response->assertStatus(200);
        $response->assertSee('Manajemen Data Satwa Dilindungi');
    }

    /**
     * Test halaman Form Tambah Satwa.
     */
    public function test_create_animal_page_is_accessible(): void
    {
        $response = $this->get('/animals/create');
        $response->assertStatus(200);
        $response->assertSee('Input Data Satwa Baru');
    }

    /**
     * Test halaman Login Admin.
     */
    public function test_login_page_is_accessible(): void
    {
        $response = $this->get('/login');
        $response->assertStatus(200);
        $response->assertSee('Masuk Pengelola FaunaGuard');
    }

    /**
     * Test proses login dan logout admin.
     */
    public function test_admin_authentication_flow(): void
    {
        $response = $this->post('/login', [
            'email' => 'admin@faunaguard.org',
            'password' => 'admin123',
        ]);

        $response->assertRedirect('/manage');
        $this->assertAuthenticated();

        $logoutResponse = $this->post('/logout');
        $logoutResponse->assertRedirect('/');
        $this->assertGuest();
    }

    /**
     * Test operasi CRUD Satwa (Store, Update, Delete) via Eloquent.
     */
    public function test_animal_crud_operations(): void
    {
        // 1. Store
        $postData = [
            'nama_lokal' => 'Pesut Mahakam Test',
            'nama_ilmiah' => 'Orcaella brevirostris',
            'category_id' => 1,
            'status_id' => 1,
            'habitat_id' => 2,
            'estimasi_populasi' => 80,
            'deskripsi' => 'Lumba-lumba air tawar Sungai Mahakam.',
            'ancaman_utama' => 'Lalu lintas kapal ponton batubara.',
            'foto_url' => 'https://example.com/pesut.jpg',
        ];

        $storeResponse = $this->post('/animals', $postData);
        $storeResponse->assertRedirect('/manage');

        $animal = Animal::where('nama_lokal', 'Pesut Mahakam Test')->first();
        $this->assertNotNull($animal);
        $this->assertEquals('Orcaella brevirostris', $animal->nama_ilmiah);

        // 2. Update
        $updateData = array_merge($postData, [
            'nama_lokal' => 'Pesut Mahakam Updated',
            'estimasi_populasi' => 75,
        ]);

        $updateResponse = $this->put('/animals/' . $animal->id, $updateData);
        $updateResponse->assertRedirect('/manage');

        $animal->refresh();
        $this->assertEquals('Pesut Mahakam Updated', $animal->nama_lokal);
        $this->assertEquals(75, $animal->estimasi_populasi);

        // 3. Delete
        $deleteResponse = $this->delete('/animals/' . $animal->id);
        $deleteResponse->assertRedirect('/manage');

        $this->assertNull(Animal::find($animal->id));
    }
}
