from fastapi import FastAPI


app = FastAPI()

@app.get('/')
def index():
    return 'Hey'


@app.get('/about')
def about():
    return {'data':'about page'}