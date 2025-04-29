from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/next-available-slot')
def next_available_slot():
    pass

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)