CREATE TABLE IF NOT EXISTS ad_events (
  id SERIAL PRIMARY KEY,
  action VARCHAR(25) CHECK (action IN ('click', 'view', 'impression')),
  location VARCHAR(25) NOT NULL DEFAULT 'Unknown',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);