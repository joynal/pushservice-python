create_push = """
INSERT INTO
    push (site_id, title, launch_url, options)
VALUES
    (%(site_id)s, %(title)s, %(launch_url)s, %(options)s) RETURNING id,
    site_id,
    title,
    launch_url,
    options;
"""

fetch_push = """
SELECT *
FROM push
WHERE id=$1;
"""

update_push = """
UPDATE push
SET {}
WHERE id=%(id)s::uuid;
"""

delete_push = """
DELETE FROM push WHERE id=$1;
"""
