from authx import AuthX, AuthXConfig


config:AuthXConfig = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET"
config.JWT_ACCESS_COOKIE_NAME = "solo_guide_auth"
config.JWT_TOKEN_LOCATION = ["cookies"]

SECURITY:AuthX = AuthX(config=config)