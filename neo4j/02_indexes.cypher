CREATE INDEX holding_rating_idx
IF NOT EXISTS
FOR (n:Holding)
ON (n.rating);

CREATE INDEX holding_market_value_idx
IF NOT EXISTS
FOR (n:Holding)
ON (n.market_value);

CREATE INDEX asset_class_name_idx
IF NOT EXISTS
FOR (n:AssetClass)
ON (n.name);

CREATE INDEX issuer_name_idx
IF NOT EXISTS
FOR (n:Issuer)
ON (n.issuer_name);

CREATE INDEX limit_name_idx
IF NOT EXISTS
FOR (n:Limit)
ON (n.name);

CREATE INDEX metric_name_idx
IF NOT EXISTS
FOR (n:Metric)
ON (n.name); 