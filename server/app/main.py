from fastapi import FastAPI
import uvicorn
from app.routes.conversation_routes import router as conversation_router
from app.routes.message_routes import router as message_router

app = FastAPI()
app.include_router(conversation_router)
app.include_router(message_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)