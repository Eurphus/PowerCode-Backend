import dotenv
from convex import ConvexClient
import os

dotenv.load_dotenv()

client = ConvexClient(os.getenv("CONVEX_URL"))

print(client.query("players"))
