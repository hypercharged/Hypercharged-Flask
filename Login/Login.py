import pyrebase
class Config:
    def __init__(self, conf):
        self.config = pyrebase.initialize_app(conf)
class CreateAccount:
    def __init__(self):
        print()
class UserLogin:
    auth = None
    def __init__(self, email, password, cfg):
        self.auth = cfg.config.auth()
        try:
            self.user = self.auth.sign_in_with_email_and_password(email, password)
        except:
            try:
                self.user = self.auth.create_user_with_email_and_password(email, password)
            except Exception as e:
                print(e)