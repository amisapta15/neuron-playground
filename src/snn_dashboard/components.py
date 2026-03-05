from dash import dcc, html

BTN_STYLE_0 = {
    'backgroundColor': '#f8f9fa', 'color': '#aaa', 'width': '50px', 'height': '50px', 
    'margin': '2px', 'fontSize': '20px', 'cursor': 'pointer', 
    'border': '1px solid #ccc', 'borderRadius': '5px'
}
BTN_STYLE_1 = {
    'backgroundColor': '#28a745', 'color': 'white', 'width': '50px', 'height': '50px', 
    'margin': '2px', 'fontSize': '20px', 'cursor': 'pointer', 
    'border': '1px solid #28a745', 'borderRadius': '5px'
}

def create_matrix():
    rows = []
    # Header row for time
    header = html.Div([
        html.Div("Time:", style={'width': '100px', 'fontWeight': 'bold', 'textAlign': 'right', 'paddingRight': '10px', 'flexShrink': 0})] + 
        [html.Div(f"{t}ms", style={'width': '50px', 'textAlign': 'center', 'margin': '2px', 'flexShrink': 0}) for t in range(0, 130, 10)],
        style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'marginBottom': '5px'}
    )
    rows.append(header)
    
    for r in range(3):
        cols = [html.Div(f"Synapse {r+1}:", style={'width': '100px', 'fontWeight': 'bold', 'textAlign': 'right', 'paddingRight': '10px', 'flexShrink': 0})]
        for c in range(13):
            is_spike = (r, c) in [(0, 1), (1, 2), (2, 3)]
            val = "1" if is_spike else "0"
            btn_style = BTN_STYLE_1 if is_spike else BTN_STYLE_0
            btn = html.Button(
                val,
                id={'type': 'matrix-btn', 'row': r, 'col': c},
                n_clicks=1 if is_spike else 0,
                style=btn_style
            )
            cols.append(btn)
        rows.append(html.Div(cols, style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'}))
    return html.Div(rows, style={'overflowX': 'auto', 'paddingBottom': '10px'})

def get_app_layout():
    return html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#f4f6f9', 'minHeight': '100vh'}, children=[
        html.H1("Spiking Neural Network (SNN) Integration & Firing", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '5px'}),
        html.P("Interactive Plotly Dash WebApp for Synaptic Integration and LIF Neuron Dynamics", style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': '20px'}),
        
        html.Div([
            # Left Panel: Knobs/Controls
            html.Div(style={'flex': '1', 'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
                html.H3("Synapse Parameters", style={'marginTop': '0', 'color': '#34495e'}),
                
                html.Div([
                    html.Strong("Synapse 1 (Red)", style={'color': '#e74c3c'}),
                    html.Div("Weight:"),
                    dcc.Slider(id='w-0', min=0, max=5, step=0.1, value=2.0, marks={i: str(i) for i in range(6)}),
                    html.Div("Time Constant τ (ms):", style={'marginTop': '10px'}),
                    dcc.Slider(id='tau-0', min=2, max=40, step=2, value=10, marks={i: str(i) for i in range(10, 41, 10)}),
                ], style={'marginBottom': '15px', 'padding': '10px', 'backgroundColor': '#fdedec', 'borderRadius': '5px'}),
                
                html.Div([
                    html.Strong("Synapse 2 (Green)", style={'color': '#27ae60'}),
                    html.Div("Weight:"),
                    dcc.Slider(id='w-1', min=0, max=5, step=0.1, value=1.5, marks={i: str(i) for i in range(6)}),
                    html.Div("Time Constant τ (ms):", style={'marginTop': '10px'}),
                    dcc.Slider(id='tau-1', min=2, max=40, step=2, value=15, marks={i: str(i) for i in range(10, 41, 10)}),
                ], style={'marginBottom': '15px', 'padding': '10px', 'backgroundColor': '#e8f8f5', 'borderRadius': '5px'}),
                
                html.Div([
                    html.Strong("Synapse 3 (Blue)", style={'color': '#2980b9'}),
                    html.Div("Weight:"),
                    dcc.Slider(id='w-2', min=0, max=5, step=0.1, value=1.0, marks={i: str(i) for i in range(6)}),
                    html.Div("Time Constant τ (ms):", style={'marginTop': '10px'}),
                    dcc.Slider(id='tau-2', min=2, max=40, step=2, value=20, marks={i: str(i) for i in range(10, 41, 10)}),
                ], style={'marginBottom': '20px', 'padding': '10px', 'backgroundColor': '#eaf2f8', 'borderRadius': '5px'}),
                
                html.Hr(),
                html.H3("Neuron Parameters (LIF)", style={'color': '#34495e'}),
                dcc.Markdown("**Membrane Time Constant** $\\tau_m$ (ms):", mathjax=True),
                dcc.Slider(id='tau-m', min=5, max=50, step=5, value=20, marks={i: str(i) for i in range(10, 51, 10)}),
                dcc.Markdown("**Firing Threshold** ($V_{th}$):", mathjax=True, style={'marginTop': '10px'}),
                dcc.Slider(id='v-th', min=1.0, max=10.0, step=0.5, value=3.0, marks={i: str(i) for i in range(2, 11, 2)}),
            ]),
            
            # Right Panel: Matrix & Play Controls
            html.Div(style={'flex': '1.5', 'marginLeft': '20px', 'display': 'flex', 'flexDirection': 'column'}, children=[
                html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'marginBottom': '20px'}, children=[
                    html.H3("Input Sequence Matrix", style={'marginTop': '0', 'color': '#34495e'}),
                    html.P("Click to add/remove spikes (1 = Spike, 0 = Rest). Instantaneous update.", style={'color': '#7f8c8d'}),
                    html.Div(create_matrix(), style={'display': 'flex', 'justifyContent': 'center'}),
                ]),
                
                html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)', 'flexGrow': '1'}, children=[
                    html.H3("Playback Controls", style={'marginTop': '0', 'color': '#34495e'}),
                    html.P("Watch the sequence play out incrementally, or drag the scrubber.", style={'color': '#7f8c8d'}),
                    html.Button("▶ Play Sequence", id="play-btn", n_clicks=0, style={
                        'padding': '10px 20px', 'backgroundColor': '#3498db', 'color': 'white', 
                        'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px', 'marginRight': '10px'
                    }),
                    html.Button("↺ Reset", id="reset-btn", n_clicks=0, style={
                        'padding': '10px 20px', 'backgroundColor': '#95a5a6', 'color': 'white', 
                        'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px'
                    }),
                    html.Div("Time Progress:", style={'marginTop': '20px', 'fontWeight': 'bold', 'color': '#34495e'}),
                    dcc.Slider(id="time-scrubber", min=0, max=120, step=0.5, value=120, marks={0: '0ms', 50: '50ms (End Inputs)', 120: '120ms'}, tooltip={"placement": "bottom", "always_visible": True}),
                    dcc.Store(id="is-playing", data=False),
                    dcc.Interval(id="interval-timer", interval=50, n_intervals=0, disabled=True)
                ])
            ])
        ], style={'display': 'flex', 'flexDirection': 'row', 'marginBottom': '20px'}),
        
        # Bottom Panel: Simulation Plots
        html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
            dcc.Graph(id='simulation-plot', config={'displayModeBar': False}, mathjax=True)
        ])
    ])
