CREATE CONSTRAINT fund_id_unique
IF NOT EXISTS
FOR (n:Fund)
REQUIRE n.fund_id IS UNIQUE;

CREATE CONSTRAINT holding_id_unique
IF NOT EXISTS
FOR (n:Holding)
REQUIRE n.holding_id IS UNIQUE;

CREATE CONSTRAINT issuer_id_unique
IF NOT EXISTS
FOR (n:Issuer)
REQUIRE n.issuer_id IS UNIQUE;

CREATE CONSTRAINT parent_issuer_id_unique
IF NOT EXISTS
FOR (n:ParentIssuer)
REQUIRE n.parent_id IS UNIQUE;

CREATE CONSTRAINT asset_class_id_unique
IF NOT EXISTS
FOR (n:AssetClass)
REQUIRE n.asset_class_id IS UNIQUE;

CREATE CONSTRAINT limit_id_unique
IF NOT EXISTS
FOR (n:Limit)
REQUIRE n.limit_id IS UNIQUE;

CREATE CONSTRAINT metric_id_unique
IF NOT EXISTS
FOR (n:Metric)
REQUIRE n.metric_id IS UNIQUE;

CREATE CONSTRAINT action_id_unique
IF NOT EXISTS
FOR (n:BreachAction)
REQUIRE n.action_id IS UNIQUE;

CREATE CONSTRAINT document_id_unique
IF NOT EXISTS
FOR (n:SourceDocument)
REQUIRE n.document_id IS UNIQUE;

CREATE CONSTRAINT citation_id_unique
IF NOT EXISTS
FOR (n:SourceCitation)
REQUIRE n.citation_id IS UNIQUE;