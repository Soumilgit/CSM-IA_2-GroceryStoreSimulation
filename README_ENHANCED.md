# 🛒 Grocery Store Checkout Queue Simulation

A comprehensive grocery store checkout simulation featuring both traditional event-driven and modern SimPy discrete event simulation approaches, with an interactive Gradio web interface.

## 🌟 Features

### Enhanced SimPy Implementation
- **Modern Discrete Event Simulation**: Built with SimPy for realistic queue modeling
- **Multiple Checkout Types**: 
  - 👨‍💼 Cashier Lines (service time: items + 7)
  - ⚡ Express Lines (≤7 items, service time: items + 4)
  - 🤖 Self-Serve Lines (service time: 2×items + 1)
- **Intelligent Customer Routing**: Automatic assignment to shortest eligible queue
- **Comprehensive Statistics**: Wait times, queue lengths, service times, and more

### Interactive Gradio UI
- **Real-time Parameter Adjustment**: Sliders for all simulation parameters
- **Multiple View Modes**: Summary, visualizations, data tables, and raw JSON
- **Beautiful Visualizations**: 
  - Customers served per line
  - Queue length analysis
  - Wait time distribution
  - Service time breakdown by line type
- **Example Configurations**: Pre-configured scenarios for quick testing

### Original Implementation
The original event-driven simulation is preserved for reference and compatibility.

## 🚀 Quick Start

### Installation

1. **Clone or navigate to the repository**:
```bash
cd csc148assginment1_grocery_store_simulation-master
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Simulation

#### Option 1: Gradio Web Interface (Recommended)
```bash
python gradio_app.py
```

Then open your browser to `http://127.0.0.1:7860`

#### Option 2: Command Line (SimPy)
```python
from simpy_simulation import run_simulation_wrapper

results = run_simulation_wrapper(
    num_customers=100,
    arrival_interval=5.0,
    num_cashier=2,
    num_express=1,
    num_self_serve=2,
    min_items=1,
    max_items=20,
    random_seed=42
)

print(results)
```

#### Option 3: Original Implementation
```bash
python simulation.py
```

## 📊 Understanding the Simulation

### Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| **Number of Customers** | Total customers to simulate | 100 | 10-500 |
| **Arrival Interval** | Avg time between arrivals (time units) | 5.0 | 1-20 |
| **Cashier Lines** | Regular checkout counters | 2 | 0-10 |
| **Express Lines** | Fast lanes for ≤7 items | 1 | 0-5 |
| **Self-Serve Lines** | Self-checkout stations | 2 | 0-10 |
| **Min Items** | Minimum items per customer | 1 | 1-10 |
| **Max Items** | Maximum items per customer | 20 | 5-50 |
| **Random Seed** | For reproducible results | 42 | Any integer |

### Service Time Formulas

- **Cashier Line**: `service_time = num_items + 7`
- **Express Line**: `service_time = num_items + 4` (only accepts ≤7 items)
- **Self-Serve Line**: `service_time = 2 × num_items + 1`

### Key Metrics

- **Wait Time**: Time spent in queue before service begins
- **Total Time**: Complete time from arrival to service completion
- **Queue Length**: Number of customers waiting in line
- **Customers Served**: Total processed by each line
- **Service Time**: Time spent being served at checkout

## 🏗️ Project Structure

```
csc148assginment1_grocery_store_simulation-master/
├── simpy_simulation.py      # NEW: SimPy-based simulation engine
├── gradio_app.py            # NEW: Gradio web interface
├── requirements.txt         # NEW: Python dependencies
├── README_ENHANCED.md       # NEW: Comprehensive documentation
│
├── simulation.py            # Original event-driven simulation
├── store.py                 # Original store models
├── event.py                 # Original event classes
├── container.py             # Priority queue implementation
├── line.py                  # Checkout line classes
├── config.json              # Store configuration
├── events.txt               # Sample events
│
└── input_files/             # Sample configuration files
    ├── config_001_10.json
    ├── config_010_10.json
    ├── config_100_10.json
    ├── config_111_10.json
    ├── events_one.txt
    ├── events_one_close.txt
    └── events_two.txt
```

## 💡 Usage Examples

### Example 1: Peak Hour Simulation
Simulate a busy period with many customers and limited checkout lines:

