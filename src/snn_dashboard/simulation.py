import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def compute_simulation_figure(spike_matrix, scrub_time, weights, taus, tau_m, v_th):
    # Simulation Settings
    dt = 0.5  # ms precision
    T_total = 120.0 # ms simulation time (increased for better viewing)
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
            # avoid index errors
            if col < spike_matrix.shape[1]: 
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
            'Accumulated Total Input Current', 
            'Neuron Membrane Potential & Spiking'
        ], vertical_spacing=0.1
    )
    colors = ['#e74c3c', '#27ae60', '#2980b9']
    
    # 1. Overlay background pulses for active synapses
    for c in range(5):
        pulse_time = c * step_duration
        if pulse_time <= scrub_time:
            for r in range(3):
                if spike_matrix[r, c] == 1:
                    # Draw a semi-transparent vertical bar for the pulse
                    fig.add_shape(
                        type="rect", xref="x", yref="y",
                        x0=pulse_time-0.5, y0=0, x1=pulse_time+0.5, y1=weights[r],
                        fillcolor=colors[r], opacity=0.3, line_width=0, row=1, col=1
                    )
    
    # 2. Add traces
    for i in range(3):
        fig.add_trace(go.Scatter(x=time_plot, y=V_syn_plot[i], mode='lines', name=f'Synapse {i+1}', line=dict(color=colors[i], width=2)), row=1, col=1)
        
    # Fill the area under the total current curve to emphasize linear accumulation
    fig.add_trace(go.Scatter(x=time_plot, y=I_plot, mode='lines', name='Total Current', fill='tozeroy', fillcolor='rgba(142, 68, 173, 0.2)', line=dict(color='#8e44ad', width=2)), row=2, col=1)
    
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
