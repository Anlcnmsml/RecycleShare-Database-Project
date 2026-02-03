-- =============================================================
-- RECYCLESHARE PROJESİ - VERİTABANI ŞEMASI (SCHEMA.SQL)
-- =============================================================

-- NOT: Bu dosyayı çalıştırmadan önce pgAdmin'de "RecycleShareDB" 
-- adında boş bir veritabanı oluşturduğunuzdan emin olun.

-- -------------------------------------------------------------
-- 1. TABLOLAR (Maddeler: 1, 2, 3, 8, 13)
-- -------------------------------------------------------------

-- 1.1. Kullanıcılar Tablosu
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY, -- Madde 8: Sequence (SERIAL)
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
    -- Madde 13: Kullanıcı Rolleri (Admin, User, Collector)
    CONSTRAINT chk_user_role CHECK (role IN ('admin', 'user', 'collector'))
);

-- 1.2. Kategoriler Tablosu
CREATE TABLE IF NOT EXISTS categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    points_per_kg DECIMAL(5,2) DEFAULT 1.0
);

-- 1.3. Atık İlanları Tablosu
CREATE TABLE IF NOT EXISTS waste_items (
    item_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    description TEXT,
    weight_kg DECIMAL(10,2) NOT NULL,
    location VARCHAR(100),
    status VARCHAR(20) DEFAULT 'Available',
    created_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
    
    -- Madde 2: Foreign Key Kısıtları
    CONSTRAINT fk_waste_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_waste_category FOREIGN KEY (category_id) REFERENCES categories(category_id),

    -- Madde 3: Sayı Kısıtı (Check)
    CONSTRAINT chk_waste_status CHECK (status IN ('Available', 'Reserved', 'Recycled')),
    CONSTRAINT chk_waste_weight CHECK (weight_kg > 0)
);

-- 1.4. Rezervasyonlar Tablosu
CREATE TABLE IF NOT EXISTS bookings (
    booking_id SERIAL PRIMARY KEY,
    item_id INTEGER NOT NULL UNIQUE,
    collector_id INTEGER NOT NULL,
    booking_date TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
    
    -- Madde 3: Silme Kısıtı
    CONSTRAINT fk_booking_item FOREIGN KEY (item_id) REFERENCES waste_items(item_id) ON DELETE RESTRICT,
    CONSTRAINT fk_booking_collector FOREIGN KEY (collector_id) REFERENCES users(user_id)
);

-- 1.5. Değerlendirmeler Tablosu
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    reviewer_id INTEGER NOT NULL,
    target_user_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5), -- Sayı Kısıtı
    comment TEXT,
    created_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reviewer FOREIGN KEY (reviewer_id) REFERENCES users(user_id),
    CONSTRAINT fk_target_user FOREIGN KEY (target_user_id) REFERENCES users(user_id)
);

-- 1.6. Mesajlar Tablosu
CREATE TABLE IF NOT EXISTS messages (
    message_id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    message_content TEXT,
    sent_at TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sender FOREIGN KEY (sender_id) REFERENCES users(user_id),
    CONSTRAINT fk_receiver FOREIGN KEY (receiver_id) REFERENCES users(user_id)
);

-- -------------------------------------------------------------
-- 2. GÖRÜNÜMLER (VIEWS) (Maddeler: 6, 9, 10)
-- -------------------------------------------------------------

-- Madde 6: Raporlama View'ı
CREATE OR REPLACE VIEW v_user_impact_report AS
SELECT u.username, COUNT(w.item_id) as total_items, COALESCE(SUM(w.weight_kg), 0) as total_kg, u.score
FROM users u
LEFT JOIN waste_items w ON u.user_id = w.user_id AND w.status = 'Recycled'
GROUP BY u.username, u.score;

-- Madde 9: UNION Kullanımı (Tüm Rolleri Birleştirme)
CREATE OR REPLACE VIEW v_all_roles_union AS
SELECT username, role FROM users WHERE role = 'user'
UNION
SELECT username, role FROM users WHERE role = 'collector';

-- Madde 10: AGGREGATE ve HAVING Kullanımı (Yüksek Ağırlıklı Kategoriler)
CREATE OR REPLACE VIEW v_high_value_categories AS
SELECT c.name, AVG(w.weight_kg) as avg_weight
FROM waste_items w
JOIN categories c ON w.category_id = c.category_id
GROUP BY c.name
HAVING AVG(w.weight_kg) > 2.0;

