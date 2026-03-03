-- ==========================
-- DROP (cuidado em produção)
-- ==========================
DROP TABLE IF EXISTS game_progress;
DROP TABLE IF EXISTS games;

-- ==========================
-- TABELA GAMES
-- ==========================
CREATE TABLE games (
    id UUID PRIMARY KEY,
    room_id UUID NOT NULL,
    text TEXT NOT NULL,
    text_size INTEGER NOT NULL,
    state VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_game_room
        FOREIGN KEY (room_id)
        REFERENCES rooms(id)
        ON DELETE CASCADE
);

-- ==========================
-- TABELA GAME_PROGRESS
-- ==========================
CREATE TABLE game_progress (
    game_id UUID NOT NULL,
    user_id UUID NOT NULL,

    progress FLOAT DEFAULT 0,
    progress_index INTEGER DEFAULT 0,

    typed_characters INTEGER DEFAULT 0,
    errors INTEGER DEFAULT 0,
    elapsed_time FLOAT DEFAULT 0,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (game_id, user_id),

    CONSTRAINT fk_progress_game
        FOREIGN KEY (game_id)
        REFERENCES games(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_progress_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);