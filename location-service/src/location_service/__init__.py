import os

import uvicorn


def main() -> None:
    uvicorn.run("location_service.main:app", port=int(os.getenv("PORT", "8082")))
