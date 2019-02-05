import pyrebase
class Config:
    def __init__(self, conf):
        self.config = pyrebase.initialize_app(conf)
class CreateAccount:
    def __init__(self):
        print()
class UserLogin:
    def __init__(self, email, password, cfg):
        auth = cfg.config.auth()
        try:
            auth.sign_in_with_email_and_password(email, password)
        except:
            try:
                auth.create_user_with_email_and_password(email, password)
            except:
                print("EMAIL/PASSWORD incorrect")