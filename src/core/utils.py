from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.response import Response 

def custom_exception_handler(exec, context):
    try : 
        response = exception_handler(exec, context)
        if isinstance(exec, PermissionDenied):
            print("Permission Denied Error !!! ")
            temp= {}
            temp['status'] = 403
            temp['message'] = "Forbidden"
            #temp['data'] = ""
            if response is not None : 
                response.data = temp
            return response
        print("exec")


        if exec.args[0]['messages'][0]['message'] == "Token is invalid or expired": 

            temp= {}
            temp['status'] = 401
            temp['message'] = "Unauthorized"
            #temp['data'] = ""
            if response is not None : 
                response.data = temp
            return response
        else : 
            response 

    except Exception as e : 
        print(e.args[0])
        if e.args[0] == 'tuple index out of range':
            temp= {}
            temp['status'] = 401
            temp['message'] = "Unauthorized"
            #temp['data'] = ""
            response.data = temp
        print("Failed while handling the exception : ", e)
        return response
  
