from __future__ import annotations

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from calc_core import evaluate_expression


# --- FastAPI app ---

app = FastAPI(
    title="Modern Calculator",
    description="A small FastAPI app that serves a static calculator UI and exposes a /api/calc endpoint.",
)

# Serve the static UI from the `static/` folder.
app.mount("/", StaticFiles(directory="static", html=True), name="static")


class CalcRequest(BaseModel):
    expression: str = Field(..., example="2*(3+4)")


class CalcResponses(BaseModel):
    result: float


@app.post("/api/calc", response_model=CalcResponses)
async def calculate(request: CalcRequest) -> CalcResponses:
    """Evaluate a calculator expression and return the result as JSON."""

    try:
        result = evaluate_expression(request.expression)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    return CalcResponses(result=result)


if __name__ == "__main__":
    # Run with: python calculator.py
    import uvicorn

    uvicorn.run("calculator:app", host="127.0.0.1", port=8000, reload=True)
