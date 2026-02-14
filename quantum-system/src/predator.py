import asyncio, aiohttp, subprocess

# DADOS FIXOS - NÃO DEPENDEM DO SISTEMA
TOKEN = "8283927359:AAFShb2avZoTudbzGjl6DC84xilDTrU8Eyk"
CHAT_ID = "1875372841"
URL_FEED = "https://hackerone.com/hacktivity.json?filter=type%3Apublic-programs"

async def avisar(txt):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": txt, "parse_mode": "Markdown"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as r:
            return await r.json()

async def caçar(handle):
    alvo = f"{handle}.com"
    await avisar(f"🔭 **CAÇANDO:** `{alvo}`")
    # Recon de subdomínios rápido
    cmd = f"~/go/bin/subfinder -d {alvo} -silent | ~/go/bin/httpx -silent"
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        out, _ = p.communicate()
        vivos = out.decode().splitlines()
        if vivos:
            await avisar(f"✅ **VIVOS:**\n" + "\n".join(vivos[:3]))
            # Scan básico de vulnerabilidade
            for v in vivos[:2]:
                s_cmd = f"~/go/bin/nuclei -u {v} -severity low,medium -silent"
                s_p = subprocess.Popen(s_cmd, shell=True, stdout=subprocess.PIPE)
                s_out, _ = s_p.communicate()
                if s_out: await avisar(f"🎯 **ACHADO:**\n`{s_out.decode()[:500]}`")
    except: pass

async def watch():
    print("🦅 PREDADOR ONLINE")
    status = await avisar("🟢 **SISTEMA ONLINE EM MESQUITA**\nVigiando HackerOne...")
    if not status.get("ok"):
        print(f"❌ ERRO: {status.get('description')}")
        return
    last_id = None
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL_FEED) as r:
                    data = await r.json()
                    top = data['nodes'][0]
                    if top['id'] != last_id:
                        if last_id: asyncio.create_task(caçar(top['team']['handle']))
                        last_id = top['id']
        except: pass
        await asyncio.sleep(120)

if __name__ == "__main__":
    asyncio.run(watch())
