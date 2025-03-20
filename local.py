import streamlit as st
import os
from google import genai
from google.genai import types

# --- กำหนดค่าเริ่มต้น ---
DEFAULT_PARENT_FOLDER = "data"  # เปลี่ยนเป็นโฟลเดอร์ที่คุณต้องการ
PARENT_FOLDER = DEFAULT_PARENT_FOLDER
parts = []
uploaded_files = []
finished = False

# --- ฟังก์ชันต่างๆ ---
def create_folder(folder_name, parent_folder):
    """สร้างโฟลเดอร์"""
    full_path = os.path.join(parent_folder, folder_name)
    try:
        os.makedirs(full_path, exist_ok=True)
        st.success(f"สร้างโฟลเดอร์ '{folder_name}' ใน '{parent_folder}' สำเร็จ")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการสร้างโฟลเดอร์: {e}")

def list_folders(parent_folder):
    """แสดงรายชื่อโฟลเดอร์ทั้งหมดในพาธที่กำหนด"""
    try:
        folders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))]
        return folders
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านรายชื่อโฟลเดอร์: {e}")
        return []

def upload_files(folder_name, uploaded_files, parent_folder):
    """อัปโหลดไฟล์หลายไฟล์ไปยังโฟลเดอร์ที่กำหนด"""
    full_path = os.path.join(parent_folder, folder_name)
    success_count = 0
    for uploaded_file in uploaded_files:
        try:
            file_path = os.path.join(full_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            success_count += 1
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการอัปโหลดไฟล์ '{uploaded_file.name}': {e}")

    if success_count > 0:
        st.success(f"อัปโหลด {success_count} ไฟล์ ไปยัง '{folder_name}' ใน '{parent_folder}' สำเร็จ")
    else:
        st.warning("ไม่มีไฟล์ใดถูกอัปโหลดสำเร็จ")

def list_files_in_folder(folder_name, parent_folder):
    """แสดงรายชื่อไฟล์ทั้งหมดในโฟลเดอร์ที่กำหนด"""
    full_path = os.path.join(parent_folder, folder_name)
    try:
        files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]
        return files
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านรายชื่อไฟล์: {e}")
        return []
    
def file_path_in_folder(folder_name, parent_folder):
    """แสดง File Path ทั้งหมดในโฟลเดอร์ที่กำหนด"""
    full_path = os.path.join(parent_folder, folder_name)
    try:
        files = [os.path.join(full_path, f) for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]
        return files
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านรายชื่อไฟล์: {e}")
        return []

def delete_file(folder_name, file_name, parent_folder):
    """ลบไฟล์"""
    full_path = os.path.join(parent_folder, folder_name)
    try:
        file_path = os.path.join(full_path, file_name)
        os.remove(file_path)
        st.success(f"ลบไฟล์ '{file_name}' จาก '{folder_name}' ใน '{parent_folder}' สำเร็จ")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการลบไฟล์: {e}")

# --- สร้าง parent folder ถ้ายังไม่มี ---
os.makedirs(PARENT_FOLDER, exist_ok=True)

