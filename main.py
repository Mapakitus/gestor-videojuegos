# Ejecutar en la terminal uvicorn main:app --reload o ejecuta el main y gracias a la sección if __name__ == "__main__" se levantará el servidor automáticamente.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import subprocess

    subprocess.run(["uvicorn", "main:app", "--reload"])
