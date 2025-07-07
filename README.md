# README

## Overview

This project provides a FastAPI application for the automated creation and modification of CVs (Curriculum Vitae) using audio transcription and natural language processing. The application offers endpoints to generate CVs from audio input, text input, and allows editing existing CVs.

## Features

- **Audio Transcription**: Transcribes audio files and generates a CV based on the transcription.
- **Textual CV Creation**: Generates a CV from provided textual information.
- **Editable Templates**: Allows modification of existing CV templates.
- **Styled CV Template**: Outputs CVs as well-styled HTML using predefined templates.

## Setup Instructions

### Requirements

- Python 3.7+
- pip package manager
- FastAPI
- `speech_recognition` library
- `google.generativeai` library
- `uvicorn` for running the app

### Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn speechrecognition google-generativeai
   ```

3. **Configuration**:
   - Ensure the presence of a `config.json` file for `google.generativeai` API configuration:
     ```json
     {
       "api_key": "your_api_key_here"
     }
     ```

### Running the Server

To start the FastAPI server, use the command:

```bash
uvicorn main:app --reload
```

**Note**: The server will start at `http://localhost:8000`.

## API Endpoints

### 1. `POST /transcribe-and-create-cv/`

- **Description**: Transcribes an audio file and generates a CV based on the transcription.
- **Parameters**:
  - `file`: An audio file to be transcribed (using `multipart/form-data`).
- **Returns**: JSON with the generated CV.

### 2. `POST /create-cv-from-string/`

- **Description**: Creates a CV from provided text input.
- **Parameters**:
  - `info`: String containing the information to be included in the CV.
- **Returns**: JSON with the generated CV.

### 3. `POST /edit-cv/`

- **Description**: Edits an existing CV based on given modifications.
- **Parameters**:
  - `cv_file`: An HTML file of the existing CV (using `multipart/form-data`).
  - `modifications`: Description of the modifications to apply.
- **Returns**: JSON with the modified CV.

## Styles and Templates

The application utilizes a detailed HTML template styled with custom CSS for generating user-friendly CVs. The layout is split into a sidebar for personal information and main content for professional details.

## CORS Configuration

The application has a CORS middleware setup allowing requests from `http://localhost:8000`. Adjust this in the code as necessary to meet your specific domain requirements.

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```


## License

[MIT License](LICENSE.txt)
