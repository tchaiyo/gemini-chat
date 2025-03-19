import streamlit as st
from google.cloud import storage
import os
import json

# ข้อมูลสำหรับเชื่อมต่อ Google Cloud Storage (แทนที่ด้วยค่าจริงของคุณ)
BUCKET_NAME = "km-files"  # ชื่อ Bucket ของคุณ
CREDENTIALS_JSON_PATH = "credentials-admin.json"  # Path ของไฟล์ credentials JSON
storage_client = storage.Client.from_service_account_json(CREDENTIALS_JSON_PATH)
bucket = storage_client.bucket(BUCKET_NAME)

def create_folder(folder_name):
    """สร้างโฟลเดอร์ใน GCS (จริงๆ คือสร้าง object ที่ลงท้ายด้วย /)"""
    try:
        blob = bucket.blob(folder_name + "/")
        blob.upload_from_string("", content_type="application/x-directory")
        st.success(f"สร้างโฟลเดอร์ '{folder_name}' สำเร็จ")
        return True  # Indicate success
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการสร้างโฟลเดอร์: {e}")
        return False  # Indicate failure

def upload_file(file, destination_folder):
    """อัปโหลดไฟล์ไปยัง GCS โดยระบุโฟลเดอร์ปลายทาง และใช้ชื่อไฟล์เดิม
       หากมีไฟล์ชื่อเดิมอยู่แล้ว จะทำการแทนที่"""
    try:
        file_name = file.name  # Use the original file name
        destination_path = os.path.join(destination_folder, file_name) if destination_folder else file_name
        blob = bucket.blob(destination_path)
        blob.upload_from_string(file.read(), content_type=file.type)
        st.success(f"อัปโหลด/แทนที่ไฟล์ '{file_name}' ไปที่ '{destination_path}' สำเร็จ")
        return True
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอัปโหลด/แทนที่ไฟล์: {e}")
        return False

def delete_file(file_path):
    """ลบไฟล์จาก GCS"""
    try:
        blob = bucket.blob(file_path)
        blob.delete()
        st.success(f"ลบไฟล์ '{file_path}' สำเร็จ")
        return True
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการลบไฟล์: {e}")
        return False

def list_files_in_folder(folder_name=""):
    """แสดงรายการไฟล์ใน GCS folder (prefix) ที่ระบุ"""
    try:
        blobs = list(bucket.list_blobs(prefix=folder_name))
        file_list = []
        for blob in blobs:
            if not blob.name.endswith("/"):  # Skip folders
                file_list.append(blob.name)
        return file_list
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการแสดงรายการไฟล์: {e}")
        return []

def list_folders():
    """แสดงรายการโฟลเดอร์ใน GCS Bucket"""
    try:
        blobs = list(bucket.list_blobs())
        folder_list = []
        for blob in blobs:
            if blob.name.endswith("/"):  # Identify folders
                folder_list.append(blob.name[:-1])  # Remove trailing slash
        return folder_list
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการแสดงรายการโฟลเดอร์: {e}")
        return []

def main():
    st.title("Google Cloud Storage Manager")

    # Initialize session state for folder list
    if "folder_list" not in st.session_state:
        st.session_state.folder_list = list_folders()

    def refresh_folder_list():
        st.session_state.folder_list = list_folders()

    # สร้างโฟลเดอร์
    st.subheader("สร้างโฟลเดอร์")
    col1, col2 = st.columns([2, 1])
    with col1:
        folder_name = st.text_input("ชื่อโฟลเดอร์:")
    with col2:
        if st.button("สร้างโฟลเดอร์"):
            if folder_name:
                if create_folder(folder_name):
                    refresh_folder_list()  # Refresh the folder list

    # อัปโหลดไฟล์ (หลายไฟล์)
    st.subheader("อัปโหลดไฟล์ (หลายไฟล์)")
    folder_options = [""] + st.session_state.folder_list
    destination_folder = st.selectbox("เลือกโฟลเดอร์ปลายทาง:", options=folder_options)  # use dropdown list
    uploaded_files = st.file_uploader("เลือกไฟล์", type=["txt", "csv", "pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)  # Allow multiple files

    if st.button("อัปโหลด"):
        if uploaded_files:
            for file in uploaded_files:
                upload_file(file, destination_folder)  # Upload each file
        else:
            st.warning("กรุณาเลือกไฟล์อย่างน้อยหนึ่งไฟล์")


    # แสดงและลบไฟล์
    st.subheader("แสดงและลบไฟล์ในโฟลเดอร์")
    display_folder = st.selectbox("เลือกโฟลเดอร์เพื่อแสดงไฟล์:", options=[""] + st.session_state.folder_list)
    file_list = list_files_in_folder(display_folder)

    if file_list:
        st.write("ไฟล์ในโฟลเดอร์:")
        for file_path in file_list:
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                st.write(f"- {file_path}")
            with col2:
                if st.button(f"ลบ", key=f"delete_{file_path}"):  # Unique key for each button
                    delete_file(file_path)
                    # Refresh file list after deletion
                    file_list = list_files_in_folder(display_folder)

    else:
        st.info("ไม่มีไฟล์ในโฟลเดอร์นี้")


if __name__ == "__main__":
    main()