from fastapi import FastAPI, Request, Query
from fastapi.responses import RedirectResponse, Response, HTMLResponse
from pydantic import BaseModel
from faker import Faker
from user_agents import parse
from PIL import Image, ImageDraw, ImageFont
import io

app = FastAPI(
    title="blvcksyxx api",
    description="awesome developer api by blvcksyxx. placeholder images, mock data, and more.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

fake = Faker()

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
      <head>
        <title>blvcksyxx api reference</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <style>
          body { margin: 0; background: #111; }
          * { text-transform: lowercase !important; }
        </style>
      </head>
      <body>
        <script id="api-reference" data-url="/openapi.json"></script>
        <script>
          document.getElementById('api-reference').dataset.configuration = JSON.stringify({
            theme: 'default',
            hideModels: true,
            hideDownloadButton: true,
            hideClientButton: true,
            hideDarkModeToggle: true,
            customCss: `
              .scalar-app-header-controls { display: none !important; }
              header .flex { display: none !important; }
              .powered-by-scalar { display: none !important; }
              a[href*="scalar.com"] { display: none !important; }
              * { font-family: monospace; }
            `
          })
          
          setInterval(() => {
            document.querySelectorAll('button, a').forEach(el => {
                const text = el.innerText ? el.innerText.toLowerCase().trim() : '';
                if (text === 'ask ai' || text === 'generate mcp server' || text === 'generate mcp' || text === 'agents') {
                    if (el.style.display !== 'none') el.style.display = 'none';
                }
            });
          }, 500);
        </script>
        <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
      </body>
    </html>
    """)

@app.get("/ip", tags=["tools"], summary="get your ip address")
async def get_ip(request: Request):
    client_ip = request.client.host
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        client_ip = forwarded.split(",")[0]
    return {"ip": client_ip}


@app.get("/image", tags=["tools"], summary="generate placeholder image")
async def generate_image(
    width: int = Query(300, description="image width"),
    height: int = Query(200, description="image height"),
    bg_color: str = Query("000000", description="background color (hex without #)"),
    text_color: str = Query("FFFFFF", description="text color (hex without #)"),
    text: str = Query("blvcksyxx", description="text on image"),
    font_size: int = Query(40, description="font size")
):
    img = Image.new('RGB', (width, height), color=f"#{bg_color}")
    d = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.truetype("Roboto-Regular.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    
    bbox = d.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    
    d.text((x, y), text, fill=f"#{text_color}", font=font)

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    
    return Response(content=img_byte_arr.getvalue(), media_type="image/png")


@app.get("/mock/users", tags=["mock data"], summary="generate mock users")
async def get_mock_users(count: int = Query(5, ge=1, le=50, description="count (1 to 50)")):
    users = []
    for _ in range(count):
        fake_name = fake.name().lower()
        users.append({
            "id": fake.uuid4(),
            "name": fake_name,
            "email": fake_name.replace(" ", ".") + "@gmail.com",
            "job": fake.job().lower(),
            "address": fake.address().lower()
        })
    return users


@app.get("/ua", tags=["tools"], summary="parse user-agent")
async def parse_user_agent(request: Request, ua: str = Query(None, description="user-agent string (optional, defaults to headers)")):
    ua_string = ua if ua else request.headers.get('user-agent', '')
    user_agent = parse(ua_string)
    
    return {
        "is_mobile": user_agent.is_mobile,
        "is_tablet": user_agent.is_tablet,
        "is_pc": user_agent.is_pc,
        "is_bot": user_agent.is_bot,
        "browser": {
            "family": user_agent.browser.family.lower(),
            "version": user_agent.browser.version_string,
        },
        "os": {
            "family": user_agent.os.family.lower(),
            "version": user_agent.os.version_string,
        },
        "device": {
            "family": user_agent.device.family.lower(),
        },
        "raw_string": ua_string.lower()
    }


@app.get("/about", tags=["personal"], summary="about me")
async def about_me():
    return {
        "nickname": "blvcksyxx",
        "domain": "blvcksyxx.xyz",
        "role": "developer / creator",
        "skills": ["python", "api development", "being awesome"],
        "links": {
            "github": "https://github.com/blvcksyxx",
            "website": "https://blvcksyxx.xyz"
        }
    }

@app.get("/status", tags=["personal"], summary="current status")
async def current_status():
    return {
        "status": "online",
        "activity": "building my awesome api",
        "coffee_cups_today": 3
    }


