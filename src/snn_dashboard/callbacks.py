import dash
from dash import Input, Output, State, MATCH, ALL
import numpy as np

from .app_instance import app
from .components import BTN_STYLE_0, BTN_STYLE_1
from .simulation import compute_simulation_figure

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
        text = "⏸ Pause Sequence" if new_state else "▶ Play Sequence"
        style = style_pause if new_state else style_play
        return (not new_state), new_state, text, style
        
    elif trigger_id == 'reset-btn':
        return True, False, "▶ Play Sequence", style_play
        
    elif trigger_id == 'time-scrubber':
        if curr_time >= 120 and is_playing:
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
        new_time = current_time + 1.0
        if new_time > 120:
            return 120
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
    spike_matrix = np.zeros((3, 13))
    ctx = dash.callback_context
    try:
        if matrix_vals:
            for idx, (row, col) in enumerate([(r, c) for r in range(3) for c in range(13)]):
                if idx < len(matrix_vals):
                    val = matrix_vals[idx]
                    if val is not None:
                        spike_matrix[row, col] = int(val)
    except (ValueError, TypeError, IndexError):
        pass
        
    weights = [w0, w1, w2]
    taus = [t0, t1, t2]
    
    return compute_simulation_figure(spike_matrix, scrub_time, weights, taus, tau_m, v_th)
