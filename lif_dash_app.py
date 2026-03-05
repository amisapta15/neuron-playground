import dash
from dash import dcc, html, Input, Output, State, MATCH, ALL
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

app = dash.Dash(__name__)
app.title = "SNN Dashboard"

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
        html.Div("Time:", style={'width': '100px', 'fontWeight': 'bold', 'textAlign': 'right', 'paddingRight': '10px'})] + 
        [html.Div(f"{t}ms", style={'width': '50px', 'textAlign': 'center', 'margin': '2px'}) for t in [0, 10, 20, 30, 40]],
        style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'marginBottom': '5px'}
    )
    rows.append(header)
    
    for r in range(3):
        cols = [html.Div(f"Synapse {r+1}:", style={'width': '100px', 'fontWeight': 'bold', 'textAlign': 'right', 'paddingRight': '10px'})]
        for c in range(5):
            btn = html.Button(
                "0",
                id={'type': 'matrix-btn', 'row': r, 'col': c},
                n_clicks=0,
                style=BTN_STYLE_0
            )
            cols.append(btn)
        rows.append(html.Div(cols, style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center'}))
    return html.Div(rows)

app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#f4f6f9', 'minHeight': '100vh'}, children=[
    html.H1("Spiking Neural Network (SNN) Integration & Firing", style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '5px'}),
    html.P("Interactive Plotly Dash WebApp for Synaptic Integration and LIF Neuron Dynamics", style={'textAlign': 'center', 'color': '#7f8c8d', 'marginBottom': '30px'}),
    
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
            ], style={'marginBottom': '15px', 'padding': '10px', 'backgroundColor': '#eaaf5' , 'backgroundColor': '#e8f8f5', 'borderRadius': '5px'}),
            
            html.Div([
                html.Strong("Synapse 3 (Blue)", style={'color': '#2980b9'}),
                html.Div("Weight:"),
                dcc.Slider(id='w-2', min=0, max=5, step=0.1, value=1.0, marks={i: str(i) for i in range(6)}),
                html.Div("Time Constant τ (ms):", style={'marginTop': '10px'}),
                dcc.Slider(id='tau-2', min=2, max=40, step=2, value=20, marks={i: str(i) for i in range(10, 41, 10)}),
            ], style={'marginBottom': '20px', 'padding': '10px', 'backgroundColor': '#eaf2f8', 'borderRadius': '5px'}),
            
            html.Hr(),
            html.H3("Neuron Parameters (LIF)", style={'color': '#34495e'}),
            html.Div("Membrane Time Constant τ_m (ms):"),
            dcc.Slider(id='tau-m', min=5, max=50, step=5, value=20, marks={i: str(i) for i in range(10, 51, 10)}),
            html.Div("Firing Threshold ($V_{th}$):", style={'marginTop': '10px'}),
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
                dcc.Slider(id="time-scrubber", min=0, max=80, step=0.5, value=80, marks={0: '0ms', 50: '50ms (End Inputs)', 80: '80ms'}, tooltip={"placement": "bottom", "always_visible": True}),
                # Hidden stores for playback state
                dcc.Store(id="is-playing", data=False),
                dcc.Interval(id="interval-timer", interval=50, n_intervals=0, disabled=True)
            ])
        ])
    ], style={'display': 'flex', 'flexDirection': 'row', 'marginBottom': '20px'}),
    
    # Bottom Panel: Simulation Plots
    html.Div(style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'}, children=[
        dcc.Graph(id='simulation-plot', config={'displayModeBar': False})
    ])
])

# Toggle Matrix Buttons
@app.callback(
    Output({'type': 'matrix-btn', 'row': MATCH, 'col': MATCH}, 'children'),
    Output({'type': 'matrix-btn', 'row': MATCH, 'col': MATCH}, 'style'),
    Input({'type': 'matrix-btn', 'row': MATCH, 'col': MATCH}, 'n_clicks'),
    State({'type': 'matrix-btn', 'row': MATCH, 'col': MATCH}, 'children'),
    prevent_initial_call=True
)
def toggle_button(n_clicks, current_state):
    if current_state == "0":
        return "1", BTN_STYLE_1
    return "0", BTN_STYLE_0