def main():
    # --- เริ่มต้น Streamlit app ---
    st.title("GEMINI-2.0-Flash RAG Chatbot")

    with st.sidebar:
        st.title('1. เตรียมไฟล์')
        # 1. สร้างโฟลเดอร์
        st.subheader("1.1 สร้างโฟลเดอร์")
        new_folder_name = st.text_input("ชื่อโฟลเดอร์ใหม่:")
        if st.button("สร้าง"):
            if new_folder_name:
                create_folder(new_folder_name, PARENT_FOLDER)
            else:
                st.warning("กรุณาใส่ชื่อโฟลเดอร์")

        # 2. อัปโหลดไฟล์ไปยังโฟลเดอร์ที่เลือก
        st.subheader("1.2 อัปโหลดไฟล์")

        # ดึงรายชื่อโฟลเดอร์
        folder_options = list_folders(PARENT_FOLDER)

        if folder_options:
            selected_folder = st.selectbox("เลือกโฟลเดอร์:", folder_options)
            uploaded_files = st.file_uploader("เลือกไฟล์:", accept_multiple_files=True)  # Allow multiple file uploads

            if uploaded_files:
                upload_files(selected_folder, uploaded_files, PARENT_FOLDER) # Call the multiple file upload function
        else:
            st.warning("ยังไม่มีโฟลเดอร์ กรุณาสร้างโฟลเดอร์ก่อน")

        # 3. แสดงรายชื่อไฟล์ในโฟลเดอร์ที่เลือก และปุ่มลบ
        st.subheader("1.3 รายชื่อไฟล์")

        # ดึงรายชื่อโฟลเดอร์อีกครั้ง (เพื่อให้แน่ใจว่าข้อมูลอัพเดท)
        folder_options = list_folders(PARENT_FOLDER)

        if folder_options:
            selected_folder_for_list = st.selectbox("เลือกโฟลเดอร์เพื่อแสดงไฟล์:", folder_options, key="folder_list")  # เพิ่ม key เพื่อให้ Streamlit ไม่สับสนกับ dropdown ก่อนหน้า
            files = list_files_in_folder(selected_folder_for_list, PARENT_FOLDER)

            if files:
                st.write("ไฟล์ในโฟลเดอร์:")
                for file_path in files:
                    col1, col2 = st.columns([0.7, 0.3])
                    with col1:
                        st.write(f"- {file_path}")
                    with col2:
                        if st.button(f"x", key=f"delete_{file_path}"):  # Unique key for each button
                            delete_file(selected_folder_for_list, file_path, PARENT_FOLDER)
                            # Refresh file list after deletion
                            file_list = list_files_in_folder(selected_folder_for_list, PARENT_FOLDER)
            else:
                st.info("ไม่มีไฟล์ในโฟลเดอร์นี้")

        else:
            st.warning("ยังไม่มีโฟลเดอร์ กรุณาสร้างโฟลเดอร์ก่อน")

        # 5. สร้างช่องบันทึก Google API Key
        st.title('2. Google AI Config')
        google_api_key = st.text_input('Enter your Google API key:', type='password')
        selected_api_folder = st.selectbox("เลือกโฟลเดอร์สำหรับวิเคราะห์:", folder_options)
        client = genai.Client(api_key=google_api_key)
        if st.button('Start Analysis'):
            km_files = file_path_in_folder(selected_api_folder, PARENT_FOLDER)
            with st.spinner("🔄 กำลังอัพโหลด..."):
                for file_path in km_files:
                    st.write(f"อัปโหลดไฟล์: {file_path}")
                    uploaded_files.append(client.files.upload(file=file_path))
                    parts.append(types.Part.from_uri(file_uri=uploaded_files[-1].uri, mime_type=uploaded_files[-1].mime_type))
                    #st.write(f"URI: {uploaded_files[-1].uri}, MIME Type: {uploaded_files[-1].mime_type}")
                finished = True

    if google_api_key:
        if selected_api_folder:
            q = st.text_input("ถามคำถามได้เลยครับ:")
            if q:
                st.write(f"ค้นข้อมูลจาก {len(uploaded_files)} ไฟล์")
                st.write(f"ค้นข้อมูลจาก {len(parts)} ไฟล์")
                with st.spinner("🤖 กำลังประมวลผล..."):
                    parts.append(types.Part.from_text(text=f"""{q}"""))
                    model = "gemini-2.0-flash"
                    contents = [
                        types.Content(
                            role="user",
                            parts=parts
                        )
                    ]
                    generate_content_config = types.GenerateContentConfig(
                        temperature=1.0,
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
                        st.write(chunk.text, end="")
        else:
            st.warning("ยังไม่ทำการเลือกโฟลเดอร์")
    else:
        st.warning("ยังไม่ทำการกรอก Google API Key")
if __name__ == "__main__":
    main()