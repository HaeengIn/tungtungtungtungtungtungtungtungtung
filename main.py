from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.gzip import GZipMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime
from starlette.responses import Response
import os

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class CachedStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response: Response = await super().get_response(path, scope)
        if response.status_code == 200:
            response.headers["Cache-Control"] = "public, max-age=10368000, immutable"
        return response

app = FastAPI()
app.mount("/static", CachedStaticFiles(directory="static"), name="static")
app.add_middleware(GZipMiddleware, minimum_size=500)
templates = Jinja2Templates(directory="templates")

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def fixDatetime(posts):
    for post in posts:
        if "created_at" in post and post["created_at"]:
            strCreatedAt = post["created_at"]
            if isinstance(strCreatedAt, str):
                strCreatedAt = datetime.fromisoformat(strCreatedAt)
            post["created_at"] = strCreatedAt.strftime("%Y/%m/%d %H/%M/%S")
    return posts

@app.get("/")
def index(request: Request):
    response = supabase.table("ght_posts").select("*").order("id", desc=True).execute()
    posts = fixDatetime(response.data)
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

@app.get("/write")
def write(request: Request):
    return templates.TemplateResponse("write.html", {"request": request})

@app.post("/write")
def writePosts(request: Request, username: str = Form(...), title: str = Form(...), content: str = Form(...)):
    supabase.table("ght_posts").insert({"username": username, "title": title, "content": content}).execute()
    return RedirectResponse(url="/", status_code=303)

@app.get("/{id}")
def view(request: Request, id: int):
    response = supabase.table("ght_posts").select("*").eq("id", id).single().execute()
    posts = fixDatetime([response.data])
    return templates.TemplateResponse("view.html", {"request": request, "posts": posts[0]})