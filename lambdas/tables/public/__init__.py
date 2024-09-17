import os
from supabase import create_client, Client

supabase_client: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
