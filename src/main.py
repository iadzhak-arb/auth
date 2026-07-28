from fastapi import FastAPI

from src.schema import UserSignUp

app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post('/signup')
async def registration(user: UserSignUp):
    print(user)
    return {
        'message': 'User created',
        'email': user.email,
    }