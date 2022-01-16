create_site = """
INSERT INTO
    site (public_key, private_key)
VALUES
    ( $1, $2) RETURNING id,
    public_key,
    private_key;
"""

fetch_site = """
SELECT *
FROM site
WHERE id = $1;
"""
