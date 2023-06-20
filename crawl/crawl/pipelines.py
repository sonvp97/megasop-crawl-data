import mysql.connector


class MySQLPipeline:
    def __init__(self, mysql_host, mysql_port, mysql_user, mysql_password, mysql_database):
        self.connection = None
        self.mysql_host = mysql_host
        self.mysql_port = mysql_port
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.mysql_database = mysql_database

    @classmethod
    def from_crawler(cls, crawler):
        mysql_host = crawler.settings.get('MYSQL_HOST')
        mysql_port = crawler.settings.get('MYSQL_PORT')
        mysql_user = crawler.settings.get('MYSQL_USER')
        mysql_password = crawler.settings.get('MYSQL_PASSWORD')
        mysql_database = crawler.settings.get('MYSQL_DATABASE')

        return cls(mysql_host, mysql_port, mysql_user, mysql_password, mysql_database)

    def open_spider(self, spider):
        self.connection = mysql.connector.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password,
            database=self.mysql_database
        )

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        cursor = self.connection.cursor()

        if item['table_name'] == 'guardian':
            query = "INSERT INTO guardian (name, price, status) VALUES (%s, %s, %s)"
            values = (item['name'], item['price'], item['status'])
        elif item['table_name'] == 'hasaki':
            query = "INSERT INTO hasaki (name, price, total, status) VALUES (%s, %s, %s, %s)"
            values = (item['name'], item['price'], item['total'], item['status'])
        elif (item['table_name'] == "pharmacity"):
            query = f"INSERT INTO {item['table_name']} (name, price, brick_price, total) VALUES (%s, %s, %s, %s)"
            values = (item['name'], item['price'], item['brick_price'], item['total'])
        else:
            query = f"INSERT INTO {item['table_name']} (name, price, total) VALUES (%s, %s, %s)"
            values = (item['name'], item['price'], item['total'])

        cursor.execute(query, values)
        self.connection.commit()
        return item


    # def process_item(self, item, spider):
    #     cursor = self.connection.cursor()
    #     query = "INSERT INTO content (name,brand_name,price,quantity) VALUES (%s,%s,%s,%s)"
    #     values = (item.get("name"), item.get("brand_name"), item.get("price"), item.get("quantity"))
    #
    #     cursor.execute(query, values)
    #     self.connection.commit()
    #     cursor.close()
    #
    #     return item
