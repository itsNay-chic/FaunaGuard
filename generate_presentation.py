"""
FaunaGuard - Generator Presentasi PPTX & Diagram Database
Menghasilkan file PowerPoint profesional bertema alam dan satwa Kalimantan
beserta diagram ERD dan tangkapan layar visual tabel database MySQL.
"""

import os
import sys
import tempfile

os.environ["MPLCONFIGDIR"] = tempfile.gettempdir()

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Pastikan folder output siap
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "pembagian_tugas")
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets_ppt")
os.makedirs(ASSETS_DIR, exist_ok=True)


# =============================================================================
# 1. GENERATOR GAMBAR DIAGRAM ERD (MySQL Workbench Style)
# =============================================================================
def generate_erd_diagram():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=200)
    ax.set_facecolor("#F4F6F4")
    fig.patch.set_facecolor("#F4F6F4")

    # Palet Warna Workbench
    header_color = "#186049"       # Deep Rainforest Green
    sub_header = "#244E3F"
    border_color = "#0E3B2D"
    bg_table = "#FFFFFF"
    fk_color = "#D98327"           # Orangutan Amber
    pk_color = "#E6A119"

    def draw_table(ax, x, y, width, height, title, columns):
        # Card Body
        rect = patches.FancyBboxPatch(
            (x, y - height), width, height,
            boxstyle="round,pad=0.02,rounding_size=0.15",
            facecolor=bg_table, edgecolor=border_color, linewidth=2, zorder=2
        )
        ax.add_patch(rect)

        # Header Box
        header_height = 0.65
        h_rect = patches.FancyBboxPatch(
            (x, y - header_height), width, header_height,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            facecolor=header_color, edgecolor=border_color, linewidth=1.5, zorder=3
        )
        ax.add_patch(h_rect)

        # Title
        ax.text(
            x + width / 2, y - header_height / 2, title,
            color="#FFFFFF", fontsize=11, fontweight="bold",
            ha="center", va="center", zorder=4, family="sans-serif"
        )

        # Columns
        col_y = y - header_height - 0.25
        line_spacing = 0.32
        for col in columns:
            is_pk = "PK" in col[0]
            is_fk = "FK" in col[0]

            prefix = col[0]
            name = col[1]
            dtype = col[2]

            prefix_color = "#C87800" if is_pk else ("#1976D2" if is_fk else "#757575")

            ax.text(x + 0.2, col_y, prefix, color=prefix_color, fontsize=8.5, fontweight="bold", zorder=4, family="sans-serif")
            ax.text(x + 0.8, col_y, name, color="#212529", fontsize=9, fontweight="bold" if (is_pk or is_fk) else "normal", zorder=4, family="sans-serif")
            ax.text(x + width - 0.2, col_y, dtype, color="#6c757d", fontsize=8, ha="right", style="italic", zorder=4, family="sans-serif")

            # Garis pemisah halus antar kolom
            ax.plot([x + 0.1, x + width - 0.1], [col_y - 0.12, col_y - 0.12], color="#E9ECEF", lw=0.75, zorder=3)
            col_y -= line_spacing

    # Tabel 1: categories (Kiri Atas)
    cat_cols = [
        ("PK", "id", "INT AUTO_INCREMENT"),
        ("", "nama_kategori", "VARCHAR(50) NOT NULL"),
        ("", "deskripsi", "TEXT NULL")
    ]
    draw_table(ax, x=0.5, y=7.2, width=3.8, height=2.0, title="categories", columns=cat_cols)

    # Tabel 2: conservation_statuses (Kanan Atas)
    status_cols = [
        ("PK", "id", "INT AUTO_INCREMENT"),
        ("", "kode", "VARCHAR(10) NOT NULL"),
        ("", "nama_status", "VARCHAR(50) NOT NULL"),
        ("", "warna_badge", "VARCHAR(20) DEFAULT"),
        ("", "tingkat_ancaman", "VARCHAR(50) NOT NULL")
    ]
    draw_table(ax, x=9.7, y=7.2, width=3.8, height=2.6, title="conservation_statuses", columns=status_cols)

    # Tabel 3: habitats (Kiri Bawah)
    hab_cols = [
        ("PK", "id", "INT AUTO_INCREMENT"),
        ("", "nama_habitat", "VARCHAR(100) NOT NULL"),
        ("", "lokasi", "VARCHAR(100) NOT NULL"),
        ("", "tipe_ekosistem", "VARCHAR(50) NOT NULL")
    ]
    draw_table(ax, x=0.5, y=3.8, width=3.8, height=2.3, title="habitats", columns=hab_cols)

    # Tabel 4: animals (Tengah Utama)
    animal_cols = [
        ("PK", "id", "INT AUTO_INCREMENT"),
        ("", "nama_lokal", "VARCHAR(100) NOT NULL"),
        ("", "nama_ilmiah", "VARCHAR(100) NOT NULL"),
        ("", "deskripsi", "TEXT NULL"),
        ("", "ancaman_utama", "TEXT NULL"),
        ("", "estimasi_populasi", "INT NULL"),
        ("", "foto_url", "VARCHAR(255) NULL"),
        ("FK", "category_id", "INT -> categories.id"),
        ("FK", "status_id", "INT -> statuses.id"),
        ("FK", "habitat_id", "INT -> habitats.id"),
        ("", "created_at", "TIMESTAMP DEFAULT")
    ]
    draw_table(ax, x=4.9, y=6.8, width=4.2, height=4.5, title="animals (Tabel Inti Transaksional)", columns=animal_cols)

    # Garis Relasi Foreign Keys (Crow's Foot style with Arrow & Badges)
    # 1. categories -> animals
    ax.annotate(
        "", xy=(4.9, 5.0), xytext=(4.3, 6.2),
        arrowprops=dict(arrowstyle="-|>", color="#186049", lw=2.5, mutation_scale=15),
        zorder=5
    )
    ax.text(4.45, 5.75, "1 : N (FK: category_id)", color="#186049", fontsize=8.5, fontweight="bold", backgroundcolor="#FFFFFF", bbox=dict(boxstyle="round,pad=0.2", fc="#E8F5E9", ec="#186049", lw=1))

    # 2. conservation_statuses -> animals
    ax.annotate(
        "", xy=(9.1, 4.6), xytext=(9.7, 5.9),
        arrowprops=dict(arrowstyle="-|>", color="#D98327", lw=2.5, mutation_scale=15),
        zorder=5
    )
    ax.text(9.1, 5.4, "1 : N (FK: status_id)", color="#D98327", fontsize=8.5, fontweight="bold", backgroundcolor="#FFFFFF", bbox=dict(boxstyle="round,pad=0.2", fc="#FFF3E0", ec="#D98327", lw=1))

    # 3. habitats -> animals
    ax.annotate(
        "", xy=(4.9, 3.8), xytext=(4.3, 2.7),
        arrowprops=dict(arrowstyle="-|>", color="#4A943E", lw=2.5, mutation_scale=15),
        zorder=5
    )
    ax.text(4.35, 3.1, "1 : N (FK: habitat_id)", color="#4A943E", fontsize=8.5, fontweight="bold", backgroundcolor="#FFFFFF", bbox=dict(boxstyle="round,pad=0.2", fc="#F1F8E9", ec="#4A943E", lw=1))

    # Judul & Watermark
    ax.text(7.0, 7.6, "MySQL Relational Schema (3NF) — FaunaGuard Kalimantan", color="#186049", fontsize=15, fontweight="bold", ha="center", va="center")
    ax.text(7.0, 0.4, "Integritas Referensial: ON UPDATE CASCADE  |  ON DELETE RESTRICT  |  Engine: InnoDB (utf8mb4)", color="#6c757d", fontsize=9, ha="center")

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")
    plt.tight_layout()

    out_path = os.path.join(ASSETS_DIR, "erd_diagram.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print("ERD Diagram generated:", out_path)
    return out_path


# =============================================================================
# 2. GENERATOR MOCKUP DATA GRID (MySQL Workbench Result Grid Style)
# =============================================================================
def generate_db_data_grid():
    fig, ax = plt.subplots(figsize=(15, 7.5), dpi=200)
    ax.set_facecolor("#FFFFFF")
    fig.patch.set_facecolor("#FFFFFF")

    # Header Workbench UI
    ui_header = patches.Rectangle((0, 7.0), 15, 0.8, facecolor="#E1E5EA", edgecolor="#B0B8C1", lw=1)
    ax.add_patch(ui_header)
    ax.text(0.4, 7.4, "MySQL Workbench 8.0 CE — Query Result Grid : [ faunaguard_db.animals ]", color="#333333", fontsize=11, fontweight="bold")
    ax.text(14.6, 7.4, "LIMIT 0, 1000  |  Fetched 6 row(s) in 0.0012 sec", color="#666666", fontsize=9, ha="right")

    # Table Header Bar
    table_bar = patches.Rectangle((0, 6.4), 15, 0.6, facecolor="#186049", edgecolor="#0E3B2D", lw=1)
    ax.add_patch(table_bar)

    headers = [
        ("id", 0.6),
        ("nama_lokal", 2.6),
        ("nama_ilmiah", 3.0),
        ("category", 1.8),
        ("status_iucn", 2.2),
        ("habitat_lokasi", 2.8),
        ("estimasi_populasi", 2.0)
    ]

    cur_x = 0.2
    for h_name, width in headers:
        ax.text(cur_x + 0.1, 6.7, h_name, color="#FFFFFF", fontsize=9.5, fontweight="bold", va="center")
        ax.plot([cur_x + width, cur_x + width], [6.4, 7.0], color="#2C7A60", lw=1)
        cur_x += width

    # Sample Data Rows
    rows = [
        ("1", "Orangutan Kalimantan", "Pongo pygmaeus", "Mamalia", "CR - Kritis", "TN Tanjung Puting", "57.000"),
        ("2", "Bekantan", "Nasalis larvatus", "Mamalia", "EN - Terancam", "DAS Mahakam", "16.000"),
        ("3", "Badak Kalimantan", "Dicerorhinus sumatrensis", "Mamalia", "CR - Kritis", "TN Kutai", "15"),
        ("4", "Enggang Gading", "Rhinoplax vigil", "Aves (Burung)", "CR - Kritis", "TN Betung Kerihun", "4.000"),
        ("5", "Trenggiling Sunda", "Manis javanica", "Mamalia", "CR - Kritis", "TN Bukit Baka Raya", "12.000"),
        ("6", "Pesut Mahakam", "Orcaella brevirostris", "Mamalia", "CR - Kritis", "Sungai Mahakam", "80"),
        ("7", "Macan Dahan Kalimantan", "Neofelis diardi borneensis", "Mamalia", "VU - Rentan", "TN Sebangau", "5.000"),
        ("8", "Gajah Kerdil Borneo", "Elephas maximus borneensis", "Mamalia", "EN - Terancam", "Hutan Heart of Borneo", "1.500")
    ]

    row_y = 5.9
    for i, row in enumerate(rows):
        bg_c = "#F8FAF8" if i % 2 == 1 else "#FFFFFF"
        row_rect = patches.Rectangle((0, row_y - 0.2), 15, 0.6, facecolor=bg_c, edgecolor="#E5E8EC", lw=0.5)
        ax.add_patch(row_rect)

        cur_x = 0.2
        for col_idx, (h_name, width) in enumerate(headers):
            val = row[col_idx]
            
            # Badge status
            if col_idx == 4:
                badge_bg = "#D98327" if "CR" in val else ("#E67E22" if "EN" in val else "#F1C40F")
                badge_fg = "#FFFFFF" if ("CR" in val or "EN" in val) else "#212529"
                b_rect = patches.FancyBboxPatch(
                    (cur_x + 0.05, row_y - 0.1), width - 0.3, 0.42,
                    boxstyle="round,pad=0.03,rounding_size=0.1",
                    facecolor=badge_bg, edgecolor="none"
                )
                ax.add_patch(b_rect)
                ax.text(cur_x + (width - 0.3) / 2 + 0.05, row_y + 0.1, val, color=badge_fg, fontsize=8.5, fontweight="bold", ha="center", va="center")
            else:
                is_num = col_idx in (0, 6)
                is_italic = (col_idx == 2)
                f_color = "#186049" if col_idx == 1 else ("#495057" if is_italic else "#212529")
                ax.text(
                    cur_x + 0.1, row_y + 0.1, val,
                    color=f_color, fontsize=9,
                    style="italic" if is_italic else "normal",
                    fontweight="bold" if col_idx in (0, 1) else "normal",
                    va="center"
                )

            cur_x += width

        row_y -= 0.6

    # Footer Status Bar
    footer_bar = patches.Rectangle((0, 0.5), 15, 0.6, facecolor="#F1F3F5", edgecolor="#CED4DA", lw=1)
    ax.add_patch(footer_bar)
    ax.text(0.4, 0.8, "Database Server: 127.0.0.1:3306  |  Schema: faunaguard_db  |  Charset: utf8mb4_unicode_ci  |  AutoCommit: ON", color="#495057", fontsize=8.5)

    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8)
    ax.axis("off")
    plt.tight_layout()

    out_path = os.path.join(ASSETS_DIR, "db_data_grid.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print("Database Data Grid generated:", out_path)
    return out_path


# =============================================================================
# 3. GENERATOR MOCKUP SQL DDL CODE BOX
# =============================================================================
def generate_sql_ddl_box():
    fig, ax = plt.subplots(figsize=(14, 7), dpi=200)
    ax.set_facecolor("#1E222A")
    fig.patch.set_facecolor("#1E222A")

    # Title Bar IDE
    title_bar = patches.Rectangle((0, 6.2), 14, 0.8, facecolor="#282C34", edgecolor="#181A1F", lw=1)
    ax.add_patch(title_bar)
    ax.text(0.4, 6.6, "faunaguard_schema.sql — DDL Constraints & B-Tree Indexes", color="#ABB2BF", fontsize=11, fontweight="bold")

    # Buttons window
    for idx, c in enumerate(["#E06C75", "#E5C07B", "#98C379"]):
        circ = patches.Circle((13.4 - idx * 0.35, 6.6), 0.1, facecolor=c, edgecolor="none")
        ax.add_patch(circ)

    sql_lines = [
        ("-- 1. DDL Tabel Utama 'animals' dengan 3 Foreign Key Relasional", "#5C6370", True),
        ("CREATE TABLE animals (", "#E5C07B", False),
        ("    id INT AUTO_INCREMENT PRIMARY KEY,", "#E06C75", False),
        ("    nama_lokal VARCHAR(100) NOT NULL,", "#ABB2BF", False),
        ("    nama_ilmiah VARCHAR(100) NOT NULL,", "#ABB2BF", False),
        ("    category_id INT NOT NULL,", "#61AFEF", False),
        ("    status_id INT NOT NULL,", "#61AFEF", False),
        ("    habitat_id INT NOT NULL,", "#61AFEF", False),
        ("    CONSTRAINT fk_animal_category FOREIGN KEY (category_id) REFERENCES categories (id)", "#98C379", False),
        ("        ON UPDATE CASCADE ON DELETE RESTRICT,", "#D19A66", True),
        ("    CONSTRAINT fk_animal_status FOREIGN KEY (status_id) REFERENCES conservation_statuses (id)", "#98C379", False),
        ("        ON UPDATE CASCADE ON DELETE RESTRICT,", "#D19A66", True),
        ("    CONSTRAINT fk_animal_habitat FOREIGN KEY (habitat_id) REFERENCES habitats (id)", "#98C379", False),
        ("        ON UPDATE CASCADE ON DELETE RESTRICT", "#D19A66", True),
        (") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;", "#E5C07B", False),
        ("", "#ABB2BF", False),
        ("-- 2. B-Tree Indexes untuk Akses Cepat JOIN & Pencarian WHERE (O(log N))", "#5C6370", True),
        ("CREATE INDEX idx_animals_nama ON animals (nama_lokal);", "#61AFEF", False),
        ("CREATE INDEX idx_animals_category ON animals (category_id);", "#61AFEF", False),
        ("CREATE INDEX idx_animals_status ON animals (status_id);", "#61AFEF", False)
    ]

    y_pos = 5.8
    for line_text, color, is_italic in sql_lines:
        ax.text(0.4, y_pos, line_text, color=color, fontsize=9.2, style="italic" if is_italic else "normal", family="monospace")
        y_pos -= 0.28

    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis("off")
    plt.tight_layout()

    out_path = os.path.join(ASSETS_DIR, "db_schema_ddl.png")
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print("SQL DDL Box generated:", out_path)
    return out_path


# =============================================================================
# 4. PEMBUATAN FILE PPTX MENGGUNAKAN PYTHON-PPTX (16:9 Widescreen)
# =============================================================================
def build_powerpoint():
    prs = Presentation()
    # Ubah ukuran slide menjadi 16:9 Widescreen (13.333 x 7.5 inches)
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Definisi Warna Tema Borneo Rainforest
    C_PRIMARY = RGBColor(24, 96, 73)      # Deep Rainforest Green (#186049)
    C_SECONDARY = RGBColor(74, 148, 62)   # Lush Forest Green (#4A943E)
    C_AMBER = RGBColor(217, 131, 39)      # Orangutan Amber (#D98327)
    C_SAND = RGBColor(236, 232, 175)      # Pale Sand (#ECE8AF)
    C_DARK = RGBColor(15, 56, 43)         # Dark Rainforest (#0F382B)
    C_LIGHT_BG = RGBColor(250, 249, 243)  # Soft Cream (#FAF9F3)
    C_WHITE = RGBColor(255, 255, 255)
    C_TEXT = RGBColor(33, 37, 41)
    C_MUTED = RGBColor(108, 117, 125)
    C_CARD_BG = RGBColor(255, 255, 255)
    C_CARD_BORDER = RGBColor(222, 216, 157)

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title_text, category_tag="FAUNAGUARD BORNEO", is_dark=False):
        # Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = category_tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_AMBER if is_dark else C_SECONDARY

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE if is_dark else C_PRIMARY

        # Decorative Bar
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8), Inches(1.5), Inches(3.0), Inches(0.06)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = C_AMBER
        line.line.color.rgb = C_AMBER

    # -------------------------------------------------------------------------
    # SLIDE 1: COVER SLIDE
    # -------------------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, C_DARK)

    # Accent Strip Top
    strip = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.2))
    strip.fill.solid()
    strip.fill.fore_color.rgb = C_AMBER
    strip.line.fill.background()

    # Badge Pill
    badge = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.3), Inches(4.5), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_PRIMARY
    badge.line.color.rgb = C_AMBER
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "🌿 SUAKA BIODIVERSITAS PULAU BORNEO"
    p_b.font.size = Pt(10.5)
    p_b.font.bold = True
    p_b.font.color.rgb = C_SAND
    p_b.alignment = PP_ALIGN.CENTER

    # Main Title
    t_box = slide1.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(11.3), Inches(2.0))
    tf = t_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "FaunaGuard"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    p2 = tf.add_paragraph()
    p2.text = "Suaka Informasi & Edukasi Konservasi Satwa Dilindungi Kalimantan"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = C_SAND
    p2.space_before = Pt(10)

    # Subtitle / Description
    desc_box = slide1.shapes.add_textbox(Inches(1.0), Inches(4.2), Inches(10.5), Inches(1.4))
    tf_d = desc_box.text_frame
    tf_d.word_wrap = True
    p_d = tf_d.paragraphs[0]
    p_d.text = (
        "Presentasi Komprehensif Arsitektur Web Flask, Fitur Publik & Manajemen, "
        "serta Rancangan Database Relasional MySQL Berintegritas Tinggi (3NF & Foreign Key)."
    )
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = RGBColor(220, 230, 225)

    # 3 Stat Mini-Pills
    stats = [
        ("🦧 4 TABEL RELASIONAL", "Normalisasi 3NF MySQL"),
        ("🛡️ STATUS IUCN RED LIST", "Pantau Satwa Kritis (CR)"),
        ("⚡ FLASK & PYMYSQL", "CRUD & Filter Cepat")
    ]
    for idx, (head, sub) in enumerate(stats):
        bx = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0 + idx * 3.8), Inches(5.8), Inches(3.5), Inches(1.0))
        bx.fill.solid()
        bx.fill.fore_color.rgb = RGBColor(20, 75, 58)
        bx.line.color.rgb = C_SECONDARY
        bx_tf = bx.text_frame
        bx_p1 = bx_tf.paragraphs[0]
        bx_p1.text = head
        bx_p1.font.size = Pt(11)
        bx_p1.font.bold = True
        bx_p1.font.color.rgb = C_SAND
        bx_p2 = bx_tf.add_paragraph()
        bx_p2.text = sub
        bx_p2.font.size = Pt(9.5)
        bx_p2.font.color.rgb = RGBColor(200, 215, 205)

    # -------------------------------------------------------------------------
    # SLIDE 2: LATAR BELAKANG & URGENSI HAYATI BORNEO
    # -------------------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, C_LIGHT_BG)
    add_header(slide2, "Latar Belakang & Urgensi Hayati Borneo", "1. PENJELASAN ISI WEB")

    # 3 Card Masalah & Solusi
    cards2 = [
        ("🌳 Hutan Tertua di Dunia", "Keanekaragaman Endemik", 
         "Hutan hujan Kalimantan telah berusia lebih dari 130 juta tahun—lebih tua dari Amazon. Menjadi rumah bagi spesies unik yang tidak dapat ditemukan di belahan bumi mana pun seperti Orangutan, Bekantan, dan Badak Kalimantan.", C_PRIMARY),
        ("⚠️ Ancaman Nyata Kepunahan", "Deforestasi & Perburuan Liar", 
         "Alih fungsi lahan gambut, kebakaran hutan musiman, fragmentasi habitat, dan perdagangan satwa liar ilegal telah mendorong populasi spesies kunci ke ambang kepunahan (status Critically Endangered / Kritis).", C_AMBER),
        ("💡 Solusi Digital FaunaGuard", "Edukasi & Data Terpadu", 
         "Dibutuhkan media informasi publik yang transparan dan terstruktur. FaunaGuard hadir memadukan edukasi keanekaragaman hayati dengan teknologi database relasional untuk inventarisasi dan advokasi pelestarian.", C_SECONDARY)
    ]

    for idx, (title, subtitle, body, border_c) in enumerate(cards2):
        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 3.95), Inches(1.8), Inches(3.8), Inches(4.9))
        card.fill.solid()
        card.fill.fore_color.rgb = C_CARD_BG
        card.line.color.rgb = border_c
        card.line.width = Pt(2)

        ctf = card.text_frame
        ctf.word_wrap = True
        cp1 = ctf.paragraphs[0]
        cp1.text = title
        cp1.font.size = Pt(14)
        cp1.font.bold = True
        cp1.font.color.rgb = border_c

        cp2 = ctf.add_paragraph()
        cp2.text = subtitle
        cp2.font.size = Pt(10)
        cp2.font.bold = True
        cp2.font.color.rgb = C_MUTED
        cp2.space_before = Pt(4)

        cp3 = ctf.add_paragraph()
        cp3.text = body
        cp3.font.size = Pt(10.5)
        cp3.font.color.rgb = C_TEXT
        cp3.space_before = Pt(14)

    # -------------------------------------------------------------------------
    # SLIDE 3: PENJELASAN ISI WEB (PLATFORM OVERVIEW)
    # -------------------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, C_LIGHT_BG)
    add_header(slide3, "Struktur & Konten Utama Web FaunaGuard", "1. PENJELASAN ISI WEB")

    # Banner Pengantar
    banner = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.1))
    banner.fill.solid()
    banner.fill.fore_color.rgb = C_PRIMARY
    banner.line.fill.background()
    btf = banner.text_frame
    btf.word_wrap = True
    bp1 = btf.paragraphs[0]
    bp1.text = "Apa itu FaunaGuard?"
    bp1.font.size = Pt(13)
    bp1.font.bold = True
    bp1.font.color.rgb = C_AMBER
    bp2 = btf.add_paragraph()
    bp2.text = "FaunaGuard adalah platform portal web edukasi konservasi yang mendokumentasikan satwa dilindungi di Kalimantan. Menghubungkan masyarakat dengan data ilmiah taksonomi, peran ekologi, status IUCN Red List, dan kawasan suaka alam."
    bp2.font.size = Pt(10.5)
    bp2.font.color.rgb = C_WHITE

    # 3 Kolom Komponen Web
    pages = [
        ("🏠 Halaman Beranda (Home)", "Suaka Edukasi Publik", [
            "Hero edukasi dengan identitas konservasi Borneo.",
            "Penjelasan singkat mengenai urgensi dan misi web.",
            "Indikator statistik hayati real-time (Total Spesies, Satwa Kritis, Kawasan Konservasi).",
            "Sorotan satwa berstatus Kritis (CR) yang butuh perlindungan segera.",
            "Banner ajakan aksi pelestarian lingkungan."
        ]),
        ("📚 Halaman Katalog Satwa", "Eksplorasi & Filter Komprehensif", [
            "Direktori lengkap seluruh data satwa Kalimantan.",
            "Kartu satwa visual dengan foto autentik & badge status IUCN berpalet warna resmi.",
            "Sistem pencarian instan nama lokal & ilmiah.",
            "Filter dinamis berdasarkan Kategori Taksonomi & Status Konservasi.",
            "Tombol modal pop-up untuk inspeksi profil mendalam."
        ]),
        ("⚙️ Panel Manajemen (CRUD)", "Pusat Kontrol Data Relasional", [
            "Tampilan tabular sinkron langsung ke database MySQL.",
            "Form penambahan satwa baru dengan validasi relasi.",
            "Fitur unggah file gambar lokal & ekstraksi link artikel.",
            "Input manual kawasan habitat baru + datalist otomatis.",
            "Fitur pembaruan (Edit) dan penghapusan aman (Delete)."
        ])
    ]

    for idx, (p_title, p_sub, bullets) in enumerate(pages):
        p_card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + idx * 3.95), Inches(3.1), Inches(3.8), Inches(3.9))
        p_card.fill.solid()
        p_card.fill.fore_color.rgb = C_CARD_BG
        p_card.line.color.rgb = C_CARD_BORDER
        p_card.line.width = Pt(1.5)

        pctf = p_card.text_frame
        pctf.word_wrap = True
        pp1 = pctf.paragraphs[0]
        pp1.text = p_title
        pp1.font.size = Pt(12.5)
        pp1.font.bold = True
        pp1.font.color.rgb = C_PRIMARY

        pp2 = pctf.add_paragraph()
        pp2.text = p_sub
        pp2.font.size = Pt(9.5)
        pp2.font.bold = True
        pp2.font.color.rgb = C_AMBER
        pp2.space_before = Pt(3)

        for b in bullets:
            pb = pctf.add_paragraph()
            pb.text = "• " + b
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = C_TEXT
            pb.space_before = Pt(6)

    # -------------------------------------------------------------------------
    # SLIDE 4: FITUR-FITUR DI WEBNYA (BAGIAN 1: MODUL PUBLIK)
    # -------------------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, C_LIGHT_BG)
    add_header(slide4, "Fitur-Fitur di Web: Modul Publik & Edukasi", "2. FITUR DI WEBNYA")

    features_pub = [
        ("1. Kartu Satwa Interaktif (Animal Cards)",
         "Desain visual kartu satwa dengan rasio 16:9, dilengkapi lencana status IUCN dengan warna khusus (CR: Oranye Kemerahan, EN: Amber, VU: Emas), estimasi sisa populasi, dan nama ilmiah berhuruf miring.",
         "templates/index.html & static/css/style.css"),
        ("2. Pencarian Instan & Filter Multi-Kriteria",
         "Pengguna dapat mencari berdasarkan nama satwa dan menyaring secara simultan berdasarkan kategori taksonomi (Mamalia, Aves, dll.) dan status keterancaman IUCN tanpa menghilangkan parameter URL.",
         "app.py (Query SQL dinamis WHERE 1=1)"),
        ("3. Pop-up Modal Edukatif Asinkron (Fetch API)",
         "Membuka detail profil satwa secara instan tanpa reload halaman menggunakan Vanilla JavaScript Fetch API ke endpoint /api/animals/<id>, menyajikan taksonomi, peran ekologis, habitat, dan ancaman kepunahan.",
         "static/js/main.js & /api/animals/<id>"),
        ("4. Sistem Pencegahan Gambar Rusak (Fallback SVG)",
         "Mencegah pemblokiran hotlinking gambar dari Wikipedia/portal berita menggunakan atribut meta referrerpolicy='no-referrer' dan otomatis beralih ke gambar cadangan placeholder.svg jika URL bermasalah.",
         "static/img/placeholder.svg & onerror handler")
    ]

    for idx, (f_title, f_desc, f_tech) in enumerate(features_pub):
        fx = Inches(0.8 + (idx % 2) * 5.95)
        fy = Inches(1.8 + (idx // 2) * 2.6)

        f_card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fx, fy, Inches(5.75), Inches(2.35))
        f_card.fill.solid()
        f_card.fill.fore_color.rgb = C_CARD_BG
        f_card.line.color.rgb = C_SECONDARY
        f_card.line.width = Pt(1.5)

        ftf = f_card.text_frame
        ftf.word_wrap = True
        fp1 = ftf.paragraphs[0]
        fp1.text = f_title
        fp1.font.size = Pt(12)
        fp1.font.bold = True
        fp1.font.color.rgb = C_PRIMARY

        fp2 = ftf.add_paragraph()
        fp2.text = f_desc
        fp2.font.size = Pt(9.5)
        fp2.font.color.rgb = C_TEXT
        fp2.space_before = Pt(6)

        fp3 = ftf.add_paragraph()
        fp3.text = "Implementasi: " + f_tech
        fp3.font.size = Pt(8.5)
        fp3.font.bold = True
        fp3.font.color.rgb = C_AMBER
        fp3.space_before = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 5: FITUR-FITUR DI WEBNYA (BAGIAN 2: CRUD & LOGIKA CERDAS)
    # -------------------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, C_LIGHT_BG)
    add_header(slide5, "Fitur-Fitur di Web: Modul CRUD & Logika Cerdas", "2. FITUR DI WEBNYA")

    features_crud = [
        ("5. Panel Manajemen Inventaris (CRUD View)",
         "Tabel tabular komprehensif menampilkan ID, foto mini, nama lokal, nama latin, status, kawasan habitat, dan estimasi populasi dengan tombol aksi langsung ke form edit dan hapus.",
         "templates/manage.html"),
        ("6. Upload File Gambar Lokal & Live Preview",
         "Mendukung unggah foto dari komputer pengguna (JPG, PNG, WebP) dengan validasi ekstensi aman werkzeug secure_filename() dan penamaan unik UUID, serta pratinjau instan sebelum disimpan.",
         "static/uploads/ & live preview JavaScript"),
        ("7. Ekstraksi Otomatis Gambar Web (Smart Scraper)",
         "Jika pengguna memasukkan link artikel berita/web (bukan link langsung .jpg), server otomatis membaca tag <meta property='og:image'> dan twitter:image untuk mengambil foto satwa terbaik secara otomatis.",
         "app.py (extract_direct_image_url)"),
        ("8. Graceful Degradation & Setup Notice",
         "Jika server MySQL lokal belum aktif atau belum di-import, web tidak menghasilkan 'Internal Server Error 500', melainkan menampilkan halaman panduan setup interaktif yang ramah pengguna.",
         "templates/setup_notice.html")
    ]

    for idx, (f_title, f_desc, f_tech) in enumerate(features_crud):
        fx = Inches(0.8 + (idx % 2) * 5.95)
        fy = Inches(1.8 + (idx // 2) * 2.6)

        f_card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, fx, fy, Inches(5.75), Inches(2.35))
        f_card.fill.solid()
        f_card.fill.fore_color.rgb = C_CARD_BG
        f_card.line.color.rgb = C_PRIMARY
        f_card.line.width = Pt(1.5)

        ftf = f_card.text_frame
        ftf.word_wrap = True
        fp1 = ftf.paragraphs[0]
        fp1.text = f_title
        fp1.font.size = Pt(12)
        fp1.font.bold = True
        fp1.font.color.rgb = C_PRIMARY

        fp2 = ftf.add_paragraph()
        fp2.text = f_desc
        fp2.font.size = Pt(9.5)
        fp2.font.color.rgb = C_TEXT
        fp2.space_before = Pt(6)

        fp3 = ftf.add_paragraph()
        fp3.text = "Implementasi: " + f_tech
        fp3.font.size = Pt(8.5)
        fp3.font.bold = True
        fp3.font.color.rgb = C_AMBER
        fp3.space_before = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 6: ARSITEKTUR DATABASE RELASIONAL (3NF CONCEPT)
    # -------------------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, C_LIGHT_BG)
    add_header(slide6, "Arsitektur Database Relasional & Normalisasi 3NF", "3. PENJELASAN DATABASE")

    # Mengapa Normalisasi 3NF?
    box_3nf = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(1.2))
    box_3nf.fill.solid()
    box_3nf.fill.fore_color.rgb = C_CARD_BG
    box_3nf.line.color.rgb = C_AMBER
    box_3nf.line.width = Pt(2)
    b3_tf = box_3nf.text_frame
    b3_tf.word_wrap = True
    b3_p1 = b3_tf.paragraphs[0]
    b3_p1.text = "Mengapa Database Dirancang Menjadi 4 Tabel Terpisah (Normalisasi 3NF)?"
    b3_p1.font.size = Pt(12.5)
    b3_p1.font.bold = True
    b3_p1.font.color.rgb = C_AMBER
    b3_p2 = b3_tf.add_paragraph()
    b3_p2.text = "Jika disimpan dalam 1 tabel raksasa (Flat Table), akan terjadi pemborosan penyimpanan dan 3 anomali data: Update Anomaly (harus update nama status ribuan kali), Insertion Anomaly (tidak bisa input habitat baru tanpa satwa), dan Deletion Anomaly (hapus satwa terakhir menghapus data habitat)."
    b3_p2.font.size = Pt(10)
    b3_p2.font.color.rgb = C_TEXT

    # 4 Tabel Penjelasan
    tables_info = [
        ("📁 categories", "Tabel Master Taksonomi", "Menyimpan kelas ilmiah satwa (Mamalia, Aves/Burung, Reptilia, Actinopterygii/Ikan). Memastikan klasifikasi taksonomi terstandar."),
        ("🛡️ conservation_statuses", "Tabel Master Standar IUCN", "Menyimpan 5 tingkat ancaman IUCN Red List (CR, EN, VU, NT, LC) lengkap dengan nama status, tingkat ancaman, dan warna badge web."),
        ("🏞️ habitats", "Tabel Master Kawasan Konservasi", "Mencatat taman nasional dan kawasan suaka alam Kalimantan (lokasi kabupaten/provinsi dan tipe ekosistem hutan gambut/hujan/karst)."),
        ("🐾 animals", "Tabel Inti Transaksional", "Tabel transaksi utama yang menyimpan profil satwa, populasi, foto, dan menghubungkan 3 tabel master melalui Foreign Key.")
    ]

    for idx, (t_name, t_sub, t_desc) in enumerate(tables_info):
        tx = Inches(0.8 + idx * 2.95)
        t_card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx, Inches(3.2), Inches(2.8), Inches(3.8))
        t_card.fill.solid()
        t_card.fill.fore_color.rgb = C_CARD_BG
        t_card.line.color.rgb = C_PRIMARY
        t_card.line.width = Pt(1.5)

        ttf = t_card.text_frame
        ttf.word_wrap = True
        tp1 = ttf.paragraphs[0]
        tp1.text = t_name
        tp1.font.size = Pt(12)
        tp1.font.bold = True
        tp1.font.color.rgb = C_PRIMARY

        tp2 = ttf.add_paragraph()
        tp2.text = t_sub
        tp2.font.size = Pt(9.5)
        tp2.font.bold = True
        tp2.font.color.rgb = C_SECONDARY
        tp2.space_before = Pt(4)

        tp3 = ttf.add_paragraph()
        tp3.text = t_desc
        tp3.font.size = Pt(9.5)
        tp3.font.color.rgb = C_TEXT
        tp3.space_before = Pt(10)

    # -------------------------------------------------------------------------
    # SLIDE 7: SCREENSHOT & PENJELASAN DIAGRAM ERD
    # -------------------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, C_LIGHT_BG)
    add_header(slide7, "Visualisasi Diagram ERD Relasional MySQL (EER Model)", "3. SCREENSHOT & PENJELASAN DATABASE")

    erd_img_path = os.path.join(ASSETS_DIR, "erd_diagram.png")
    if os.path.exists(erd_img_path):
        # Sisipkan gambar ERD di sebelah kiri
        slide7.shapes.add_picture(erd_img_path, Inches(0.8), Inches(1.8), width=Inches(7.8))

    # Keterangan di sebelah kanan
    erd_text_box = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.733), Inches(5.1))
    erd_text_box.fill.solid()
    erd_text_box.fill.fore_color.rgb = C_CARD_BG
    erd_text_box.line.color.rgb = C_PRIMARY
    erd_text_box.line.width = Pt(2)

    etf = erd_text_box.text_frame
    etf.word_wrap = True
    ep1 = etf.paragraphs[0]
    ep1.text = "Poin Analisis Diagram ERD:"
    ep1.font.size = Pt(12)
    ep1.font.bold = True
    ep1.font.color.rgb = C_PRIMARY

    erd_bullets = [
        "Relasi 1 to Many (1:N): Satu kategori taksonomi dapat menaungi banyak spesies satwa.",
        "Relasi 1 to Many (1:N): Satu status IUCN digunakan oleh banyak satwa yang berada di level ancaman serupa.",
        "Relasi 1 to Many (1:N): Satu kawasan habitat suaka menjadi rumah bagi berbagai satwa berbeda.",
        "Foreign Key di animals:",
        "  • category_id → categories(id)",
        "  • status_id → statuses(id)",
        "  • habitat_id → habitats(id)",
        "Sistem ini menjamin konsistensi data dan menghindari duplikasi teks tak terstruktur."
    ]
    for b in erd_bullets:
        eb = etf.add_paragraph()
        eb.text = b
        eb.font.size = Pt(9)
        eb.font.color.rgb = C_TEXT
        eb.space_before = Pt(5)

    # -------------------------------------------------------------------------
    # SLIDE 8: SCREENSHOT & PENJELASAN STRUKTUR DDL & INTEGRITAS
    # -------------------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, C_LIGHT_BG)
    add_header(slide8, "Struktur DDL, Foreign Key Constraints & Indexing", "3. SCREENSHOT & PENJELASAN DATABASE")

    ddl_img_path = os.path.join(ASSETS_DIR, "db_schema_ddl.png")
    if os.path.exists(ddl_img_path):
        slide8.shapes.add_picture(ddl_img_path, Inches(0.8), Inches(1.8), width=Inches(7.8))

    # Keterangan Integritas di sebelah kanan
    ddl_info = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.8), Inches(3.733), Inches(5.1))
    ddl_info.fill.solid()
    ddl_info.fill.fore_color.rgb = C_CARD_BG
    ddl_info.line.color.rgb = C_AMBER
    ddl_info.line.width = Pt(2)

    dtf = ddl_info.text_frame
    dtf.word_wrap = True
    dp1 = dtf.paragraphs[0]
    dp1.text = "Penjelasan Integritas & Index:"
    dp1.font.size = Pt(12)
    dp1.font.bold = True
    dp1.font.color.rgb = C_AMBER

    ddl_notes = [
        "1. ON UPDATE CASCADE:",
        "Jika Primary Key pada tabel master diubah, seluruh Foreign Key di tabel animals akan otomatis diperbarui secara instan.",
        "2. ON DELETE RESTRICT:",
        "Mencegah penghapusan habitat atau kategori yang masih digunakan oleh data satwa. Menjaga database dari data yatim (orphan records).",
        "3. Optimasi B-Tree Indexing:",
        "Index dibuat pada kolom nama_lokal, category_id, status_id, dan habitat_id.",
        "Mempercepat waktu respon pencarian WHERE dan operasi JOIN relasional dari O(N) ke O(log N)."
    ]
    for n in ddl_notes:
        np = dtf.add_paragraph()
        np.text = n
        np.font.size = Pt(9)
        np.font.color.rgb = C_TEXT
        np.space_before = Pt(5)
        if n.startswith(("1.", "2.", "3.")):
            np.font.bold = True
            np.font.color.rgb = C_PRIMARY

    # -------------------------------------------------------------------------
    # SLIDE 9: SCREENSHOT & PENJELASAN DATA GRID MYSQL WORKBENCH
    # -------------------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, C_LIGHT_BG)
    add_header(slide9, "Inspeksi Tabel & Seeder Satwa di MySQL Workbench", "3. SCREENSHOT & PENJELASAN DATABASE")

    grid_img_path = os.path.join(ASSETS_DIR, "db_data_grid.png")
    if os.path.exists(grid_img_path):
        slide9.shapes.add_picture(grid_img_path, Inches(0.8), Inches(1.8), width=Inches(11.733))

    # Keterangan Singkat di bawah gambar
    exp_bar = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.733), Inches(0.95))
    exp_bar.fill.solid()
    exp_bar.fill.fore_color.rgb = C_CARD_BG
    exp_bar.line.color.rgb = C_SECONDARY
    exp_bar.line.width = Pt(1.5)
    etf = exp_bar.text_frame
    etf.word_wrap = True
    ep = etf.paragraphs[0]
    ep.text = "Keterangan Hasil Query Relasional:"
    ep.font.size = Pt(10)
    ep.font.bold = True
    ep.font.color.rgb = C_SECONDARY
    ep2 = etf.add_paragraph()
    ep2.text = "Data satwa menampilkan keterkaitan antar-tabel (JOIN): nama_kategori diambil dari categories, nama_status dan warna_badge diambil dari conservation_statuses, serta nama_habitat dan lokasi diambil dari habitats."
    ep2.font.size = Pt(9)
    ep2.font.color.rgb = C_TEXT

    # -------------------------------------------------------------------------
    # SLIDE 10: INTEGRASI BACKEND & KONEKSI DATABASE (DB.PY)
    # -------------------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, C_LIGHT_BG)
    add_header(slide10, "Integrasi Backend Python ke MySQL (db.py & PyMySQL)", "ARSITEKTUR INTEGRASI")

    steps_db = [
        ("1. Driver Murni PyMySQL", "Tanpa Dependency Eksternal",
         "Menggunakan driver pymysql murni Python yang stabil di Windows/Linux tanpa perlu kompilasi library C."),
        ("2. DictCursor Mapping", "Kemudahan Konsumsi Data",
         "Hasil query dikembalikan sebagai Python Dictionary (animal['nama_lokal']), mempermudah mapping langsung ke template HTML Jinja2."),
        ("3. Pencegahan SQL Injection", "Prepared Statements (%s)",
         "Seluruh query pencarian dan transaksi CRUD menggunakan parameter binding (%s), melindungi sistem dari eksploitasi SQL Injection."),
        ("4. Autocommit & Pool Aman", "Konsistensi Transaksi",
         "Koneksi menggunakan autocommit=True untuk integritas data instan dan blok try-finally memastikan koneksi selalu ditutup rapi.")
    ]

    for idx, (head, sub, desc) in enumerate(steps_db):
        sx = Inches(0.8 + idx * 2.95)
        s_box = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, Inches(1.8), Inches(2.8), Inches(3.2))
        s_box.fill.solid()
        s_box.fill.fore_color.rgb = C_CARD_BG
        s_box.line.color.rgb = C_PRIMARY
        s_box.line.width = Pt(1.5)

        stf = s_box.text_frame
        stf.word_wrap = True
        sp1 = stf.paragraphs[0]
        sp1.text = head
        sp1.font.size = Pt(11)
        sp1.font.bold = True
        sp1.font.color.rgb = C_PRIMARY

        sp2 = stf.add_paragraph()
        sp2.text = sub
        sp2.font.size = Pt(9)
        sp2.font.bold = True
        sp2.font.color.rgb = C_AMBER
        sp2.space_before = Pt(3)

        sp3 = stf.add_paragraph()
        sp3.text = desc
        sp3.font.size = Pt(9)
        sp3.font.color.rgb = C_TEXT
        sp3.space_before = Pt(8)

    # Arsitektur Alur Request
    flow_box = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.2), Inches(11.733), Inches(1.7))
    flow_box.fill.solid()
    flow_box.fill.fore_color.rgb = C_DARK
    flow_box.line.fill.background()
    ftf = flow_box.text_frame
    ftf.word_wrap = True
    ftp1 = ftf.paragraphs[0]
    ftp1.text = "DIAGRAM ALUR EKSEKUSI DATA (REQUEST-RESPONSE FLOW)"
    ftp1.font.size = Pt(11)
    ftp1.font.bold = True
    ftp1.font.color.rgb = C_AMBER

    ftp2 = ftf.add_paragraph()
    ftp2.text = "Client Browser  ⟶  Flask Controller (app.py)  ⟶  PyMySQL Driver (db.py)  ⟶  MySQL 8.0 InnoDB Engine (faunaguard_db)\nHTML/CSS Response  ⟵  Jinja2 Engine Render  ⟵  PyMySQL DictCursor (JSON/Dict)  ⟵  MySQL Relational Result"
    ftp2.font.size = Pt(10)
    ftp2.font.color.rgb = C_WHITE
    ftp2.space_before = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 11: TEKNOLOGI YANG DIGUNAKAN (TECH STACK)
    # -------------------------------------------------------------------------
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, C_LIGHT_BG)
    add_header(slide11, "Teknologi yang Digunakan (Tech Stack)", "SPESIFIKASI TEKNIS")

    stacks = [
        ("🗄️ Database Tier", [
            ("RDBMS Engine", "MySQL 8.0+ / MariaDB"),
            ("Storage Engine", "InnoDB (ACID Compliant)"),
            ("Charset", "utf8mb4 (Full Emoji & Unicode)"),
            ("Management Tool", "MySQL Workbench 8.0 CE")
        ], C_PRIMARY),
        ("⚙️ Backend Tier", [
            ("Programming Language", "Python 3.13"),
            ("Web Framework", "Flask 3.0+"),
            ("MySQL Connector", "PyMySQL 1.1+ (DictCursor)"),
            ("Environment Config", "python-dotenv (.env)")
        ], C_AMBER),
        ("🎨 Frontend Tier", [
            ("Framework UI", "Bootstrap 5.3.3 CDN"),
            ("Icons Library", "Bootstrap Icons 1.11.3"),
            ("Styling System", "Vanilla CSS3 Custom Tokens"),
            ("Interaktivitas", "Vanilla JavaScript (Fetch API)")
        ], C_SECONDARY)
    ]

    for idx, (tier_title, items, col) in enumerate(stacks):
        tx = Inches(0.8 + idx * 3.95)
        st_card = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, tx, Inches(1.8), Inches(3.8), Inches(5.1))
        st_card.fill.solid()
        st_card.fill.fore_color.rgb = C_CARD_BG
        st_card.line.color.rgb = col
        st_card.line.width = Pt(2)

        stf = st_card.text_frame
        stf.word_wrap = True
        stp1 = stf.paragraphs[0]
        stp1.text = tier_title
        stp1.font.size = Pt(13)
        stp1.font.bold = True
        stp1.font.color.rgb = col

        for label, val in items:
            lp = stf.add_paragraph()
            lp.text = label
            lp.font.size = Pt(9)
            lp.font.bold = True
            lp.font.color.rgb = C_MUTED
            lp.space_before = Pt(8)

            vp = stf.add_paragraph()
            vp.text = val
            vp.font.size = Pt(10)
            vp.font.bold = True
            vp.font.color.rgb = C_TEXT

    # -------------------------------------------------------------------------
    # SLIDE 12: KESIMPULAN & PENUTUP
    # -------------------------------------------------------------------------
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, C_DARK)

    # Accent Top
    strip2 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.2))
    strip2.fill.solid()
    strip2.fill.fore_color.rgb = C_AMBER
    strip2.line.fill.background()

    # Title
    t12_box = slide12.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(1.5))
    t12_tf = t12_box.text_frame
    t12_tf.word_wrap = True
    tp_12 = t12_tf.paragraphs[0]
    tp_12.text = "Kesimpulan & Nilai Tambah Proyek"
    tp_12.font.size = Pt(32)
    tp_12.font.bold = True
    tp_12.font.color.rgb = C_WHITE

    tp_12_sub = t12_tf.add_paragraph()
    tp_12_sub.text = "Sinergi Arsitektur Basis Data Relasional & Edukasi Hayati Hutan Tropis Kalimantan"
    tp_12_sub.font.size = Pt(15)
    tp_12_sub.font.color.rgb = C_SAND
    tp_12_sub.space_before = Pt(6)

    # 3 Summary Cards
    conclusions = [
        ("Integritas Data Solid", "Normalisasi 3NF dan Foreign Key CASCADE/RESTRICT menjamin data selalu konsisten dan bebas dari anomali pembaruan atau penghapusan."),
        ("Pengalaman Pengguna Ramah", "Desain visual bertema hutan Kalimantan dengan filter interaktif, modal cepat tanpa reload, dan manajemen data yang mudah digunakan."),
        ("Mendukung Konservasi Nyata", "Bukan sekadar aplikasi web biasa, FaunaGuard hadir sebagai media advokasi dan edukasi nyata dalam melindungi satwa langka Borneo.")
    ]

    for idx, (c_head, c_body) in enumerate(conclusions):
        cx = Inches(1.0 + idx * 3.8)
        c_box = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(3.0), Inches(3.6), Inches(2.8))
        c_box.fill.solid()
        c_box.fill.fore_color.rgb = RGBColor(20, 75, 58)
        c_box.line.color.rgb = C_AMBER
        c_box.line.width = Pt(1.5)

        ctf = c_box.text_frame
        ctf.word_wrap = True
        cp1 = ctf.paragraphs[0]
        cp1.text = c_head
        cp1.font.size = Pt(12)
        cp1.font.bold = True
        cp1.font.color.rgb = C_SAND

        cp2 = ctf.add_paragraph()
        cp2.text = c_body
        cp2.font.size = Pt(9.5)
        cp2.font.color.rgb = RGBColor(230, 240, 235)
        cp2.space_before = Pt(10)

    # Footer Team
    team_box = slide12.shapes.add_textbox(Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.8))
    ttf_t = team_box.text_frame
    tp_t = ttf_t.paragraphs[0]
    tp_t.text = "Tim Pengembang FaunaGuard: Anggota 1 (Database) • Anggota 2 (Backend) • Anggota 3 (Frontend UI) • Anggota 4 (Frontend CRUD)"
    tp_t.font.size = Pt(11)
    tp_t.font.bold = True
    tp_t.font.color.rgb = C_AMBER
    tp_t.alignment = PP_ALIGN.CENTER

    output_pptx_path = os.path.join(OUTPUT_DIR, "FaunaGuard_Presentasi_Web_dan_Database.pptx")
    prs.save(output_pptx_path)
    print("PowerPoint presentation generated successfully:", output_pptx_path)
    return output_pptx_path


if __name__ == "__main__":
    print("Mulai membuat aset visual & presentasi PPT...")
    generate_erd_diagram()
    generate_db_data_grid()
    generate_sql_ddl_box()
    pptx_file = build_powerpoint()
    print("Selesai! File tersimpan di:", pptx_file)

