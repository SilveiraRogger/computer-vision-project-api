from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.api.routes import auth, detect, user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(detect.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    first_error = exc.errors()[0]
    field = first_error["loc"][-1]
    message = first_error["msg"]
    return JSONResponse(
        status_code=400, content={"message": f"Erro no campo '{field}': {message}"}
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500, content={"message": f"Erro interno: {str(exc)}"}
    )
