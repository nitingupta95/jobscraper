import os
from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv('.env')

import uvicorn

port = int(os.getenv('PORT', 8000))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
