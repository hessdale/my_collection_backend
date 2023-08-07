import mariadb
import dbcreds
def convert_data(cursor,results):
    column_names = [i[0] for i in cursor.description]
    new_results = []
    for row in results:
        new_results.append(dict(zip(column_names,row)))
    return new_results

def run_procedure(sql,args):
    try:
        results = None
        conn = mariadb.connect(**dbcreds.conn_params)
        cursor = conn.cursor()
        cursor.execute(sql,args)
        results = cursor.fetchall()
        results = convert_data(cursor,results)
    except mariadb.ProgrammingError as error:
        print('there is an issue with the db code: ',error)
    except mariadb.OperationalError:
        print('there is an issue with connection to the DB',error)
    except Exception as error:
        print('there was an unknown error',error)
    finally:
        if(cursor!=None):
            cursor.close()
        if(conn != None):
            conn.close()
        return results
        
def check_endpoint_info(sent_data,expected_data):
    for data in expected_data:
        if(sent_data.get(data) == None):
            return f'The {data} paramater is required'
        
