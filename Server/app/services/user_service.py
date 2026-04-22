import asyncio
from fastapi import HTTPException, UploadFile, File, BackgroundTasks
from app.models import User
from app.repository import UserRepo
from app.dependencies import UserForm
from app.schemas import PasswordSchema, UserUpdate
from app.security import hash_password, verify_password, create_token, oaut2_form
from app.cloudinary import cloudinary_uploader

from datetime import datetime, timezone, timedelta
from typing import Optional

class UserService:
    def __init__(self, db, user_repo = UserRepo):
        self.db = db
        self.user_repo = user_repo(db)
    
    async def register(self, data: UserForm, photo_file: Optional[UploadFile] = File(None)):
        user_exists = await self.user_repo.exists_email_or_name(data.email, data.name)

        if user_exists:
            raise HTTPException(
                status_code=409,
                detail='Email ou nome ja existente.'
        )

        secure_url = 'No Profile Photo'
        public_id = None

        if photo_file:
            try:
                loop = asyncio.get_running_loop()
                upload_result = await loop.run_in_executor(
                    None,
                    lambda: cloudinary_uploader.upload(photo_file.file)
                )
                secure_url = upload_result['secure_url']
                public_id = upload_result['public_id']
            except Exception as e:
                print(f'erro no cloudinary, {e}')
                raise HTTPException(status_code=500, detail=f'Tivemos um problema ao salvar a sua foto, tente novamnte')

        password_hash = hash_password(data.password)

        user_created = User(
            name = data.name,
            email = data.email,
            password = password_hash,
            profile_photo = secure_url,
            public_photo_id = public_id
        )
        return await self.user_repo.create_user(user_created)
    
    async def login(self, data: oaut2_form):
        username_exist = await self.user_repo.username_exist(data.username)

        if not username_exist:
            raise HTTPException(
                status_code=400,
                detail='Senha ou email errado.'
            )
        elif not verify_password(data.password, username_exist.password):
            raise HTTPException(
                status_code=400,
                detail='Senha ou email errado.'
            )

        token = {
            'access_token': create_token(username_exist, datetime.now(timezone.utc) + timedelta(minutes=60)),
            'refresh_token': create_token(username_exist, datetime.now(timezone.utc) + timedelta(days=7)),
            'token_type': 'bearer',
        }
        return token
    
    async def update_password(self, data: PasswordSchema, user: User):
        password = verify_password(data.password, user.password)
        if not password:
            raise HTTPException(
                status_code=400,
                detail='Senha Incorreta'
            )
        new_password = await self.user_repo.update_password_user(hash_password(data.new_password), user)
        if not new_password:
            raise HTTPException(
                status_code=500,
                detail=f'Erro ao alterar Senha'
            )
        return {'msg': 'Senha alterada com sucesso!'}
    
    async def update_data(self, data: UserUpdate, user: User):
            if data.name == None or '' and data.email == None or '':
                raise HTTPException(status_code=400, detail='Nenhuma alteração foi feita')
            return await self.user_repo.update_user(data, user)

    async def add_photo(self,  background_tasks: BackgroundTasks, user: User, photo_file: UploadFile = File(...)):
        old_public_photo_id = user.public_photo_id
        loop = asyncio.get_running_loop()
        if photo_file :
            try:
                upload_result = await loop.run_in_executor(
                    None,
                    lambda: cloudinary_uploader.upload(photo_file.file)
                )
                secure_url = upload_result['secure_url']
                public_id = upload_result['public_id']
            except Exception as e:
                print(f'Erro no cloudinary: {e}')
                raise HTTPException(
                    status_code=409,
                    detail=f'Erro Ao Salvar a Imagem'
                )
        else:
            raise HTTPException(
                status_code=400,
                detail='Por Favor Insira uma Imagem'
            )

        try:
            if old_public_photo_id:
                background_tasks.add_task(cloudinary_uploader.destroy, old_public_photo_id)
            await self.user_repo.add_photo(secure_url, public_id, user)
        except Exception as e:
            print(f'Erro ao Salvar Imagem no cloudinary: {e}')
            raise HTTPException(
                status_code=500,
                detail='Erro ao salvar a foto.'
            )

        message = "Foto alterada com sucesso" if old_public_photo_id else "Foto adicionada com sucesso"
        return {
            "msg": message,
            "url": user.profile_photo
        }
                    