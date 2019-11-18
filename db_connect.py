import psycopg2
from config import config
import datetime
# import crawl 


def connect():
    conn = None
    try:
        # read connection parameters
        params = config()
        conn = psycopg2.connect(**params) # 무슨 문법 ?
        # create a cursor
        cur = conn.cursor()

        stmt = 'select title from event_event' # 모든 title 가져오기
        cur.execute(stmt)
        result = cur.fetchall()
        # print(type(result[0])) # tuple
        
        title = ('[강화학습 핸즈온] 딥리워드 101 : 11월',)
        if title in result:
            print('exist')
        else:
            print('not exist')

        # execute a statement
        # cur.execute('SELECT version();')
        # cols = 'id'
        # table = 'event_event'
        # stmt = f'select {cols} from {table} order by id'
        # cur.execute(stmt)

        # db_result = cur.fetchall() # 이것도 함수 종류 알아야겠다..
        # for r in db_result:
        #     print(r)
        # print(type(db_result))

        # # insert
        # title, host, content, date_list, location = crawl.crawling()
        # stmt = "INSERT INTO event_event (id,title,host,content,image,category_id,created_at,updated_at,start_at,end_at,external_link,location) VALUES ("
        # stmt += f"26,'시현 더미','시현','시현','',2, '{datetime.datetime.now()}','{datetime.datetime.now()}', '{datetime.datetime.now()}','{datetime.datetime.now()}' ,'https://festa.io/events/666','시현')"
        # cur.execute(stmt)
        # # 결과 확인 -- ok
        # stmt = 'select id from event_event where id in (select max(id) from event_event)'
        # cur.execute(stmt)
        # db_result = cur.fetch()
        # print(type(db_result))



        # close communication postgresql. not connection
        
        # conn.commit() # commit 해야 변화되나 ?

        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()
            print('database connection closed')


if __name__ == '__main__':
    connect()