-- users
CREATE TABLE IF NOT EXISTS users (
  id BIGSERIAL PRIMARY KEY,
  name        VARCHAR(120) NOT NULL,
  email       VARCHAR(255) NOT NULL UNIQUE,
  timezone    VARCHAR(64)  NOT NULL DEFAULT 'America/Sao_Paulo',
  created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- medicines (pertencem ao usuário)
CREATE TABLE IF NOT EXISTS medicines (
  id BIGSERIAL PRIMARY KEY,
  user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name        VARCHAR(120) NOT NULL,
  dose_amount NUMERIC(10,2) NOT NULL,
  dose_unit   VARCHAR(16)  NOT NULL DEFAULT 'mg',
  notes       TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_meds_user ON medicines(user_id);

-- reminders (agenda de tomadas)
CREATE TABLE IF NOT EXISTS reminders (
  id BIGSERIAL PRIMARY KEY,
  user_id      BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  medicine_id  BIGINT NOT NULL REFERENCES medicines(id) ON DELETE CASCADE,
  start_date   DATE   NOT NULL,
  end_date     DATE,
  times_of_day TIME[] NOT NULL,  -- ex: '{08:00,14:00,20:00}'
  days_mask    INT    NOT NULL DEFAULT 127, -- bitmask dom(1)…sáb(64); 127=todos os dias
  next_run_at  TIMESTAMPTZ,      -- calculado pelo serviço
  active       BOOLEAN NOT NULL DEFAULT TRUE,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT ck_times_not_empty CHECK (array_length(times_of_day,1) >= 1),
  CONSTRAINT ck_date_range CHECK (end_date IS NULL OR end_date >= start_date)
);
CREATE INDEX IF NOT EXISTS idx_reminders_user_next ON reminders(user_id, next_run_at) WHERE active = TRUE;
