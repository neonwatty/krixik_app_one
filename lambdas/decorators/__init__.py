import os

aws_profile = os.getenv("AWS_PROFILE")
STAGE = os.environ.get("STAGE", "development")
