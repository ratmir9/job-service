from src import app
import config

if __name__ == '__main__':
  app.run(
    host=config.SERVER_HOST,
    port=config.SERVER_PORT
  )

