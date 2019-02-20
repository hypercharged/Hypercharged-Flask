from app.Shop.Prices import Prices; import random, string
class Wallpaper:
	BASE_URL = "localhost:5000"
	amount, price, user_uid = 0, 0, ""
	def __init__(self,  *args, **kwargs):
		self.amount = kwargs.get("amount")
		self.price = Prices[kwargs.get("amount")].value
		self.user_uid = kwargs.get("uuid")
		self.wallpaper_id = kwargs.get("wallpaper_id")
		self.request_token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))