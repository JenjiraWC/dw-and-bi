from typing import NewType

import psycopg2


PostgresCursor = NewType("PostgresCursor", psycopg2.extensions.cursor)
PostgresConn = NewType("PostgresConn", psycopg2.extensions.connection)

table_drop_account = "DROP TABLE IF EXISTS account CASCADE"
table_drop_events = "DROP TABLE IF EXISTS events"
table_drop_actors = "DROP TABLE IF EXISTS actors"
table_drop_repo = "DROP TABLE IF EXISTS repo"
table_drop_org = "DROP TABLE IF EXISTS org"
table_drop_creator = "DROP TABLE IF EXISTS creator CASCADE"
table_drop_reaction = "DROP TABLE IF EXISTS reaction"
table_drop_comment = "DROP TABLE IF EXISTS comment"
table_drop_milestone = "DROP TABLE IF EXISTS milestone"
table_drop_labels = "DROP TABLE IF EXISTS labels"
table_drop_payload = "DROP TABLE IF EXISTS payload"
table_drop_issue = "DROP TABLE IF EXISTS issue"



table_create_actors = """
    CREATE TABLE IF NOT EXISTS actors (
        id int,
        login text,
        url text,
        PRIMARY KEY(id)
    )
"""
table_create_repo = """
    CREATE TABLE IF NOT EXISTS repo (
        id int,
        name text,
        url text,
        PRIMARY KEY(id)
    )
"""
table_create_org = """
    CREATE TABLE IF NOT EXISTS org (
        id int,
        login text,
        url text,
        PRIMARY KEY(id)
    )
"""

table_create_creator = """
    CREATE TABLE IF NOT EXISTS creator (
        id int,
        login text,
        url text,
        node_id int,
        type text,
        site_admin text,
        PRIMARY KEY(id)
    )
"""
table_create_account = """
    CREATE TABLE IF NOT EXISTS account (
        id int,
        login text,
        url text,
        node_id int,
        type text,
        site_admin text,
        PRIMARY KEY(id)
    )
"""
table_create_labels = """
    CREATE TABLE IF NOT EXISTS labels (
        id int,
        url text,
        node_id int,
        name text,
        PRIMARY KEY(id)
    )
"""
table_create_comment = """
    CREATE TABLE IF NOT EXISTS comment (
        id int,
        url text,
        node_id int,
        account_id int,
        PRIMARY KEY(id),
        CONSTRAINT fk_account FOREIGN KEY(account_id) REFERENCES account(id)
    )
"""
table_create_issue = """
    CREATE TABLE IF NOT EXISTS issue (
        id int,
        url text UNIQUE,
        node_id int,
        number int,
        title text,
        is_account_id int,
        comments int,
        created_at timestamp,
        updated_at timestamp,
        close_at timestamp,
        state text,
        locked text,
        PRIMARY KEY(id),
        CONSTRAINT fk_issue_account FOREIGN KEY(is_account_id) REFERENCES account(id)
    )
"""
table_create_reaction = """
    CREATE TABLE IF NOT EXISTS reaction (
        issueurl text,
        total_count int,
        "+1" int,
        "-1" int,
        laugh int,
        hooray int,
        confused int,
        heart int,
        rocket int,
        eyes int,
        CONSTRAINT fk_issueurl FOREIGN KEY(issueurl) REFERENCES issue(url)
    )
"""

table_create_milestone = """
    CREATE TABLE IF NOT EXISTS milestone (
        id int,
        url text,
        node_id int,
        number int,
        title text,
        creator_id int,
        open_issues text,
        close_issues text, 
        state text,
        created_at timestamp,
        update_at timestamp,
        close_at timestamp,
        PRIMARY KEY(id),
        CONSTRAINT fk_creator FOREIGN KEY(creator_id) REFERENCES creator(id)
    )
"""

table_create_events = """
    CREATE TABLE IF NOT EXISTS events (
        id int,
        type text,
        actor_id int,
        repo_id int,
        public text,
        created_at timestamp,
        org_id int,
        PRIMARY KEY(id),
        CONSTRAINT fk_actor FOREIGN KEY(actor_id) REFERENCES actors(id),
        CONSTRAINT fk_repo FOREIGN KEY(repo_id) REFERENCES repo(id),
        CONSTRAINT fk_org FOREIGN KEY(org_id) REFERENCES org(id)
    )
"""
table_create_payload = """
    CREATE TABLE IF NOT EXISTS payload (
        events_id int,
        action text,
        issue_id int,
        push_id int,
        size int,
        distinct_size int,
        comment int,
        ref text,
        ref_type text,
        master_branch text,
        pusher_type text,
        CONSTRAINT fk_events FOREIGN KEY(events_id) REFERENCES events(id),
        CONSTRAINT fk_issue FOREIGN KEY(issue_id) REFERENCES issue(id)
    )
"""

create_table_queries = [
    table_create_actors,
    table_create_repo,
    table_create_org,
    table_create_creator,
    table_create_account,
    table_create_issue,
    table_create_reaction,
    table_create_comment,
    table_create_milestone,
    table_create_labels,
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
    table_drop_labels,
    table_drop_payload,
    table_drop_account,
    table_drop_issue,
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
