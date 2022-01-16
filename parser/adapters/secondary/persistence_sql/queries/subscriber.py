create_subscriber = """
INSERT INTO
    subscriber (site_id, endpoint)
VALUES 
    ($1, $2) RETURNING id,
    site_id,
    subscribed,
    endpoint;
"""

fetch_subscriber = """
SELECT *
FROM subscriber
WHERE id = $1;
"""

fetch_stream = """
SELECT *
FROM subscriber
WHERE site_id=$1 AND subscribed=true;
"""
