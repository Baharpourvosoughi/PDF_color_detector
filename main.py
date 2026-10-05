from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz
from PIL import Image
import numpy as np
import os
import uuid

app = FastAPI(title="PDF Color Detector")


def is_colored_page(page: fitz.Page) -> bool:
    """Return True if the page contains color (non-grayscale) content."""
    pix = page.get_pixmap(alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    arr = np.array(img, dtype=float)
    # A page is grayscale when R, G, B channels have identical mean values
    means = arr.mean(axis=(0, 1))
    return not (means[0] == means[1] == means[2])


@app.post("/detect")
async def detect_colors(file: UploadFile = File(...)):
    """Analyze a PDF and return which pages are colored vs black & white."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Save to a unique temp path to avoid filename collisions
    temp_path = f"/tmp/{uuid.uuid4().hex}.pdf"
    try:
        contents = await file.read()
        with open(temp_path, "wb") as f:
            f.write(contents)

        colored_pages = []
        bw_pages = []

        with fitz.open(temp_path) as doc:
            for i, page in enumerate(doc, start=1):
                if is_colored_page(page):
                    colored_pages.append(i)
                else:
                    bw_pages.append(i)

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {
        "total_pages": len(colored_pages) + len(bw_pages),
        "colored_count": len(colored_pages),
        "bw_count": len(bw_pages),
        "colored_pages": colored_pages,
        "bw_pages": bw_pages,
    }
