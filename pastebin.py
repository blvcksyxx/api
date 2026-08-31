from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
import uuid
import time

app = FastAPI(
    title="BLVCKSYXX Pastebin",
    description="Simple pastebin for code snippets.",
    docs_url=None,
    redoc_url=None
)

# In-memory storage for pastes (For real production, use SQLite/PostgreSQL)
pastes = {}

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>dev.blvcksyxx.xyz - pastebin</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
          body { background-color: #000; color: #fff; font-family: monospace; text-transform: lowercase; }
          .focus-ring:focus { outline: none; border-color: #fff; }
          .glass { background: #000; border: 1px solid #333; }
        </style>
      </head>
      <body class="min-h-screen flex flex-col">
        <nav class="border-b border-gray-800 px-6 py-4 flex justify-between items-center mb-8">
            <div class="text-2xl font-bold tracking-widest">
                blvcksyxx paste
            </div>
            <div class="flex gap-4">
                <a href="https://blvcksyxx.xyz" target="_blank" class="text-gray-400 hover:text-white transition"><i class="fa-solid fa-globe"></i> blvcksyxx.xyz</a>
                <a href="https://t.me/blvcksyxxchannel" target="_blank" class="text-gray-400 hover:text-white transition"><i class="fa-brands fa-telegram"></i> @blvcksyxxchannel</a>
            </div>
        </nav>
        
        <main class="flex-grow container mx-auto px-4 flex flex-col items-center">
            <div class="w-full max-w-4xl glass p-6">
                <form action="/new" method="post" class="flex flex-col gap-4">
                    <div class="flex justify-between items-center px-1">
                        <label class="text-sm font-bold text-gray-400 tracking-wider">new snippet</label>
                    </div>
                    <textarea name="content" required placeholder="paste your code here..." 
                        class="w-full h-[500px] bg-black text-white p-4 font-mono text-sm resize-none border border-gray-700 transition focus-ring"
                        spellcheck="false"></textarea>
                    
                    <button type="submit" class="self-end bg-white text-black font-bold tracking-wider py-3 px-8 transition hover:bg-gray-300 flex items-center gap-2">
                        <i class="fa-solid fa-arrow-turn-down fa-rotate-90"></i> create paste
                    </button>
                </form>
            </div>
        </main>
        
        <footer class="text-center py-6 text-gray-600 text-sm mt-auto tracking-widest">
            &copy; 2026 blvcksyxx.xyz
        </footer>
      </body>
    </html>
    """

@app.post("/new")
async def create_paste(content: str = Form(...)):
    paste_id = uuid.uuid4().hex[:8]
    pastes[paste_id] = {
        "content": content,
        "created_at": time.time()
    }
    return RedirectResponse(url=f"/{paste_id}", status_code=303)

@app.get("/{paste_id}")
async def get_raw_paste(paste_id: str):
    paste = pastes.get(paste_id)
    if not paste:
        return PlainTextResponse("paste not found", status_code=404)
    return PlainTextResponse(paste["content"])



