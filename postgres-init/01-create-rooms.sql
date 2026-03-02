DROP TABLE IF EXISTS rooms; -- Cuidado: isso apaga os dados atuais

CREATE TABLE rooms (
    id UUID PRIMARY KEY, -- Mudança para o tipo nativo
    state VARCHAR(20),
    id_admin VARCHAR(50),
    data JSONB
);