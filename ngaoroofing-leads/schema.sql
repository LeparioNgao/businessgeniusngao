CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    phone TEXT,
    email TEXT,
    company TEXT,
    source TEXT,
    project_type TEXT,
    location TEXT,
    estimated_roof_area REAL CHECK (estimated_roof_area IS NULL OR estimated_roof_area >= 0),
    product_profile TEXT,
    inquiry_date TEXT NOT NULL,
    status TEXT NOT NULL CHECK (
        status IN (
            'NEW',
            'QUALIFIED',
            'QUOTED',
            'FOLLOW-UP',
            'SITE VISIT',
            'NEGOTIATION',
            'WON',
            'LOST',
            'DORMANT'
        )
    ),
    notes TEXT,
    next_action TEXT,
    next_follow_up_date TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    archived_at TEXT
);

CREATE TABLE IF NOT EXISTS follow_ups (
    id INTEGER PRIMARY KEY,
    lead_id INTEGER NOT NULL,
    contact_date TEXT NOT NULL,
    contact_method TEXT,
    what_happened TEXT,
    customer_response TEXT,
    outcome TEXT,
    next_action TEXT,
    next_follow_up_date TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads (id) ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_leads_status ON leads (status);
CREATE INDEX IF NOT EXISTS idx_leads_next_follow_up_date ON leads (next_follow_up_date);
CREATE INDEX IF NOT EXISTS idx_follow_ups_lead_id ON follow_ups (lead_id);