```python
results = run_simulation_wrapper(
    num_customers=200,
    arrival_interval=3.0,  # Customers arrive frequently
    num_cashier=3,
    num_express=2,
    num_self_serve=3,
    min_items=1,
    max_items=15,
    random_seed=42
)
```

### Example 2: Off-Peak Hours
Simulate quiet periods with fewer customers:

```python
results = run_simulation_wrapper(
    num_customers=50,
    arrival_interval=10.0,  # Customers arrive slowly
    num_cashier=1,
    num_express=1,
    num_self_serve=1,
    min_items=1,
    max_items=30,
    random_seed=42
)
```

### Example 3: Express Lane Analysis
Test the impact of express lanes:

```python
# Without express lanes
results_no_express = run_simulation_wrapper(
    num_customers=150,
    arrival_interval=4.0,
    num_cashier=4,
    num_express=0,
    num_self_serve=2,
    min_items=1,
    max_items=20,
    random_seed=42
)

# With express lanes
results_with_express = run_simulation_wrapper(
    num_customers=150,
    arrival_interval=4.0,
    num_cashier=2,
    num_express=2,
    num_self_serve=2,
    min_items=1,
    max_items=20,
    random_seed=42
)
```

## 🎯 Use Cases

1. **Retail Planning**: Optimize checkout line configuration
2. **Capacity Planning**: Determine staffing needs for different traffic levels
3. **Customer Experience**: Analyze wait times and queue lengths
4. **Education**: Learn discrete event simulation concepts
5. **Research**: Test queueing theory hypotheses

## 🔧 Advanced Configuration

### Custom Line Configurations

You can create specialized configurations by modifying the `simpy_simulation.py`:

```python
# Create a store with custom configuration
from simpy_simulation import GroceryStoreSimPy

store = GroceryStoreSimPy(
    num_cashier_lines=3,
    num_express_lines=2,
    num_self_serve_lines=4
)

results = store.run_simulation(
    num_customers=100,
    arrival_interval=5.0,
    min_items=1,
    max_items=20,
    random_seed=42
)
```

### Extending the Simulation

To add new features:

1. **New Line Types**: Extend the `CheckoutLine` class in `simpy_simulation.py`
2. **Custom Statistics**: Modify the `calculate_statistics()` method
3. **UI Enhancements**: Update `gradio_app.py` with new components

## 📈 Performance Tips

- Use random seeds for reproducible experiments
- Start with smaller customer counts (50-100) for quick iterations
- Increase customers to 500+ for statistically significant results
- Monitor queue lengths to identify bottlenecks
- Compare configurations side-by-side using the same random seed

## 🐛 Troubleshooting

### Common Issues

**Issue**: Gradio won't start
```bash
# Solution: Ensure all dependencies are installed
pip install --upgrade -r requirements.txt
```

**Issue**: Simulation runs slowly
```bash
# Solution: Reduce number of customers or increase arrival interval
# Large simulations (500+ customers) may take a few seconds
```

**Issue**: Import errors
```bash
# Solution: Make sure you're in the correct directory
cd csc148assginment1_grocery_store_simulation-master
python gradio_app.py
```

## 🤝 Contributing

This project enhances the original CSC148 assignment. Feel free to:
- Add new visualization types
- Implement additional statistics
- Create new queue routing algorithms
- Improve the UI/UX

## 📚 Technical Details

### Technologies Used
- **SimPy**: Discrete event simulation framework
- **Gradio**: Web UI framework for ML/data science apps
- **Matplotlib**: Visualization library
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing

### Simulation Approach
The SimPy implementation uses:
- **Resource-based queuing**: Each line is a SimPy Resource
- **Process-based modeling**: Customers are simulated as processes
- **Exponential arrivals**: Realistic customer arrival patterns
- **Priority-based routing**: Shortest queue selection

## 📝 Original Assignment

This project is based on a CSC148 course assignment. The original assignment description can be found in `README.md`. This enhanced version adds:

- Modern SimPy discrete event simulation
- Interactive Gradio web interface
- Advanced visualizations
- Comprehensive statistics
- Easy-to-use parameter controls

## 👏 Acknowledgments

- Original assignment structure from CSC148 course
- SimPy documentation and examples
- Gradio official repository patterns
- Queueing theory principles

---

**Built with ❤️ using Python, SimPy, and Gradio**
