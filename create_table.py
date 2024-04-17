# coding=utf-8
import pymysql
from config import db_host, db_user, db_password, db_name

try:
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name, charset="utf8mb4",
                                 cursorclass=pymysql.cursors.DictCursor)
    print(connection)
except Exception as e:
    print(e)

cursor = connection.cursor()
set_sql = "SET NAMES utf8mb4"
set_sql2 = "SET FOREIGN_KEY_CHECKS = 0"
cursor.execute(set_sql)
cursor.execute(set_sql2)

sql_1="DROP TABLE IF EXISTS `demetic`"
cursor.execute(sql_1)

sql = """
CREATE TABLE `demetic`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键自增',
  `user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '',
  `wallet_address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '',
  `private_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '',
  `phrase` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '',
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '',
  `alerts` TINYINT(1) NULL DEFAULT '0' COMMENT '节点预警',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC"""

cursor.execute(sql)


sql_2="DROP TABLE IF EXISTS `user_info`"
cursor.execute(sql_2)

sql = """
CREATE TABLE `user_info`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键自增',
  `user_id2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '',
  `transaction_hash2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '',
  `username2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '',
  `email2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '',
  `order_info2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '',
  `sell_info2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC"""

cursor.execute(sql)


set_sql3 = "SET FOREIGN_KEY_CHECKS = 1;"
cursor.execute(set_sql3)

connection.commit()
cursor.close()
connection.close()