-- -------------------------------------------------------------
-- 3. FONKSİYONLAR (Maddeler: 5, 11)
-- -------------------------------------------------------------

-- 3.1. Puan Ekleme
CREATE OR REPLACE FUNCTION update_user_score(target_id INT, points INT) RETURNS VOID AS $$
BEGIN
    UPDATE users SET score = score + points WHERE user_id = target_id;
END;
$$ LANGUAGE plpgsql;

-- 3.2. Hesaplama
CREATE OR REPLACE FUNCTION calculate_potential_points(weight_val DECIMAL, cat_id INT) RETURNS DECIMAL AS $$
DECLARE
    factor DECIMAL;
BEGIN
    SELECT points_per_kg INTO factor FROM categories WHERE category_id = cat_id;
    RETURN weight_val * COALESCE(factor, 0);
END;
$$ LANGUAGE plpgsql;

-- 3.3. Kategori Toplamı
CREATE OR REPLACE FUNCTION get_total_waste_by_category(cat_name VARCHAR) RETURNS DECIMAL AS $$
DECLARE
    total_weight DECIMAL;
BEGIN
    SELECT SUM(w.weight_kg) INTO total_weight
    FROM waste_items w
    JOIN categories c ON w.category_id = c.category_id
    WHERE c.name = cat_name;
    RETURN COALESCE(total_weight, 0);
END;
$$ LANGUAGE plpgsql;

-- 3.4. Cursor ve Record Kullanımı (Madde 11 & 5)
CREATE OR REPLACE FUNCTION list_waste_status_by_location(loc_name VARCHAR) RETURNS TEXT AS $$
DECLARE
    waste_cursor CURSOR FOR SELECT status, COUNT(*) as cnt FROM waste_items WHERE location = loc_name GROUP BY status;
    rec RECORD;
    out_text TEXT := 'Bölge Raporu: ';
BEGIN
    OPEN waste_cursor;
    LOOP
        FETCH waste_cursor INTO rec;
        EXIT WHEN NOT FOUND;
        out_text := out_text || rec.status || ': ' || rec.cnt || ', ';
    END LOOP;
    CLOSE waste_cursor;
    IF out_text = 'Bölge Raporu: ' THEN RETURN 'Bu bölgede veri bulunamadı.'; END IF;
    RETURN out_text;
END;
$$ LANGUAGE plpgsql;

-- -------------------------------------------------------------
-- 4. TETİKLEYİCİLER (Maddeler: 12)
-- -------------------------------------------------------------

-- 4.1. Durum Güncelleme
CREATE OR REPLACE FUNCTION trg_func_update_status() RETURNS TRIGGER AS $$
BEGIN
    UPDATE waste_items SET status = 'Reserved' WHERE item_id = NEW.item_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_booking_made ON bookings;
CREATE TRIGGER trg_booking_made AFTER INSERT ON bookings
FOR EACH ROW EXECUTE FUNCTION trg_func_update_status();

-- 4.2. Hata Mesajı Döndürme (Negatif Ağırlık)
CREATE OR REPLACE FUNCTION trg_func_check_weight() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.weight_kg <= 0 THEN
        RAISE EXCEPTION 'Hata: Ağırlık 0 veya negatif olamaz!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_check_waste_weight ON waste_items;
CREATE TRIGGER trg_check_waste_weight BEFORE INSERT ON waste_items
FOR EACH ROW EXECUTE FUNCTION trg_func_check_weight();

-- 4.3. Silme Koruması
CREATE OR REPLACE FUNCTION trg_func_prevent_delete() RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IN ('Reserved', 'Recycled') THEN
        RAISE EXCEPTION 'Hata: Rezerve edilmiş veya tamamlanmış işlemler silinemez!';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_prevent_waste_deletion ON waste_items;
CREATE TRIGGER trg_prevent_waste_deletion BEFORE DELETE ON waste_items
FOR EACH ROW EXECUTE FUNCTION trg_func_prevent_delete();

-- -------------------------------------------------------------
-- 5. İNDEKSLER (Madde: 7)
-- -------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_waste_location ON waste_items(location);
CREATE INDEX IF NOT EXISTS idx_waste_category ON waste_items(category_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);