import os
from dotenv import load_dotenv

# use env file from base directory - above lambdas
dotenv_path = os.path.join(os.path.dirname(__file__), "../../", ".env")
print(f"INFO: dotenv path: {dotenv_path}")
load_dotenv(dotenv_path)
