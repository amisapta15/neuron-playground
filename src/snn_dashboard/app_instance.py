import dash

# Define the Dash app globally so it can be imported by callbacks and layout
app = dash.Dash(__name__)
app.title = "SNN Dashboard"
