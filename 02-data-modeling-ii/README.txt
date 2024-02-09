ใน Folder นี้ประกอบด้วย 3 files
1. docker-compose.yml
2. etl.py
3. README.txt

ขั้นตอน
1. run docker-compose up ใน terminal
2. ดูที่ ports 9042 เลือก open in browser
3. กด New terminal
4. run pip install cassandra-driver
5. run python etl.py
มี 1 table ชื่อ events
        id text,
        type text,
        actor_id int,
        repo_id int,
        payload text,
        public boolean,
        created_at text,
        org int,
        PRIMARY KEY (
            id,
            type