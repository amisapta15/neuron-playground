from src.snn_dashboard.app_instance import app
from src.snn_dashboard.components import get_app_layout

# Import callbacks to register them with the app
import src.snn_dashboard.callbacks

app.layout = get_app_layout()
server = app.server

if __name__ == '__main__':
    print("Starting SNN Dashboard.")
    app.run(debug=True,port=8050)
