import os
import logging
import pathlib
import json
import hashlib
from fastapi import FastAPI, HTTPException, Form, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "images"
origins = [os.environ.get("FRONT_URL", "http://localhost:3000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
#pythonカスタム型でggl
#プログラミングで変数って言ったらy=x+2のyで、xは元々ある値しか入れられない
#何かを箱(=変数)の中に入れて保管したい
#classはテンプレート
#class item:
#    def __init__(self, name, category):
#        self.name = name
#        self.category = category
# 何行もコメントアウトしたい時は⌘/

@app.get("/")
def root():
    return {"message": "Hello, world!"}


@app.post("/items")
#メソッドを指定している
#アクセスしても返ってこないのはポストだから

#step3-3
#かっこの中が引数で、入力された情報
#
def add_item(name: str = Form(...), category: str = Form(...)):
    #変数の定義
    #変数の定義は＝を使う、これは代入
    #名前つけて保存しておこう、が代入
    item = {"name": name, "category": category}
    #itemは型を定義してない。。上へ行って型を定義したい！
    #jsonファイルを開くよ
    with open('items.json', 'r') as file:
        #jsonファイルの情報を読み込む
        #辞書型（keyとvalueの組み合わせ）になっている
        #jsonファイルと相性が良い型らしい
        #keyとvalueの組み合わせとして読み込める！
        #json.load(file)って書けば辞書型として読み込める！
        items_data = json.load(file)
    print (items_data)
    #{'items': [{'name': 'jacket', 'category': 'fashion'}]}が返ってくる
    #[]がリスト、{}が辞書型
    #今から{}を増やして情報を追加していきたい
    items_data['items'].append(item)
    #items_data['items'].append({"name": name, "category": category})
    print (items_data)
    with open('items.json', 'w') as file:
        json.dump(items_data, file)
        #できたぁ！
    logger.info(f"Receive item: {name}")
    #user側に返すメッセージ
    return {"message": f"item received: {name}"}
#
# async def add_item(name: str = Form(...), category: str = Form(...), image: Optional[UploadFile] = None):
#     # アイテム情報のログ出力
#     logger.info(f"Received item: {name}, Category: {category}")
#     # 画像ファイルがある場合は処理
#     image_name = ""
#     if image:
#         # 画像の内容を読み取り
#         contents = await image.read()
#         # 画像のハッシュ値を計算してファイル名を生成
#         hash_name = hashlib.sha256(contents).hexdigest()
#         image_name = f"{hash_name}.jpg"
#         image_path = os.path.join(images_dir, image_name)
#         # 画像をファイルに保存
#         with open(image_path, "wb") as file:
#             file.write(contents)
#         logger.info(f"Image saved: {image_name}")

#     # 新しいアイテムIDの決定
#     new_item_id = 1
#     try:
#         with open("items.json", "r") as file:
#             data = json.load(file)
#             if data["items"]:
#                 new_item_id = max(item["item_id"] for item in data["items"]) + 1
#     except FileNotFoundError:
#         raise HTTPException(
#             status_code=404, detail="'items.json' not found"
#         )
    
# @app.get("/items")
# def get_items():
#     with open('items.json', 'r') as file:
#         items_data = json.load(file)
#     return items_data

# # アイテムゲットその２
# @app.get("/items")
# async def get_items():
#     try:
#         with open("items.json", "r") as file:
#             data = json.load(file)
#             return data
#     except FileNotFoundError:
#         # return {"detail": "Items not found."}


# @app.get("/items/{item_id}")
# def get_item_id(item_id: int):
#     with open('items.json', 'r') as file:
#         items_data = json.load(file)
#         items_list = items_data["items"]
#         item = items_list[item_id]
#         return item


# @app.get("/image/{image_name}")
# async def get_image(image_name):
#     # Create image path
#     image = images / image_name

#     if not image_name.endswith(".jpg"):
#         raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

#     if not image.exists():
#         logger.debug(f"Image not found: {image}")
#         image = images / "default.jpg"

#     return FileResponse(image)
