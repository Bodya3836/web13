from fastapi import APIRouter, Depends, HTTPException, status, Security, BackgroundTasks, Request, File, UploadFile
from depenedencies.database import get_db, SessionLocal
from depenedencies.auth import Token, create_access_token, get_current_user
from schemas.user import User, UserConfirmed
from services.users import UserService
from services.email import send_email
from fastapi.security import OAuth2PasswordRequestForm

from depenedencies.rate_limiter import RateLimiter
from depenedencies.cloudinary_client import get_uploader


router = APIRouter()

rate_limiter = RateLimiter(3, 120)

async def rate_limit(request: Request):
    global rate_limiter
    client_id = request.client.host
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(status_code=429, detail="Too Many Requests")
    return True




@router.post("/register", response_model=User)
async def register(user: User, db: SessionLocal = Depends(get_db)):
    user_service = UserService(db=db)
    return user_service.create_new(user)

@router.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_for_auth(form_data.username, form_data.password)
    access_token = create_access_token(username = user.username, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected-resource/", response_model=User)
async def protected_resource(current_user: User = Depends(get_current_user)):
    return current_user



@router.post('/confirmed/', response_model=User)
async def confirmed(data: UserConfirmed, db: SessionLocal = Depends(get_db)):
    user_service = UserService(db)
    return user_service.confirmed_user(data)

@router.post("/upload_image")
def upload(current_user: User = Depends(get_current_user), file: UploadFile = File(...),  uploader = Depends(get_uploader), db: SessionLocal = Depends(get_db)):
    try:
        current_user
        user_service = UserService(db)
        contents = file.file.read()
        responce = uploader.upload(contents, public_id=file.filename)
        responce.get('secure_url')
        user_service.set_image(current_user, responce.get('secure_url'))

    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}