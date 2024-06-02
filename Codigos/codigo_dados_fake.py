from faker import Faker
import random
import pymongo
import datetime

# Configurações de conexão ao MongoDB com autenticação
username = "root"
password = "123"
database_name = "supermarket"
connection_string = f"mongodb://{username}:{password}@localhost:27017/"

# Conectar ao MongoDB
client = pymongo.MongoClient(connection_string)
db = client[database_name]
core_collection = db["core_data"]
extended_collection = db["extended_data"]

# Gerar e inserir dados simulados
fake = Faker()

for _ in range(10000):
    store_id = fake.uuid4()
    product_id = fake.uuid4()

    core_data = {
        "store_id": store_id,
        "product_id": product_id,
        "product_name": fake.word(),
        "category": fake.word(),
        "quantity": random.randint(1, 100),
        "price": round(random.uniform(1, 100), 2)
    }
    core_collection.insert_one(core_data)

    sales_history = [{"date": fake.date_this_year().strftime("%Y-%m-%d"), "quantity_sold": random.randint(1, 10)} for _
                     in range(random.randint(1, 10))]
    extended_data = {
        "product_id": product_id,
        "supplier": fake.company(),
        "sales_history": sales_history
    }
    extended_collection.insert_one(extended_data)
