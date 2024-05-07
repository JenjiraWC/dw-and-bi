# capstone project rainfall

## folder นี้ประกอบด้วย
1. dags >> ETL_Postgres_to_Bigquery.py : code การทำงานใน airflow
2. docker-compose.yml
3. load.ipynb : code นำข้อมูลจากไฟล์ csv เข้า neoo Postgres
4. requirements.txt
5. agriculture_cond_sql.sql : code SQL insert ข้อมูลเงื่อนไขปริมาณน้ำฝนที่เหมาะสมกับการปลูกพืชเศรษฐกิจเข้าใน Bigquery
6. README.md

## ขั้นตอนการทำงาน

### Neon
project นี้จะนำ raw data ไปเก็บไว้ที่ database postgres ของ [Neon — Serverless, Fault-Tolerant, Branchable Postgres](https://neon.tech/) ซึ่งเป็น serverless ที่สามารถทดลองใช้งานฟรีได้โดยขนาดของข้อมูลไม่เกิน 512 MiB storage, Limited to 0.25 vCPU, 1GB RAM

1. สร้าง new project
![alt text](<Screenshot 2024-05-06 165009.png>)

2. สร้าง new database
![alt text](<Screenshot 2024-05-06 170344.png>)

3. copy url ของ Postgres
![alt text](<Screenshot 2024-05-06 172344.png>)

### Google colab
1. download file load.ipynb ใช้งานผ่าน Google colab ที่เป็นบริการ Software as a Service (Saas) โฮสต์โปรแกรม Jupyter Notebook บน Cloud จาก Google ถ้ามี account gmail ก็สามารถใช้งานได้ฟรี

2. นำ url ที่ copy มาจาก neon ไปแทนที่ตรง connection_string เพื่อ connect กับ database ใน neon
![alt text](<Screenshot 2024-05-06 170120.png>)

3. run code เพื่อ create table
![alt text](<Screenshot 2024-05-06 170957.png>)

4. download file rainfall.csv upload ใส่ google colab แล้ว run code ต่อเพื่อ read file ,ทำความสะอาดข้อมูล และนำข้อมูลเข้าไปเก็บใน database posstgres neon 
![alt text](<Screenshot 2024-05-06 171137.png>)

5. โดยข้อมูลจาก file rainfall.csv ที่นำไปเก็บใน database มีรายละเอียดดังนี้
![alt text](<Screenshot 2024-05-06 211232.png>)

6. ตรวจสอบว่าข้อมูลอยู่ใน database เรียบร้อย
![alt text](<Screenshot 2024-05-06 182801.png>)

### Google BigQuery
Google BigQuery เป็น Serverless Data Warehouse หนึ่งในบริการของ Google cloud platform ค่าบริการเป็นแบบ Pay-per-use แต่มีให้ทดลองใช้ฟรี สามารถวิเคราะห์และประมวลผลข้อมูลขนาดใหญ่ (ฺBig data) เพื่อหาผลลัพธ์ตามที่ต้องการได้อย่างมีประสิทธิภาพและรวดเร็ว โดยการใช้ SQL
1. สร้าง new project
2. สร้าง dataset เป็นเหมือนกล่องไว้เก็บ table
![alt text](<Screenshot 2024-05-06 184122.png>)

3. กด ⋮ ที่ dataset ที่สร้างไว้เลือก create table และระบุชื่อ table “agriculture_cond” และกด CREATE TABLE
![alt text](<Screenshot 2024-05-07 193003.png>)

4. เลือก agriculture_cond table แล้วกด EDIT SCHEMA และระบุข้อมูลดังนี้
![alt text](<Screenshot 2024-05-07 193439.png>)

5. กด ⋮ ที่ agriculture_cond เลือก Query จะมีหน้าต่าง Query ขึ้นมา ให้ copy จากไฟล์ agriculture_cond_sql.sql (อย่าลืมปรับแก้ชื่อ dataset) จากนั้นกด RUN จะได้ตารางเงื่อนไขปริมาณน้ำฝนที่เหมาะสมกับพืชเศรษฐกิจ
![alt text](<Screenshot 2024-05-07 193728.png>)

6. Create service account ที่ IAM & Admin เพื่อสร้าง Key และกำหนด role
![alt text](<Screenshot 2024-05-06 184426.png>)

7. เมื่อสร้างเสร็จ download file key ในรูปแบบ .json แล้ว upload ใน folder capstone project ใน github 
![alt text](<Screenshot 2024-05-06 185017.png>)


### Github
1. ปรับแก้ไฟล์ ETL_Postgres_to_Bigquery.py โดยสามารถ ctrl+F 'changes' ได้ว่าจุดไหนที่ต้องปรับแก้

- แก้ dbname, user, password, host เพื่อเชื่อมต่อกับฐานข้อมูล Neon Postgres
![alt text](<Screenshot 2024-05-06 185949.png>)
![alt text](<Screenshot 2024-05-06 190724.png>)

-  แก้ keyfile และ project_id
![alt text](<Screenshot 2024-05-06 191916.png>)
![alt text](<Screenshot 2024-05-06 192402-1.png>)

- แก้ dataset_id ให้ตรงกับชื่อ dataset ใน BigQuery ทุกจุดสามารถ ctrl+F 'changes dataset_id' ได้
![alt text](<Screenshot 2024-05-07 221853.png>)

2. เปิด terminal run

```sh
docker-compose up
```
3. เปิด port 8080 จะเข้าไปที่หน้า airflow ซึ่งจะให้ใส่ username password
4. จากไฟล์ docker-compose.yaml จะมีตรง _AIRFLOW_WWW_USER_USERNAME และ _AIRFLOW_WWW_USER_PASSWORD บอก username และ password  สามารถนำไปใช้ login airflow ได้

### Airflow
1. set connection neon และ Bigquery ที่ tab admin >> connection กด + 
- add connection neon
![alt text](<Screenshot 2024-05-07 222449.png>)
- add connection BigQuery
![alt text](<Screenshot 2024-05-07 222859.png>)

ถ้ากด save แล้วขึ้นว่า page can't be found ให้ลบ :8080 ออกแล้ว refresh
![alt text](<Screenshot 2024-05-07 200524.png>)
![alt text](<Screenshot 2024-05-07 200847.png>)

2. แก้ postgres_conn_id="neon" ได้มาจากการเพิ่ม connection neon ใน UI Airflow tab Admin >> connection
![alt text](<Screenshot 2024-05-07 212956.png>)

3. run ETL_Postgres_to_Bigquery ในหน้า UI Airflow
![alt text](<Screenshot 2024-05-07 223127.png>)

4. จะได้ไฟล์ rainfall.csv กับ province.csv เข้ามาอยู่ใน dags เพื่อที่จะเอาข้อมูลจากตรงนี้ไปเข้าใน BigQuery
![alt text](<Screenshot 2024-05-07 223439.png>)

3. ตรวจสอบข้อมูลที่ BigQuery จะมี table rainfall และ province เพิ่มขึ้นมา
![alt text](<Screenshot 2024-05-07 224739.png>)

### Power BI
ในการทำ Visualize ของ project นี้ใช้ Power BI เพราะมี tools ให้เลือกใช้หลากหลาย ยืดหยุ่นและปรับแต่งได้ตามต้องการ มีผู้ใช้งานอย่างกว้างขวางสามารถเรียนรู้ตามได้ง่าย และสามารถ connect ข้อมูลได้จากหลายช่องทาง
1. ดึงข้อมูลจาก BigQuery เข้ามาใน Power BI เพื่อดู Visualize dashboard 
![alt text](image-1.png)

2.