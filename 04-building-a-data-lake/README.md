# 04-Building a Data Lake
## folder นี้ประกอบด้วย 15 file

1. .ipynb_checkpoints
2. actors
3. data
4. events
5. img
6. output_csv
7. output_parquet
8. repos
9. workshop
10. .gitignore
11. docker-compose.yml
12. etl_local_with_s3.ipynb
13. etl_local.ipynb
14. etl.ipynb
15. README.md

## ขั้นตอนการทำงาน

1. เปิด terminal run

```sh
docker-compose up
```
2. เปิด port 8888 จะเข้าไปที่หน้า jupyterlab 
3. copy token ใน terminal ไปใส่ใน Key
4. จะเข้าสู่หน้า jupyterlab มี folder work ที่ประกอบด้วยไฟล์
    1. actors
    2. data
    3. events
    4. img
    5. output_csv
    6. output_parquet
    7. repos
    8. workshop
    9. docker-compose.yml
    10. etl_local_with_s3.ipynb
    11. etl_local.ipynb
    12. etl.ipynb
    13. README.md
   

   โดยข้อมูลจาก folder data file github_events_01.json และ github_events_02.json จะถูกดึงไปอยู่ในรูปแบบตารางที่ folder 
```sh
   actors ได้ file ประกอบด้วยข้อมูล
    actor.login
    id as event_id
    actor.url as actor_url
```
```sh  
   events ได้ folder: date=2022-08-17 และ file ประกอบด้วยข้อมูล
    id
    type
    created_at
    day(created_at) as day
    month(created_at) as month
    year(created_at) as year
    date(created_at) as date
```
```sh 
   repos ได้ file ประกอบด้วยข้อมูล
    repo.name
    id as event_id
    repo.url as repo_url
```
```sh   
   output_csv และ output_parquet folder: year=2022 ได้ file ประกอบด้วยข้อมูล
    id
    type
    created_at
    to_date(created_at) as date
    year(created_at) as year
    actor.login
    actor.url as actor_url
    repo.name
    repo.url as repo_url
```