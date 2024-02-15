import requests
from io import BytesIO

def displayFile(file_id):
    file_id = "file-dmE0kKefCFMMK7Z9VgfCUwom"
    headers = {
    "Authorization": f"Bearer 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"
    }
    response = requests.get(f"https://api.openai.com/v1/files/{file_id}/content 12", headers=headers)
    img = Image.open(BytesIO(response.content))
    image.show()