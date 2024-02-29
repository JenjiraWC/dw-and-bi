# 03-Building a Data Warehouse-2
## folder นี้ประกอบด้วย 5 file

1. events_json_path.json
2. etl.py
3. github_events_01.json
4. README.md
5. requirements.txt

## ขั้นตอนการทำงาน

## AWS

1. Create Bucket ใน S3
2. นำ file events_json_path.json และ github_events_01.json upload ลง Bucket

## github

1. เปิด terminal run
```sh
python -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt

เพื่อ install และ activate requirements.txt
```


2. ตรวจสอบ file etl.py ว่า path และ region ตรงกับ path และ region ใน AWS
```sh
    COPY staging_events FROM 's3://jenjira-swu-labs/github_events_01.json'
    CREDENTIALS 'aws_iam_role=arn:aws:iam::851725509891:role/LabRole'
    JSON 's3://jenjira-swu-labs/events_json_path.json'
    REGION 'us-east-1'
```

3. run file etl.py 
```sh
python etl.py 
```