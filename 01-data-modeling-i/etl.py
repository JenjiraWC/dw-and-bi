import glob
import json
import os
from typing import List

import psycopg2


def get_files(filepath: str) -> List[str]:
    """
    Description: This function is responsible for listing the files in a directory
    """

    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print(f"{num_files} files found in {filepath}")

    return all_files


def process(cur, conn, filepath):
    # Get list of files from filepath
    all_files = get_files(filepath)

    for datafile in all_files:
        with open(datafile, "r") as f:
            data = json.loads(f.read())
            for each in data:
                # Print some sample data
                if each["type"] == "IssueCommentEvent":
                    print(
                        each["id"],
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["org"]["id"],
                        each["org"]["login"],
                        each["payload"]["action"],
                        each["payload"]["issue"]["url"],
                        each["payload"]["comment"]["id"],
                        each["public"],
                        each["created_at"],
                    )

                elif each["type"] == "PushEvent":
                    print(
                        each["id"],
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["org"]["id"],
                        each["org"]["login"],
                        #each["payload"]["push_id"],
                        each["payload"]["commits"]["url"],
                        each["public"],
                        each["created_at"],
                    )
                elif each["type"] == "IssuesEvent":
                    print(
                        each["id"],
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["payload"]["action"],
                        each["payload"]["issue"]["id"],
                        each["payload"]["issue"]["url"],
                        each["public"],
                        each["created_at"],
                    )
                elif each["type"] == "ReleaseEvent":
                    print(
                        each["id"],
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["payload"]["action"],
                        #each["payload"]["release"]["id"],
                        each["public"],
                        each["created_at"],
                    )
                elif each["type"] == "DeleteEvent":
                    print(
                        each["id"],
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["payload"]["ref"],
                        each["payload"]["ref_type"],
                        each["payload"]["pusher_type"],
                        each["public"],
                        each["created_at"],
                        each["org"]["id"],
                        each["org"]["login"],
                    )
                elif each["type"] == "CreateEvent":
                    print(
                        each["id"],
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["payload"]["ref"],
                        each["payload"]["ref_type"],
                        each["payload"]["pusher_type"],
                        each["public"],
                        each["created_at"],
                    )
                else:
                    print(
                        each["id"],
                        each["type"],
                        each["actor"]["id"],
                        each["actor"]["login"],
                        each["repo"]["id"],
                        each["repo"]["name"],
                        each["org"]["id"],
                        each["org"]["login"],
                        each["payload"]["action"],
                        each["payload"]["issue"]["id"],
                        each["payload"]["issue"]["url"],
                        each["payload"]["comment"]["id"],
                        #each["payload"]["push_id"],
                        each["payload"]["ref"],
                        each["payload"]["ref_type"],
                        each["payload"]["pusher_type"],
                        each["payload"]["commits"]["url"],
                        #each["payload"]["release"]["id"],
                        each["public"],
                        each["created_at"],
                    )

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO actors (
                        id,
                        login
                    ) VALUES ('{each["actor"]["id"]}', '{each["actor"]["login"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                cur.execute(insert_statement)

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO repo (
                        id,
                        name
                    ) VALUES ('{each["repo"]["id"]}', '{each["repo"]["name"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                cur.execute(insert_statement)

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO org (
                        id,
                        login
                    ) VALUES ('{each["org"]["id"]}', '{each["org"]["login"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                cur.execute(insert_statement)

                insert_statement_issue = f"""
                    INSERT INTO issue (
                        id,	
                        url
                    ) VALUES ('{each["payload"]["issue"]["id"]}','{each["payload"]["issue"]["url"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                cur.execute(insert_statement)

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO payload (
                        action,
                        issue_id,
                        comment,
                        commit_url,
                        ref,
                        ref_type,
                        pusher_type
                    ) VALUES (
                        '{each["payload"]["action"]}',
                        '{each["payload"]["issue"]["id"]}',
                        '{each["payload"]["comment"]["id"]}',
                        '{each["payload"].get("commits", {}).get("url", "")}',
                        '{each["payload"].get("ref", "")}',
                        '{each["payload"].get("ref_type", "")}',
                        '{each["payload"].get("pusher_type", "")}'
                    )
                """
                cur.execute(insert_statement)

                # Insert data into tables here
                insert_statement = f"""
                    INSERT INTO events (
                        id,
                        type,
                        actor_id,
                        repo_id,
                        payload,
                        public,
                        created_at,
                        org_id
                    ) VALUES ('{each["id"]}', '{each["type"]}', '{each["actor"]["id"]}', '{each["repo"]["id"]}', '{each["payload"]["issue"]["url"]}', '{each["public"]}', '{each["created_at"]}', '{each["org"]["id"]}')
                    ON CONFLICT (id) DO NOTHING
                """
                cur.execute(insert_statement)

               

    conn.commit()

def main():
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=postgres user=postgres password=postgres"
    )
    cur = conn.cursor()

    process(cur, conn, filepath="../data")

    conn.close()


if __name__ == "__main__":
    main() 