def FetchAllAssoc(cursor, sql):
    try:
        result = []
        cursor.execute(sql)
        cols   = tuple([field[0].decode('utf8') for field in cursor.description])
        for row in cursor.fetchall():
            result.append(dict(zip(cols,row)))
    except Exception as e:
        result = {"error": str(e)}
    return result
