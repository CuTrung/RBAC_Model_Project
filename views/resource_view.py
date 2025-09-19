from fastapi.responses import JSONResponse

def success_response(data, message="Success"):
    return JSONResponse(content={"message": message, "data": data}, status_code=200)

def error_response(message="Error", status_code=400):
    return JSONResponse(content={"message": message}, status_code=status_code)
