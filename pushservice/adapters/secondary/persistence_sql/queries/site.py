create_site = """
INSERT INTO
    site (public_key, private_key)
VALUES
    (%(public_key)s, %(private_key)s) RETURNING id,
    public_key,
    private_key;
"""

fetch_site = """
SELECT *
FROM site
WHERE id=$1;
"""
