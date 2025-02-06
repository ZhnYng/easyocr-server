from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
import easyocr
import uvicorn
import threading
from typing import Annotated
import json
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, AfterValidator, BeforeValidator, Field, AliasChoices
import re

app = FastAPI()

reader_cache = {}
cache_lock = threading.Lock()


def get_reader(languages: list[str]) -> easyocr.Reader:
    key = ",".join(sorted(languages))
    with cache_lock:
        if key in reader_cache:
            print(f"[INFO]: Using cached ocr reader for languages: {key}")
            return reader_cache[key]

        reader = easyocr.Reader(languages)
        reader_cache[key] = reader
        print(f"[INFO]: Cached new reader for languages: {key}")
        return reader


def valid_languages(languages: str) -> str:
    pattern = re.compile(
        r"^(?:[a-zA-Z]{2,}(?:-[a-zA-Z0-9]+)?)(?:,(?:[a-zA-Z]{2,}(?:-[a-zA-Z0-9]+)?))*$"
    )
    if not bool(pattern.match(languages)):
        raise ValueError(
            "Invalid language codes or format. Supported language codes found here: https://www.jaided.ai/easyocr/."
        )
    return languages


def valid_boxes(boxes):
    if not isinstance(boxes, list):
        raise ValueError("Boxes must be a list.")
    if len(boxes) != 4:
        raise ValueError("Boxes must contain exactly 4 vertices.")
    try:
        vertices = [Vertex(x=pair[0], y=pair[1]) for pair in boxes]
    except Exception as e:
        raise ValueError(f"Invalid vertices: {e}")
    return vertices


class Vertex(BaseModel):
    x: int
    y: int


class TextAnnotations(BaseModel):
    boxes: Annotated[list[Vertex], BeforeValidator(valid_boxes)]
    text: str
    confidence: float = Field(validation_alias=AliasChoices("confident"))


class OCRResponse(BaseModel):
    text_annotations: list[TextAnnotations]


@app.post("/ocr")
async def ocr_processing(
    image: Annotated[UploadFile, File(description="Image file to run OCR on")],
    languages: Annotated[
        str,
        Form(
            description="Comma-separated list of language codes (e.g., en,ko,fr)",
        ),
        AfterValidator(valid_languages),
    ],
) -> OCRResponse:
    contents = await image.read()
    langs = languages.split(",")

    try:
        reader = get_reader(langs)
        results = reader.readtext(contents, output_format="json")
        response = [TextAnnotations(**json.loads(result)) for result in results]

        return OCRResponse(text_annotations=response)
    except Exception as e:
        print(f"[ERROR]: OCR processing failed: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong.")
