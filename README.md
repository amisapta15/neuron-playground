# Neuron Playground 🧠

Interactive Plotly Dash WebApp for simulating and visualizing **Spiking Neural Network (SNN)** integration and **Leaky Integrate-and-Fire (LIF)** neuron dynamics. 

This educational dashboard allows you to experiment with synaptic inputs, weights, time constants, and neuron membrane properties to see how they affect action potential firing in real-time.

## Features ✨

- **Interactive Spike Matrix**: Click to toggle input spikes across 3 different synapses (channels) over time.
- **Adjustable Synapse Parameters**: Control the weight and time constant (decay) for each independent synapse.
- **Customizable LIF Neuron**: Fine-tune the Membrane Time Constant ($\tau_m$) and Firing Threshold ($V_{th}$).
- **Real-time Playback**: Watch the sequence play out incrementally with built-in playback controls and a time scrubber.
- **Dynamic Visualizations**: 
  - Synaptic Voltages (Exponential Decay)
  - Accumulated Total Input Current ($\sum I_{syn}(t)$)
  - Neuron Membrane Potential ($V_m(t)$) & Spiking events

## Prerequisites 📋

Ensure you have Python 3.8+ installed on your system.

## Installation & Setup 🚀

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/your-username/neuron-playground.git
   cd neuron-playground
   ```

2. **Create a virtual environment (Recommended)**:
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard 🏃‍♂️

Start the application by running the main entry point:

```bash
python app.py
```

The application will launch a local server. Open your web browser and navigate to:
**http://127.0.0.1:8050**

## Project Structure 📁

- `app.py`: Main entry point for the Dash application.
- `requirements.txt`: Python package dependencies.
- `src/snn_dashboard/`: Application source code.
  - `components.py`: Defines the UI layout, sliders, and playback controls.
  - `callbacks.py`: Contains the interactive logic linking UI inputs to the simulation.
  - `app_instance.py`: Initializes the Dash app instance.
  - `simulation.py`: Core mathematical simulation for LIF neuron dynamics and Plotly figure generation.

## License 📜

Please refer to the `LICENSE` file in the repository for more details.