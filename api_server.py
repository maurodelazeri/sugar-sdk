from fastapi import FastAPI, HTTPException
from dataclasses import asdict
from sugar.chains import AsyncOPChain

app = FastAPI()

_chain: AsyncOPChain | None = None

@app.on_event("startup")
async def startup_event():
    global _chain
    _chain = AsyncOPChain()
    await _chain.__aenter__()

@app.on_event("shutdown")
async def shutdown_event():
    if _chain is not None:
        await _chain.__aexit__(None, None, None)

@app.get("/pool/{address}")
async def get_pool(address: str):
    if _chain is None:
        raise HTTPException(status_code=500, detail="Chain not initialized")
    pool = await _chain.get_pool_by_address(address)
    if pool is None:
        raise HTTPException(status_code=404, detail="Pool not found")
    return asdict(pool)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000)