# Play/Pause Logic
@app.callback(
    Output('interval-timer', 'disabled'),
    Output('is-playing', 'data'),
    Output('play-btn', 'children'),
    Output('play-btn', 'style'),
    Input('play-btn', 'n_clicks'),
    Input('reset-btn', 'n_clicks'),
    Input('time-scrubber', 'value'),
    State('is-playing', 'data'),
    prevent_initial_call=True
)
def play_controls(play_clks, reset_clks, curr_time, is_playing):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    style_play = {'padding': '10px 20px', 'backgroundColor': '#3498db', 'color': 'white', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px', 'marginRight': '10px'}
    style_pause = {'padding': '10px 20px', 'backgroundColor': '#e67e22', 'color': 'white', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px', 'marginRight': '10px'}

    if trigger_id == 'play-btn':
        new_state = not is_playing
        # If scrubbing reached the end and user clicks play, restart from 0
        if new_state and curr_time >= 80:
           # Will be handled by advance_time to loop or rest, but we just toggle
           pass
        text = "⏸ Pause Sequence" if new_state else "▶ Play Sequence"
        style = style_pause if new_state else style_play
        return (not new_state), new_state, text, style
        
    elif trigger_id == 'reset-btn':
        return True, False, "▶ Play Sequence", style_play
        
    elif trigger_id == 'time-scrubber':
        if curr_time >= 80 and is_playing:
            return True, False, "▶ Play Sequence", style_play
            
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update

# Time Scrubber Advancement
@app.callback(
    Output('time-scrubber', 'value'),
    Input('interval-timer', 'n_intervals'),
    Input('reset-btn', 'n_clicks'),
    State('is-playing', 'data'),
    State('time-scrubber', 'value'),
    prevent_initial_call=True
)
def advance_time(n_intervals, reset_clks, is_playing, current_time):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if trigger_id == 'reset-btn':
        return 0
        
    if trigger_id == 'interval-timer' and is_playing:
        new_time = current_time + 1.0  # advance 1ms per 50ms interval tick (smooth)
        if new_time > 80:
            return 80
        return new_time
        
    return dash.no_update

# Main Simulation & Plot Update
@app.callback(
    Output('simulation-plot', 'figure'),
    Input({'type': 'matrix-btn', 'row': ALL, 'col': ALL}, 'children'),
    Input('time-scrubber', 'value'),
    Input('w-0', 'value'), Input('tau-0', 'value'),
    Input('w-1', 'value'), Input('tau-1', 'value'),
    Input('w-2', 'value'), Input('tau-2', 'value'),
    Input('tau-m', 'value'), Input('v-th', 'value')
)
def update_simulation_plot(matrix_vals, scrub_time, w0, t0, w1, t1, w2, t2, tau_m, v_th):
    # Parse Matrix
    spike_matrix = np.zeros((3, 5))
    ctx = dash.callback_context
    try:
        if ctx.inputs_list:
            for inp in ctx.inputs_list[0]:
                row = inp['id']['row']
                col = inp['id']['col']
                spike_matrix[row, col] = int(inp['value'])
    except Exception as e:
        pass # default to zeros on load error
        
    weights = [w0, w1, w2]
    taus = [t0, t1, t2]
    
    # Simulation Settings
    dt = 0.5  # ms precision
    T_total = 80.0 # ms simulation time
    time = np.arange(0, T_total + dt, dt)
    step_duration = 10.0 # ms between columns
    
    V_syn = np.zeros((3, len(time)))
    I_total = np.zeros(len(time))
    V_m = np.zeros(len(time))
    v_reset = 0.0
    spikes_x = []
    spikes_y = []
    
    # Handle inputs exactly at t=0 before loop
    if time[0] <= 40:
        for syn_idx in range(3):
            if spike_matrix[syn_idx, 0] == 1:
                V_syn[syn_idx, 0] += weights[syn_idx]
                
    # Run integration over time
    for t_idx in range(1, len(time)):
        # 1. Decay Synapse (from previous state)
        for syn_idx in range(3):
            dV_syn = -(V_syn[syn_idx, t_idx-1] / taus[syn_idx]) * dt
            V_syn[syn_idx, t_idx] = max(0, V_syn[syn_idx, t_idx-1] + dV_syn)
            
        # 2. Add Spikes arriving exactly at this time
        if time[t_idx] <= 40 and abs(time[t_idx] % step_duration) < 1e-5:
            col = int(round(time[t_idx] / step_duration))
            for syn_idx in range(3):
                if spike_matrix[syn_idx, col] == 1:
                    V_syn[syn_idx, t_idx] += weights[syn_idx]
                    
        # 3. Sum total current
        I_total[t_idx] = np.sum(V_syn[:, t_idx])
        
        # 4. Integrate Membrane Potential
        dV_m = (-V_m[t_idx-1] + I_total[t_idx]) / tau_m * dt
        v_next = V_m[t_idx-1] + dV_m
        
        # 5. Check Threshold & Spike
        if v_next >= v_th:
            spikes_x.extend([time[t_idx], time[t_idx], None]) 
            spikes_y.extend([v_th, v_th + 1.5, None]) # Draw a vertical line for spike
            v_next = v_reset # Hard reset
            
        V_m[t_idx] = v_next

    # Slice arrays based on scrubber
    valid_mask = time <= scrub_time
    time_plot = time[valid_mask]
    V_syn_plot = V_syn[:, valid_mask]
    I_plot = I_total[valid_mask]
    V_m_plot = V_m[valid_mask]
    
    # Plotly Subplots
    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True, 
        subplot_titles=[
            'Synaptic Voltages (Exponential Decay)',
            'Accumulated Input Current $I_{total}(t)$', 
            'Neuron Membrane Potential $V_m(t)$ & Spiking'
        ], vertical_spacing=0.1
    )
                        
    colors = ['#e74c3c', '#27ae60', '#2980b9']
    for i in range(3):
        fig.add_trace(go.Scatter(x=time_plot, y=V_syn_plot[i], mode='lines', name=f'Synapse {i+1}', line=dict(color=colors[i], width=2)), row=1, col=1)
        
    fig.add_trace(go.Scatter(x=time_plot, y=I_plot, mode='lines', name='Total Current', line=dict(color='#8e44ad', width=2)), row=2, col=1)
    
    fig.add_trace(go.Scatter(x=time_plot, y=V_m_plot, mode='lines', name='Membrane Potential', line=dict(color='#2c3e50', width=2)), row=3, col=1)
    
    # Only show spike lines if they occur before or at the scrub time
    valid_spikes_x = []
    valid_spikes_y = []
    for i in range(0, len(spikes_x), 3):
        if spikes_x[i] is not None and spikes_x[i] <= scrub_time:
            valid_spikes_x.extend([spikes_x[i], spikes_x[i+1], spikes_x[i+2]])
            valid_spikes_y.extend([spikes_y[i], spikes_y[i+1], spikes_y[i+2]])
            
    if valid_spikes_x:
        fig.add_trace(go.Scatter(x=valid_spikes_x, y=valid_spikes_y, mode='lines', name='Spikes', line=dict(color='#e67e22', width=2)), row=3, col=1)
    
    # Threshold & Resting Reference Lines
    fig.add_hline(y=v_th, line_dash="dash", line_color="#e74c3c", annotation_text="Thresh", row=3, col=1)
    fig.add_hline(y=v_reset, line_dash="solid", line_color="#bdc3c7", line_width=1, row=3, col=1)
    
    # Scrubber Indicator Line
    fig.add_vline(x=scrub_time, line_width=2, line_dash="dot", line_color="rgba(52, 152, 219, 0.5)")
    
    fig.update_layout(
        height=700, margin=dict(l=40, r=40, t=40, b=40),
        hovermode="x unified", title_text="", showlegend=False,
        plot_bgcolor='white', paper_bgcolor='white'
    )
    
    # Axis styling
    fig.update_xaxes(title_text="Time (ms)", range=[0, T_total], showgrid=True, gridcolor='#ecf0f1', row=3, col=1)
    fig.update_xaxes(range=[0, T_total], showgrid=True, gridcolor='#ecf0f1', row=1, col=1)
    fig.update_xaxes(range=[0, T_total], showgrid=True, gridcolor='#ecf0f1', row=2, col=1)
    
    fig.update_yaxes(title_text="mV", range=[0, max(6, np.max(V_syn)+1)], showgrid=True, gridcolor='#ecf0f1', row=1, col=1)
    fig.update_yaxes(title_text="mA", range=[0, max(8, np.max(I_total)+1)], showgrid=True, gridcolor='#ecf0f1', row=2, col=1)
    fig.update_yaxes(title_text="mV", range=[min(-1, np.min(V_m)-0.5), max(v_th+2, np.max(V_m)+0.5)], showgrid=True, gridcolor='#ecf0f1', row=3, col=1)
                        
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
