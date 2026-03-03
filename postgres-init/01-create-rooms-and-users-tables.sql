-- CUIDADO: apaga tudo
DROP TABLE IF EXISTS room_users;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS rooms;

-- ==========================
-- TABELA ROOMS
-- ==========================
CREATE TABLE rooms (
    id UUID PRIMARY KEY,
    room_code VARCHAR(6) UNIQUE NOT NULL,
    port INTEGER,
    state VARCHAR(20) NOT NULL,
    id_admin UUID NOT NULL,
    game JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- TABELA USERS
-- ==========================
CREATE TABLE users (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    is_host BOOLEAN DEFAULT FALSE,
    avatar_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================
-- TABELA RELACIONAMENTO
-- ==========================
CREATE TABLE room_users (
    room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY (room_id, user_id)
);

-- ==========================
-- FOREIGN KEY DO ADMIN
-- ==========================
ALTER TABLE rooms
ADD CONSTRAINT fk_room_admin
FOREIGN KEY (id_admin)
REFERENCES users(id)
ON DELETE CASCADE;