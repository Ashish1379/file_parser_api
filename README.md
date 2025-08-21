# file_parser_api
File Parser CRUD API (Django + DRF)

A simple API to upload large files (CSV/XLSX), track upload/processing progress, parse with pandas, and fetch parsed content. Includes polling-based progress and an optional path for Server-Sent Events (SSE).

Features
Upload a file (form-data)
Store file metadata + binary (Django FileField)
Background processing (thread) with fake/streamed progress
Parse using pandas (CSV/XLSX) → store as JSON
CRUD: list files, get parsed content, delete file
Progress polling endpoint (returns 102 Processing until ready)
Optional SSE endpoint for real-time parsing progress


Tech Used
Django, Django REST Framework
SQLite (default) or any DB supported by Django
pandas, openpyxl for parsing




Setup Instructions
1) Clone & install
git clone https://github.com/Ashish1379/file_parser_api/tree/master
cd file
pip install django djangorestframework pandas openpyxl





2) Configure media & DRF (already in code, but check)
In settings.py:
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

3) Migrate
python manage.py makemigrations
python manage.py migrate

4) Run server
python manage.py runserver
Default base URL: http://127.0.0.1:8000/



API Documentation(using POSTMAN)
1) Upload File
POST /files/
Body: form-data with key file

Response
201 Created
received data: 
{
  "id": "94cf877d-ceaf-4d22-9192-dbe3049806f2",
  "filename": "your.csv",
  "file": "/media/uploads/your.csv",
  "status": "uploading",
  "progress": 0,
  "parsed_content": null,
  "created_at": "2025-08-21T19:05:13.002Z"
}

2) Get Upload/Processing Progress
GET /files/{file_id}/progress/
While processing: returns HTTP 102 Processing (Postman shows as 102).
When ready: returns HTTP 200 OK with progress: 100 and status: "ready".

Responses
102 Processing
{
  "file_id": "94cf877d-ceaf-4d22-9192-dbe3049806f2",
  "status": "processing",
  "progress": 59
}

OR
200 OK
{
  "file_id": "94cf877d-ceaf-4d22-9192-dbe3049806f2",
  "status": "ready",
  "progress": 100
}


3) Get Parsed Content
GET /files/{file_id}/
Responses:
(If still processing) 
{ "message": "File upload or processing in progress. Please try again later." }


(If ready) → 200 OK (with parsed JSON (list of rows as dicts) )
[
  {"col1": "value", "col2": 123},
  {"col1": "value2", "col2": 456}
]


4) List Files (minimal fields)
GET /files/
Responses:
200 OK 

[
  {
    "id": "05075e0e-ff22-498c-999f-5dee57236ec3",
    "filename": "data.csv",
    "status": "ready",
    "created_at": "2025-08-21T19:00:10.120Z"
  },
  {
    "id": "94cf877d-ceaf-4d22-9192-dbe3049806f2",
    "filename": "big.xlsx",
    "status": "processing",
    "created_at": "2025-08-21T19:05:13.002Z"
  }
]

5) Delete File
DELETE /files/{file_id}/
Response:
200 OK
{ "message": "File and its data deleted" }


On upload, a background thread starts (process_file)
It reads the file in 1MB chunks → updates progress (0…100) in DB
Once pandas parsing completes, it stores parsed_content (as JSON) and sets status="ready"
Polling: Client hits /files/{id}/progress/ every 1–2 seconds until progress reaches 100.
