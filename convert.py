import csv
import sqlite3
import json
import os

class Convert:
    def __init__(self):
        csv_file_name = self.csv_to_json('test.csv')
        #print(csv_file_name)
        self.csv_to_sqlite(csv_file_name, 'test.db')

    # 将CSV文件导入到数据库
    def csv_to_sqlite(self, csv_file, db_file):
        # 连接到SQLite数据库
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # 读取CSV文件
        with open(csv_file, 'r') as file:
            csv_data = csv.reader(file)
            headers = next(csv_data)  # 获取表头

            # 创建表格
            table_name = (csv_file.split('.')[0]).replace('_converted','')  # 使用CSV文件名作为表名
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join(headers)})"
            cursor.execute(create_table_query)

            # 插入或更新数据
            for row in csv_data:
                company_value = row[headers.index('company')]
                select_query = f"SELECT * FROM {table_name} WHERE company = ?"
                cursor.execute(select_query, (company_value,))
                existing_data = cursor.fetchone()

                if existing_data:
                    update_query = f"UPDATE {table_name} SET {', '.join([f'{header} = ?' for header in headers])} WHERE company = ?"
                    cursor.execute(update_query, (*row, company_value))
                else:
                    insert_query = f"INSERT INTO {table_name} ({', '.join([f'{header} ' for header in headers])}) VALUES ({', '.join(['?' for _ in headers])})"
                    print(f' ')
                    cursor.execute(insert_query, row)

        # 提交更改并关闭连接
        conn.commit()
        conn.close()


    def csv_to_json(self, input_file):
        # 读取CSV文件
        with open(input_file, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        # 创建新的表格数据
        new_data = [['company', 'email_info', 'contacts']]

        # 遍历数据并进行合并
        for i in range(1, len(data)):
            row = data[i]
            merged_row = [row[0], row[1]]
            contacts = {}

            # 遍历每个联系人的信息
            for j in range(2, len(row)-2, 3):
                name = row[j]
                position = row[j+1]
                email = row[j+2]

                # 如果名字不为空，则将联系人信息添加到字典中
                if name:
                    contacts[name] = {'position': position, 'email': email}
            if not str(contacts) == '{}':
                # 将联系人字典转换为JSON字符串并添加到新的表格数据中
                merged_row.append(json.dumps(contacts))
                new_data.append(merged_row)
            else:
                contacts = ""
                merged_row.append(contacts)
                new_data.append(merged_row)                

        # 获取输入文件的文件名和扩展名
        file_name, file_ext = os.path.splitext(input_file)

        # 拼接新文件名
        output_file = file_name + '_converted' + file_ext

        # 保存合并后的表格数据到新文件
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(new_data)
        
        return output_file

main = Convert()