-- LOG_TYPE
CREATE TABLE IF NOT EXISTS log_type (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        is_active BOOLEAN,
        additional_info TEXT,
        login_required BOOLEAN
);

-- LOG
CREATE TABLE IF NOT EXISTS log (
    id SERIAL PRIMARY KEY,
    type INTEGER REFERENCES log_type(id),
    time TIMESTAMP,
    text TEXT,
    session_id INTEGER,
    server_response VARCHAR(255),
    user_id INTEGER
);
