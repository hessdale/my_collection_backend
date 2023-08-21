import mariadb
import dbcreds
from uuid import uuid4
import os
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
        
def save_file(file):
    # Check to see if first, the filename contains a . character. 
    # Then, split the filename around the . characters into an array
    # Then, see if the filename ends with any of the given extensions in the array
    # You can add or remove file types you want or do not want the user to store
    if('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ['csv']):
        # Create a new filename with a token so we don't get duplicate file names
        # End the filename with . and the original filename extension
        filename = uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()
        try:
            # Use built-in functions to save the file in the images folder
            # You can put any path you want, in my example I just need them in the images folder right here
            file.save(os.path.join('collections_csv', filename))
            # Return the filename so it can be stored in the DB
            return filename
        except Exception as error:
            # If something goes wrong, print out to the terminal and return nothing
            print("FILE SAVE ERROR: ", error)
    # If any conditional is not met or an error occurs, None is returned