import psycopg2

conn = psycopg2.connect(database="meshdata", user="postgres", password="postgres", host="localhost", port="5432")

cur = conn.cursor()

# cur.execute('CREATE EXTENSION postgis')
# cur.execute('CREATE EXTENSION postgis_topology')
# cur.execute('CREATE EXTENSION fuzzystrmatch')
# 地理编码
# cur.execute('CREATE EXTENSION postgis_tiger_geocoder')
# 存储属性tags, key-value
# cur.execute('CREATE EXTENSION hstore')
    
cur.execute("CREATE SCHEMA BjMap")
cur.execute('GRANT ALL ON SCHEMA BjMap TO postgres')
cur.execute('GRANT ALL ON SCHEMA BjMap TO PUBLIC')

cur.execute('''CREATE TABLE BjMap.nodes
       (BDC           BIGINT NOT NULL PRIMARY KEY,
       BDB            BIGINT NOT NULL,
       BDI            BIGINT,
       ID             VARCHAR(20) NOT NULL,
       TYPE           VARCHAR(20),
       NAME           VARCHAR(10),
       CENTER         GEOMETRY,
       BOUNDER        GEOMETRY,
       BDBOUNDER      GEOMETRY,
       LEVELB         SMALLINT,
       BOUNDERI       GEOMETRY,
       LEVELI         SMALLINT);''')
cur.execute('''CREATE TABLE BjMap.attributes
       (BDC           BIGINT NOT NULL PRIMARY KEY,
       BDB            BIGINT NOT NULL,
       ID             VARCHAR(20),
       COLOR          VARCHAR(10),
       HEIGHT         DOUBLE PRECISION,
       MINHEIGHT      DOUBLE PRECISION,
       NAME           TEXT,
       AGE            INT,
       TIMEBUILD      DATE,
       MATERIAL       VARCHAR(15),
       ADDRESS        CHAR(50)
       );''')

print("Table created successfully")

conn.commit()
conn.close()
