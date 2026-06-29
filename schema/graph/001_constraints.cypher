// =====================================================
// Constraints
// =====================================================

CREATE CONSTRAINT profile_name IF NOT EXISTS
FOR (p:Profile)
REQUIRE p.name IS UNIQUE;

CREATE CONSTRAINT metric_id IF NOT EXISTS
FOR (m:Metric)
REQUIRE m.id IS UNIQUE;

CREATE CONSTRAINT guideline_id IF NOT EXISTS
FOR (g:Guideline)
REQUIRE g.id IS UNIQUE;

CREATE CONSTRAINT rule_id IF NOT EXISTS
FOR (r:Rule)
REQUIRE r.id IS UNIQUE;

CREATE CONSTRAINT citation_id IF NOT EXISTS
FOR (c:Citation)
REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT asset_class_name IF NOT EXISTS
FOR (a:AssetClass)
REQUIRE a.name IS UNIQUE;

CREATE CONSTRAINT issuer_name IF NOT EXISTS
FOR (i:Issuer)
REQUIRE i.name IS UNIQUE;

CREATE CONSTRAINT holding_id IF NOT EXISTS
FOR (h:Holding)
REQUIRE h.instrument_id IS UNIQUE;