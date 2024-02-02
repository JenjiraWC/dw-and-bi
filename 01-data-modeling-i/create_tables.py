from typing import NewType

import psycopg2


PostgresCursor = NewType("PostgresCursor", psycopg2.extensions.cursor)
PostgresConn = NewType("PostgresConn", psycopg2.extensions.connection)

table_drop_users = "DROP TABLE IF EXISTS users CASCADE"
table_drop_events = "DROP TABLE IF EXISTS events CASCADE"
table_drop_actors = "DROP TABLE IF EXISTS actors"
table_drop_repo = "DROP TABLE IF EXISTS repo"
table_drop_org = "DROP TABLE IF EXISTS org"
table_drop_creator = "DROP TABLE IF EXISTS creator CASCADE"
table_drop_reaction = "DROP TABLE IF EXISTS reaction"
table_drop_comment = "DROP TABLE IF EXISTS comment CASCADE"
table_drop_milestone = "DROP TABLE IF EXISTS milestone CASCADE"
table_drop_payload = "DROP TABLE IF EXISTS payload CASCADE"
table_drop_issue = "DROP TABLE IF EXISTS issue CASCADE"
table_drop_author = "DROP TABLE IF EXISTS author CASCADE"
table_drop_release = "DROP TABLE IF EXISTS release CASCADE"

table_create_actors = """
    CREATE TABLE IF NOT EXISTS actors (
        id bigint,
        login text,
        PRIMARY KEY(id)
    )
"""
table_create_repo = """
    CREATE TABLE IF NOT EXISTS repo (
        id bigint,
        name text,
        PRIMARY KEY(id)
    )
"""
table_create_org = """
    CREATE TABLE IF NOT EXISTS org (
        id bigint,
        login text,
        PRIMARY KEY(id)
    )
"""

table_create_creator = """
    CREATE TABLE IF NOT EXISTS creator (
        id bigint,
        login text,
        url text,
        type text,
        site_admin text,
        PRIMARY KEY(id)
    )
"""

table_create_users = """
    CREATE TABLE IF NOT EXISTS users (
        id bigint,
        login text,
        url text,
        type text,
        site_admin text,
        PRIMARY KEY(id)
    )
"""
table_create_author = """
    CREATE TABLE IF NOT EXISTS author (
        id bigint,
        login text,
        type text,
        PRIMARY KEY(id)
    )
"""
table_create_release = """
    CREATE TABLE IF NOT EXISTS release (
        id bigint,
        url text,
        author_id bigint,
        name text,
        created_at text,
        published_at text,
        PRIMARY KEY(id),
        CONSTRAINT fk_author_release FOREIGN KEY(author_id) REFERENCES author(id)
    )
"""

table_create_comment = """
    CREATE TABLE IF NOT EXISTS comment (
        id bigint,
        url text,
        users_id bigint,
        PRIMARY KEY(id),
        CONSTRAINT fk_users_comment FOREIGN KEY(users_id) REFERENCES users(id)
    )
"""

table_create_milestone = """
    CREATE TABLE IF NOT EXISTS milestone (
        id bigint,
        url text,
        number int,
        title text,
        creator_id bigint,
        open_issues text,
        close_issues text, 
        state text,
        created_at text,
        update_at text,
        close_at text,
        PRIMARY KEY(id),
        CONSTRAINT fk_creator FOREIGN KEY(creator_id) REFERENCES creator(id)
    )
"""

table_create_issue = """
    CREATE TABLE IF NOT EXISTS issue (
        id bigint,
        number int,
        title text,
        users_id bigint,
        comments int,
        created_at text,
        updated_at text,
        close_at text,
        state text,
        locked text,
        milestone_id bigint,
        PRIMARY KEY(id),
        CONSTRAINT fk_users_issue FOREIGN KEY(users_id) REFERENCES users(id),
        CONSTRAINT fk_milestone_issue FOREIGN KEY(milestone_id) REFERENCES milestone(id)
    )
"""

table_create_reaction = """
    CREATE TABLE IF NOT EXISTS reaction (
        issue_id bigint,
        total_count int,
        "+1" int,
        "-1" int,
        laugh int,
        hooray int,
        confused int,
        heart int,
        rocket int,
        eyes int,
        CONSTRAINT fk_issuereac FOREIGN KEY(issue_id) REFERENCES issue(id)
    )
"""

table_create_events = """
    CREATE TABLE IF NOT EXISTS events (
        id bigint,
        type text,
        actor_id bigint,
        repo_id bigint,
        public text,
        created_at text,
        payload bigint,
        org_id bigint,
        PRIMARY KEY(id),
        CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id),
        CONSTRAINT fk_repo FOREIGN KEY(repo_id) REFERENCES repo(id),
        CONSTRAINT fk_org FOREIGN KEY(org_id) REFERENCES org(id),
        CONSTRAINT fk_payload FOREIGN KEY(payload) REFERENCES issue(id)
    )
"""

table_create_payload = """
    CREATE TABLE IF NOT EXISTS payload (
        events_id bigint,
        action text,
        issue_id bigint,
        push_id bigint,
        size int,
        distinct_size int,
        comment int,
        ref text,
        ref_type text,
        master_branch text,
        pusher_type text,
        commit_url text,
        release_id bigint,
        CONSTRAINT fk_events FOREIGN KEY(events_id) REFERENCES events(id),
        CONSTRAINT fk_issue FOREIGN KEY(issue_id) REFERENCES issue(id),
        CONSTRAINT fk_comment FOREIGN KEY(comment) REFERENCES comment(id),
        CONSTRAINT fk_release FOREIGN KEY(release_id) REFERENCES release(id)
    )
"""

create_table_queries = [
    table_create_actors,
    table_create_repo,
    table_create_org,
    table_create_creator,
    table_create_users,
    table_create_author,
    table_create_release,
    table_create_comment,
    table_create_milestone,
    table_create_issue,
    table_create_reaction,
    table_create_events,
    table_create_payload,
]
drop_table_queries = [
    table_drop_events,
    table_drop_actors,
    table_drop_repo,
    table_drop_org,
    table_drop_creator,
    table_drop_reaction,
    table_drop_comment,
    table_drop_milestone,
    table_drop_payload,
    table_drop_users,
    table_drop_issue,
    table_drop_author,
    table_drop_release,
]


def drop_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur: PostgresCursor, conn: PostgresConn) -> None:
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database.
    - Establishes connection with the sparkify database and gets
    cursor to it.
    - Drops all the tables.
    - Creates all tables needed.
    - Finally, closes the connection.
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
