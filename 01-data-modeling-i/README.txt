ความตั้งใจแรกอยากจะสร้าง table ประมาณนี้เพื่อแสดงความสัมพันธ์ของข้อมูล

create_table_queries =
    table_create_actors,
    table_create_repo,
    table_create_users,
    table_create_author,
    table_create_release,
    table_create_events,
    table_create_payload

แต่พอมาทำในส่วนของ insert data ไม่สามารถ insert เข้าไปใน table ได้ สามารถใส่ได้แค่ table actor repo events ไม่เข้าใจเหมือนกันว่าโค้ดผิดตรงไหนค่ะ
เนื่องจากไม่สันทัดการเขียน python ก็เลยปรับลด table กับ column ไปเรื่อยๆ เอาเท่าที่จะสามารถ insert ข้อมูลเข้าไปได้