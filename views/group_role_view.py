from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder


def success_response(data, message="Thành công", status_code=status.HTTP_200_OK):
    return JSONResponse(content={"message": message, "data": jsonable_encoder(data)}, status_code=status_code)


def error_response(message="Lỗi", status_code=status.HTTP_400_BAD_REQUEST):
    return JSONResponse(content={"message": message, "data": None}, status_code=status_code)
