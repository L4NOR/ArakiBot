from aiohttp import web
import asyncio
from config_catenaccio import PORT

# Configuration du serveur web
app = web.Application()

async def handle_health_check(request):
    return web.Response(text="Catenaccio Bot is running! ⚽", status=200)

app.router.add_get('/', handle_health_check)

# Fonction pour lancer le serveur web
async def start_webserver(bot):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    print(f"Serveur web démarré sur le port {PORT}")