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
