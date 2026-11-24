<?php

namespace Tests\Feature;

use App\Models\Animal;
use App\Models\User;
use Tests\TestCase;

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

        $response = $this->getJson('/api/animals/'.$animal->id);
        $response->assertStatus(200);
        $response->assertJsonFragment([
            'nama_lokal' => $animal->nama_lokal,
        ]);
    }

    /**
     * Test tamu tak terautentikasi (guest) dicegah mengakses halaman kelola dan diarahkan ke login.
     */
    public function test_guest_cannot_access_manage_page(): void
    {
        $response = $this->get('/manage');
        $response->assertRedirect('/login');
    }

    /**
     * Test tamu tak terautentikasi dicegah mengakses formulir tambah satwa.
     */
    public function test_guest_cannot_access_create_animal_page(): void
    {
        $response = $this->get('/animals/create');
        $response->assertRedirect('/login');
    }

    /**
     * Test tamu tak terautentikasi dicegah memanipulasi (tambah/ubah/hapus) data satwa.
     */
    public function test_guest_cannot_manipulate_animals(): void
    {
        $postResponse = $this->post('/animals', [
            'nama_lokal' => 'Satwa Ilegal Tamu',
            'nama_ilmiah' => 'Animalia illegalis',
            'category_id' => 1,
            'status_id' => 1,
            'habitat_id' => 1,
        ]);
        $postResponse->assertRedirect('/login');
        $this->assertDatabaseMissing('animals', ['nama_lokal' => 'Satwa Ilegal Tamu']);
    }

    /**
     * Test admin terautentikasi dapat membuka panel kelola dan formulir tambah satwa.
     */
    public function test_authenticated_admin_can_access_manage_and_create(): void
    {
        $admin = User::first();
        $this->assertNotNull($admin);

        $manageResponse = $this->actingAs($admin)->get('/manage');
        $manageResponse->assertStatus(200);
        $manageResponse->assertSee('Manajemen Data Satwa Dilindungi');

        $createResponse = $this->actingAs($admin)->get('/animals/create');
        $createResponse->assertStatus(200);
        $createResponse->assertSee('Input Data Satwa Baru');
    }

    /**
     * Test halaman Login Admin dapat diakses.
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
     * Test operasi CRUD Satwa (Store, Update, Delete) oleh admin terautentikasi.
     */
    public function test_animal_crud_operations(): void
    {
        $admin = User::first();
        $this->assertNotNull($admin);

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

        $storeResponse = $this->actingAs($admin)->post('/animals', $postData);
        $storeResponse->assertRedirect('/manage');

        $animal = Animal::where('nama_lokal', 'Pesut Mahakam Test')->first();
        $this->assertNotNull($animal);
        $this->assertEquals('Orcaella brevirostris', $animal->nama_ilmiah);

        // 2. Update
        $updateData = array_merge($postData, [
            'nama_lokal' => 'Pesut Mahakam Updated',
            'estimasi_populasi' => 75,
        ]);

        $updateResponse = $this->actingAs($admin)->put('/animals/'.$animal->id, $updateData);
        $updateResponse->assertRedirect('/manage');

        $animal->refresh();
        $this->assertEquals('Pesut Mahakam Updated', $animal->nama_lokal);
        $this->assertEquals(75, $animal->estimasi_populasi);

        // 3. Delete
        $deleteResponse = $this->actingAs($admin)->delete('/animals/'.$animal->id);
        $deleteResponse->assertRedirect('/manage');

        $this->assertNull(Animal::find($animal->id));
    }
}
