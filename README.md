# FastAPI Server for EasyOCR

This repository provides a FastAPI-based server to run OCR (Optical Character Recognition) tasks using the [EasyOCR](https://github.com/JaidedAI/EasyOCR) library.

## Features

- Perform OCR on uploaded images.
- Supports multiple languages via a comma-separated list of language codes (e.g., `en`, `ko`, `fr`).
- Outputs detected text with bounding boxes and confidence scores.

## How It Works

1. Upload an image file through the `/ocr` endpoint.
2. Specify the languages for text detection as a comma-separated list.
3. Get a structured JSON response with text annotations, including bounding boxes, detected text, and confidence levels.

## Example Response

```json
{
    "text_annotations": [
        {
            "boxes": [
                {
                    "x": 35,
                    "y": 27
                },
                {
                    "x": 241,
                    "y": 27
                },
                {
                    "x": 241,
                    "y": 95
                },
                {
                    "x": 35,
                    "y": 95
                }
            ],
            "text": "giangleons",
            "confidence": 0.022250899770254733
        },
        {
            "boxes": [
                {
                    "x": 225,
                    "y": 543
                },
                {
                    "x": 437,
                    "y": 543
                },
                {
                    "x": 437,
                    "y": 583
                },
                {
                    "x": 225,
                    "y": 583
                }
            ],
            "text": "도메와 함께하는",
            "confidence": 0.10227684988940935
        },
        {
            "boxes": [
                {
                    "x": 251,
                    "y": 575
                },
                {
                    "x": 1061,
                    "y": 575
                },
                {
                    "x": 1061,
                    "y": 665
                },
                {
                    "x": 251,
                    "y": 665
                }
            ],
            "text": "I리쇠레로 화보 촬영현장",
            "confidence": 0.08273127717998732
        }
    ]
}
```

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/ZhnYng/easyocr-server.git
   cd easyocr-server
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:
   ```bash
   fastapi run
   ```

4. Access the API at [http://127.0.0.1:8000](http://127.0.0.1:8000).
5. API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

- **`POST /ocr`**: Perform OCR on an uploaded image.
  - **Parameters**:
    - `image`: Image file (required).
    - `languages`: Comma-separated list of language codes (required).
  - **Response**: JSON with detected text and bounding boxes.
