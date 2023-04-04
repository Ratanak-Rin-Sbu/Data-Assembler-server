from fastapi import FastAPI

app = FastAPI(
    title="DataAssembler",
)

# ROUTES
@app.get("/")
def read_root():
	return {"data":"Hello World"}