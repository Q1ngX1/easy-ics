from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return{"hello": "world"}

@app.get("/health")
def health_check():
    return {"status": "ok"}


def main():
    print("Hello from backend!")


if __name__ == "__main__":
    main()
