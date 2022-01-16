create_push = """
INSERT INTO
    push (site_id, title, launch_url, options)
VALUES
    ($1, $2, $3, $4) RETURNING id,
    site_id,
    title,
    launch_url,
    options;
"""

fetch_push = """
SELECT *
FROM push
WHERE id = $1;
"""

update_push = """
UPDATE push
SET {}
WHERE id=%(id)s
"""

delete_push = """
DELETE FROM push WHERE %(id)s
"""
