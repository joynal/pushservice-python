create_subscriber = """
INSERT INTO
    subscriber (site_id, endpoint)
VALUES 
    ($1, $2) RETURNING id,
    site_id,
    subscribed,
    endpoint;
"""
