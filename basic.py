import base64
import os
from google import genai
from google.genai import types

PARENT_FOLDER = "data"
FOLDER_NAME = "bio"
full_path = os.path.join(PARENT_FOLDER, FOLDER_NAME)

def generate():
    client = genai.Client(
        api_key="AIzaSyAqXw5g35k2EBLWOWxNkfyoicdPik69QsI"
    )

    files = [client.files.upload(file=os.path.join(full_path, f)) for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]
    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=files[0].uri,
                    mime_type=files[0].mime_type,
                ),
                types.Part.from_uri(
                    file_uri=files[1].uri,
                    mime_type=files[1].mime_type,
                ),
            ],
        ),
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""สรุปความเหมือนและแตกต่างของสองไฟล์นี้"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()