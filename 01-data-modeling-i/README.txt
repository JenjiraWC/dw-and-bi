ใน Folder 01-data-modeling-i ประกอบด้วย file
1. create_tables.py
2. docker-compose.yml
3. etl.py
4. README.txt

ขั้นตอนการใช้งาน
1. run docker-compose up ใน Terminal 
2. ดูที่ Ports ที่ Ports 8080 เลือก Open in browser
3. System : PostgreSQL
   Server : postgres	
   db     : postgres
   Username : postgres	
   Password : postgres	
   Database : postgres
4. เลือก new Terminal แล้ว run python create_tables.py
5. refresh adminar จะได้ table
    actors
        id bigint,
        login text,
        PRIMARY KEY(id)

    repo
        id bigint,
        name text,
        PRIMARY KEY(id)

    users
        id bigint,
        login text,
        url text,
        type text,
        site_admin text,
        PRIMARY KEY(id)

    author
        id bigint,
        login text,
        type text,
        PRIMARY KEY(id)

    release
        id bigint,
        url text,
        author_id bigint,
        name text,
        created_at text,
        published_at text,
        PRIMARY KEY(id),
        CONSTRAINT fk_author_release FOREIGN KEY(author_id) REFERENCES author(id)
    
    events
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

6. แล้ว run python etl.py เพื่อ insert ข้อมูล json จาก folder data เข้าไปใน table 