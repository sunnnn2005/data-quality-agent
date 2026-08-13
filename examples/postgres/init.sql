CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id TEXT,
    team TEXT,
    priority TEXT,
    status TEXT,
    amount NUMERIC,
    created_at TIMESTAMP
);

TRUNCATE TABLE support_tickets;

INSERT INTO support_tickets (ticket_id, team, priority, status, amount, created_at) VALUES
    ('TCK-1001', 'billing', 'high', 'open', 42.50, '2026-08-01 09:15:00'),
    ('TCK-1002', 'platform', 'medium', 'open', 88.00, '2026-08-01 10:20:00'),
    ('TCK-1003', NULL, 'low', 'closed', 16.75, '2026-08-01 10:45:00'),
    ('TCK-1004', 'billing', NULL, 'open', 51.30, '2026-08-01 11:05:00'),
    ('TCK-1004', 'billing', NULL, 'open', 51.30, '2026-08-01 11:05:00'),
    ('TCK-1006', 'support', 'critical', 'open', -12.00, '2026-08-01 12:30:00'),
    ('TCK-1007', 'support', 'high', 'open', 1350.00, '2026-08-01 13:10:00'),
    ('TCK-1008', 'platform', 'medium', 'closed', 72.10, '2026-08-01 13:45:00');

CREATE USER readonly_agent WITH PASSWORD 'readonly_agent';
GRANT CONNECT ON DATABASE quality_demo TO readonly_agent;
GRANT USAGE ON SCHEMA public TO readonly_agent;
GRANT SELECT ON support_tickets TO readonly_agent;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO readonly_agent;
