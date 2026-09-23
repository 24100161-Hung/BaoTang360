from fastapi import FastAPI

app = FastAPI(title="Bảo tàng ảo - Data Service")

@app.get("/healthz")
def health():
    return {"status": "ok"}
