# 05-data-pipeline
## folder นี้ประกอบด้วย
1. dags มี folder data , file my_first_dag.py, hello.py, etl.py
2. logs
3. docker-compose.yml
4. README.md

## ขั้นตอนการทำงาน

1. เปิด terminal run

```sh
docker-compose up
```
2. เปิด port 8080 จะเข้าไปที่หน้า airflow ซึ่งจะให้ใส่ username password
3. จากไฟล์ docker-compose.yaml จะมีตรง _AIRFLOW_WWW_USER_USERNAME และ _AIRFLOW_WWW_USER_PASSWORD บอก username และ password  
4. จะสามารถเข้าไปดูหน้า UI ได้ว่า เมื่อเราสร้างไฟล์โค้ดการทำงานในโฟลเดอร์ dags ใน github ในหน้า UI ของ airflow ก็จะเป็นไปตามโค้ดที่เขียนไว้