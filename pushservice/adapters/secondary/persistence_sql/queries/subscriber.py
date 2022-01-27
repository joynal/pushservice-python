create_subscriber = """
INSERT INTO
    subscriber (site_id, subscription_info)
VALUES 
    (%(site_id)s, %(subscription_info)s) RETURNING id,
    site_id,
    subscribed,
    subscription_info;
"""

fetch_subscriber = """
SELECT *
FROM subscriber
WHERE id=$1;
"""

fetch_stream = """
SELECT *
FROM subscriber
WHERE site_id=$1 AND subscribed=true;
"""
