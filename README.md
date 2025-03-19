# Streamlit GCS App

This project is a Streamlit application that allows users to interact with Google Cloud Storage (GCS). Users can create and delete folders, upload and delete files, and view the list of files and folders in a specified GCS bucket.

## Project Structure

```
streamlit-gcs-app
├── src
│   ├── app.py          # Main entry point of the Streamlit application
│   ├── gcs_utils.py    # Utility functions for interacting with Google Cloud Storage
│   └── config.py       # Configuration settings and GCS client initialization
├── requirements.txt     # List of dependencies
└── README.md            # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd streamlit-gcs-app
   ```

2. **Create a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up Google Cloud Storage:**
   - Create a Google Cloud project and enable the Google Cloud Storage API.
   - Create a service account and download the JSON key file.
   - Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of the JSON key file.

5. **Configure the bucket name:**
   - Update the `src/config.py` file with your GCS bucket name.

## Usage

To run the Streamlit application, execute the following command:

```
streamlit run src/app.py
```

Once the application is running, you can:

- Create new folders in the specified GCS bucket.
- Delete existing folders.
- Upload files to the bucket.
- Delete files from the bucket.
- View a list of all files and folders in the bucket.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.