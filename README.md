# PDF Color Detector

A simple FastAPI service that analyzes a PDF file and identifies which pages are colored and which are black & white.

## Setup
```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

## Usage

Send a POST request to `/detect` with a PDF file:

```bash
curl -X POST "http://localhost:8000/detect" \
  -F "file=@your_document.pdf"
```

## Response

```json
{
  "total_pages": 10,
  "colored_count": 3,
  "bw_count": 7,
  "colored_pages": [2, 5, 8],
  "bw_pages": [1, 3, 4, 6, 7, 9, 10]
}
```

