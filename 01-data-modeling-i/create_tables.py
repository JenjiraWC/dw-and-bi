from typing import NewType

import psycopg2


PostgresCursor = NewType("PostgresCursor", psycopg2.extensions.cursor)
PostgresConn = NewType("PostgresConn", psycopg2.extensions.connection)

table_drop_users = "DROP TABLE IF EXISTS users CASCADE"
table_drop_events = "DROP TABLE IF EXISTS events CASCADE"
table_drop_actors = "DROP TABLE IF EXISTS actors"
table_drop_repo = "DROP TABLE IF EXISTS repo"
table_drop_payload = "DROP TABLE IF EXISTS payload CASCADE"
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

table_create_events = """
    CREATE TABLE IF NOT EXISTS events (
        id bigint,
        type text,
        actor_id bigint,
        repo_id bigint,
        public text,
        created_at text,
        payload text,
        PRIMARY KEY(id),
        CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id),
        CONSTRAINT fk_repo FOREIGN KEY(repo_id) REFERENCES repo(id)
    )
"""

create_table_queries = [
    table_create_actors,
    table_create_repo,
    table_create_users,
    table_create_author,
    table_create_release,
    table_create_events,
]

drop_table_queries = [
    table_drop_events,
    table_drop_actors,
    table_drop_repo,
    table_drop_payload,
    table_drop_users,
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
