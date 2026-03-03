-- ==========================
-- DROP (cuidado produção)
-- ==========================
DROP TABLE IF EXISTS game_results;

-- ==========================
-- TABELA GAME_RESULTS
-- ==========================
CREATE TABLE game_results (
    game_id UUID NOT NULL,
    user_id UUID NOT NULL,

    name VARCHAR(100) NOT NULL,
    position INTEGER NOT NULL,
    wpm FLOAT NOT NULL,
    final_time FLOAT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (game_id, user_id),

    CONSTRAINT fk_result_game
        FOREIGN KEY (game_id)
        REFERENCES games(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_result_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);