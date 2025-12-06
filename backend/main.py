from fastapi import FastAPI
from routes.residentes import router as residentes_router
from routes.accesos import router as accesos_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(residentes_router)
app.include_router(accesos_router)

@app.get("/")
def root():
    return {"message": "Backend running"}
