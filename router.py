from fastapi import APIRouter, Depends, File, UploadFile
import pyrebase
import openai

router = APIRouter()

openai.api_key = "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"


def getDb():
    config = {
        "apiKey": "AIzaSyD3XIbP2aJ2p-oAELSdJBN4uIoaeYL3CKM",
        "authDomain": "flash-chat-ios-4dc92.firebaseapp.com",
        "databaseURL": "https://flash-chat-ios-4dc92-default-rtdb.firebaseio.com",
        "projectId": "flash-chat-ios-4dc92",
        "storageBucket": "flash-chat-ios-4dc92.appspot.com",
        "messagingSenderId": "266501316835",
        "appId": "1:266501316835:web:66840b54e5393e0542a5d6"
    }
    firebase = pyrebase.initialize_app(config)
    return firebase


@router.get("/products")
async def getProducts():
    db = getDb()
    products = db.database().child("products").get()
    produc = {"data": []}
    for user in products.val().items():
        produc["data"].append(user[1])
    return produc


@router.get("/createimage")
async def createImage(prompt: str):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url


@router.get("/generateText")
async def generateText(prompt: str):
    response = openai.Completion.create(
        prompt=prompt,
        model="text-davinci-003"
    )

    return response['choices'][0]['text']


@router.post("/products")
async def addProduct(name: str, price: float, file: UploadFile):
    db = getDb()
    storage = db.storage()
    storage.child("/products").child(file.filename).put(file.file)
    url = storage.child("/products").get_url("")
    # .set gives custom id
    # .push generated automatically
    db.database().child("products").push({"name": name, "price": price, "url": url})
    products = db.database().child("products").get()
    produc = {"data": []}
    for user in products.val().items():
        produc["data"].append(user[1])
    return produc


@router.delete("/products")
async def deleteProducts():
    db = getDb()
    storage = db.storage()
    storage.delete("products", "")
    db.database().child("products").remove()
    return {"data": "Items deleted successfully!"}
