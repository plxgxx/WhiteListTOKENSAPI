import os
from app import app

port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
	app.run()
