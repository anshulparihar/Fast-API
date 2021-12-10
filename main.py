from fastapi import FastAPI


app = FastAPI()

@app.get('/')   #app is a variable name act as FastAPI instance
def index():
    return 'Hey'


@app.get('/about/{id}')
def about(id :int):
    # id = int(id)
    return({'data':id})