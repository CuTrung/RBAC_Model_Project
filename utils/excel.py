import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi import UploadFile

def export_excel(data: list[dict], filename: str = "export.xlsx", sheet_name: str = "Sheet1"):
    df = pd.DataFrame(data)

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    output.seek(0)

    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )


async def import_excel(file: UploadFile) -> list[dict]:
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))
    return df.to_dict(orient="records")
