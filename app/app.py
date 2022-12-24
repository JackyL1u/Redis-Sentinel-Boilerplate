from fastapi import FastAPI, Request
import uvicorn
from tools.redis_client import RedisClient
import json
from tools.errors import *

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/get")
async def get_value(request: Request):
    try:
        data = await request.json()
    except (Exception,):
        return json_error

    key = data.get("key")

    try:
        result = RedisClient.get(str(key))
    except (Exception,):
        return key_error

    return result


@app.post("/set")
async def set_value(request: Request):
    try:
        data = await request.json()
    except (Exception,):
        return json_error

    key = data.get("key")
    value = data.get("value")

    try:
        value = json.dumps(value)
    except (Exception,):
        pass

    return RedisClient.set(key, value)

uvicorn.run(app, host="0.0.0.0", port=5000)
