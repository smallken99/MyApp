from sqlalchemy import create_engine

# 建立資料庫連線字串，格式為 "mysql+pymysql://<username>:<password>@<host>/<database_name>"
db_url = "mysql+pymysql://root:ydhqm@smallken.com/testdb"

# 建立資料庫連線引擎
engine = create_engine(db_url, echo=True)

# 建立資料庫連線
conn = engine.connect()

# 執行 SQL 查詢
result = conn.execute("SELECT * FROM test_table")

# 讀取查詢結果
for row in result:
    print(row)

# 關閉連線
conn.close()