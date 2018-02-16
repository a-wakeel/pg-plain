# pg-plain
A plain wrapper around psycopg2

## Usage
### pg plain usage
```python
    from pg_plain.pg import Pg

    conn_str = {
        "Host": "localhost",
        "Port": 5432,
        "Database": "postgres",
        "User": "postgres",
        "Password": "postgres"
    }
    
    query = 'your query'
    params = ('your params',)

    pg = Pg()
    pg.connect(conn_str)
    pg.execute(query, params)
    pg.commit()
    pg.close()
```

### pg pool usage
```python
    from pg_plain.pg_pool import PgPool
    
    conn_str = {
        "Host": "localhost",
        "Port": 5432,
        "Database": "postgres",
        "User": "postgres",
        "Password": "postgres"
    }
    
    pool_limit = {
        "Min": 1,
        "Max": 50
    }
    
    query = 'your query'
    params = ('query params',)
    
    pg_pool = PgPool()
    pg_pool.create_pool(conn_str, pool_limit)
    conn, cursor = pg_pool.get_conn()
    query_res = pg_pool.execute_query(cursor, query, params)
    pg_pool.commit_changes(conn)
    pg_pool.put_conn(conn)
    pg_pool.close_pool()
    
```
