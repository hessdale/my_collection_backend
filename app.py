import dbcreds
import dbhelper
import uuid
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

app.post("/api/admin")
def post_discogs():
    try:
        # Use request.files to make sure the uploaded_image is there
        # Again you can call it whatever you would like
        is_valid = dbhelper.check_endpoint_info(request.files, ['uploaded_csv'])
        if(is_valid != None):
            return make_response(jsonify(is_valid),400)
        # Save the image using the helper found in apihelpers
        file_name = dbhelper.save_file(request.files['uploaded_csv'])
        # If the filename is None something has gone wrong
        header_check = dbhelper.check_endpoint_info(request.headers,["token"])
        if(header_check != None):
            return make_response(jsonify(header_check), 400)
        if(file_name == None):
            return make_response(jsonify("Sorry, something has gone wrong"), 500)
        results = dbhelper.run_procedure("call post_image(?,?,?,?)",[request.headers.get("token"),request.files.get['uploaded_csv']])
        if(type(results) == list):
            return make_response(jsonify(results),200)
        else:
            return make_response("sorry something went wrong",500)
    # some except blocks with possible errors
    except TypeError:
        print("invalid input type, try again.")
    except UnboundLocalError:
        print("coding error")
    except ValueError:
        print("value error, try again")


app.get("/api/library")
def get_library():
    try:
        results = dbhelper.run_procedure("call get_library()",[])
        if(type(results) == list):
            return make_response(jsonify(results),200)
        else:
            return make_response("sorry something went wrong",500)
    except TypeError:
        print("invalid input type, try again.")
    except UnboundLocalError:
        print("coding error")
    except ValueError:
        print("value error, try again")





if(dbcreds.production_mode == True):
    print("Running Production Mode")
    import bjoern #type: ignore
    bjoern.run(app,"0.0.0.0",5000)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)
