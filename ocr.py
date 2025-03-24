import streamlit as st
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def main():
    """Main Streamlit app function with sidebar layout."""
    st.set_page_config(layout="wide")  # Set to wide mode

    st.title("OCR with Gemini")

    with st.sidebar:
        st.subheader("1. Google API Config")
        google_api_key = st.text_input('Enter your Google API key:', type='password', value=GOOGLE_API_KEY)
        st.subheader("2. Upload PDF หรือ Image")
        uploaded_file = st.file_uploader("Upload file", type=["pdf", "png", "jpg", "jpeg"])

    if google_api_key and uploaded_file:
        with st.spinner("🤖 Generating response..."):
            """Load file."""
            file_path = os.path.join("ocr_files", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            client = genai.Client(api_key=google_api_key)
            
            files = [
                client.files.upload(file=file_path),
            ]
            model = "gemini-2.0-flash-001"
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_uri(
                            file_uri=files[0].uri,
                            mime_type=files[0].mime_type,
                        ),
                        types.Part.from_text(text="""{page}"""),
                    ]
                )
            ]
            generate_content_config = types.GenerateContentConfig(
                temperature=1.0,
                top_p=0.95,
                top_k=40,
                max_output_tokens=8192,
                response_mime_type="text/plain",
                system_instruction=[
                    """
                        1. อ่านตัวอักษรจากไฟล์ที่ส่งให้
                        2. หากเป็นไฟล์ PDF ให้แสดงเลขที่หน้า และข้อความที่อ่านได้โดยตรง ไม่ต้องลดทอนเนื้อหา อ่านได้อย่างไร แสดงอย่างนั้น
                        3. หากเป็นไฟล์รูปไม่ต้องสนใจเลขหน้า ให้แสดงข้อความเลย
                        
                        Context: {context}

                        Page: {page}

                        Extracted Text:"""
                ]
            )
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=generate_content_config
            )
            st.write(response.usage_metadata)
            extracted_text = response.text

            if extracted_text is not None:
                st.header("Download Text File")
                txt_file_name = "extracted_text.txt"
                txt_data = extracted_text.encode()
                
                st.subheader("Extracted Text:")
                st.text_area("Extracted Content", extracted_text, height=300)

                st.download_button(
                    label="Download as .txt",
                    data=txt_data,
                    file_name=txt_file_name,
                    mime="text/plain",
                    on_click="ignore",
                )
    else:
        st.info("📥 Please upload a file to proceed.")


if __name__ == "__main__":
    main()