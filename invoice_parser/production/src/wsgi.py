from app import invoice_app
import config

if __name__ == "__main__":
    invoice_app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
