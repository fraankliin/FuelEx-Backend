from supabase import create_client, ClientOptions
from api.config import settings
import httpx

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_SECRET

http_client = httpx.Client(
    timeout=httpx.Timeout(
        connect=10.0,
        read=30.0,
        write=30.0,
        pool=30.0
    )
)

options = ClientOptions(
    httpx_client=http_client
)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
    options=options
)