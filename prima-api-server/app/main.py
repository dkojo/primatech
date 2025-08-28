from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routes import router

app = FastAPI()
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def welcome():
    return """
    <html>
        <head>
            <title>Welcome to Prima API</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(to right, #2c3e50, #4ca1af);
                    color: white;
                }
                h1 {
                    font-size: 3rem;
                    font-weight: bold;
                    margin-top: 12%;
                    text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
                }
                p {
                    font-size: 1.3rem;
                    margin-bottom: 30px;
                    font-weight: 300;
                }
                a.button {
                    display: inline-block;
                    margin: 15px;
                    padding: 15px 35px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 1.2rem;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
                    transition: all 0.3s ease;
                }
                a.button:hover {
                    background-color: #45a049;
                    transform: translateY(-3px);
                    box-shadow: 0px 6px 15px rgba(0,0,0,0.4);
                }
            </style>
        </head>
        <body>
            <h1>👋 Welcome to the Prima API <br> By <span style="color: #FFD700;">Robert Megbenu</span></h1>
            <p>Use the links below to explore:</p>
            <a href="/users" class="button">List Users</a>
            <a href="/docs" class="button">Upload User (Swagger UI)</a>
        </body>
        </html>
    """

