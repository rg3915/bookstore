from ninja import NinjaAPI

from bookstore.api import router as bookstore_router

api = NinjaAPI()

api.add_router('/bookstore/', bookstore_router)
