from src import app
from configs import App_Config

@app.route("/test")
def test():
    return "EVALSYS API TEST"

if __name__ == "__main__":
    app.run(host=App_Config.HOST, port=App_Config.PORT, debug=App_Config.DEBUG)
    