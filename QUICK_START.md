# 🚀 Quick Start Guide

## Installation & Setup

### Step 1: Install Dependencies

Open your terminal/PowerShell in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- `simpy` - Discrete event simulation framework
- `gradio` - Interactive web UI
- `pandas` - Data analysis
- `matplotlib` - Visualizations
- `numpy` - Numerical operations

### Step 2: Test the Installation

Run the test suite to ensure everything is working:

```bash
python test_simulation.py
```

You should see all tests passing with a success message.

### Step 3: Launch the Gradio UI

Start the interactive web interface:

```bash
python gradio_app.py
```

Open your browser to: **http://127.0.0.1:7860**

## Using the Web Interface

### Basic Usage

1. **Adjust Parameters**: Use the sliders on the left to configure your simulation
   - Number of customers
   - Arrival interval (time between customers)
   - Number of each line type
   - Item count range

2. **Run Simulation**: Click the "🚀 Run Simulation" button

3. **View Results**: Check the tabs on the right:
   - **Summary**: Text-based detailed results
   - **Visualizations**: Charts and graphs
   - **Data Table**: Structured data view
   - **Raw JSON**: Complete data export

### Example Scenarios

Try these pre-configured examples:

#### Busy Store (Peak Hours)
- Customers: 200
- Arrival Interval: 3.0
- Cashier Lines: 3
- Express Lines: 2
- Self-Serve Lines: 3

#### Small Store (Off-Peak)
- Customers: 50
- Arrival Interval: 10.0
- Cashier Lines: 1
- Express Lines: 1
- Self-Serve Lines: 1

#### Express Lane Test
- Customers: 150
- Arrival Interval: 4.0
- Cashier Lines: 2
- Express Lines: 2
- Self-Serve Lines: 2

## Command Line Usage

You can also run simulations from Python code:

```python
from simpy_simulation import run_simulation_wrapper

# Run a simulation
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

# Print results
print(f"Average Wait Time: {results['avg_wait_time']}")
print(f"Max Wait Time: {results['max_wait_time']}")

# Access line statistics
for line in results['line_stats']:
    print(f"Line {line['line_id']} ({line['line_type']}): "
          f"{line['customers_served']} customers served")
```

## Understanding the Output

### Key Metrics Explained

- **Total Customers**: Number of customers simulated
- **Completed Customers**: Customers who finished checkout
- **Average Wait Time**: Mean time spent waiting in queue
- **Maximum Wait Time**: Longest wait experienced
- **Total Time in System**: From arrival to completion
- **Queue Length**: Number of people waiting in line
- **Service Time**: Time spent being served

### Interpreting Results

**Good Performance Indicators:**
- Low average wait times (< 10 time units)
- Small difference between min and max wait
- Balanced customer distribution across lines
- All customers completed service

**Performance Issues:**
- High maximum wait times (> 50 time units)
- Large variance in wait times
- Very uneven line utilization
- Long queue lengths

## Troubleshooting

### Common Issues

**Problem**: `ModuleNotFoundError: No module named 'simpy'`
```bash
# Solution: Install requirements
pip install -r requirements.txt
```

**Problem**: Gradio window won't open
```bash
# Solution: Check the console for the URL and open it manually
# Should be: http://127.0.0.1:7860
```

**Problem**: Simulation is slow
```bash
# Solution: Reduce the number of customers
# Start with 50-100 for quick tests
# Use 200+ for detailed analysis
```

**Problem**: Import errors
```bash
# Solution: Make sure you're in the correct directory
cd csc148assginment1_grocery_store_simulation-master
python gradio_app.py
```

## Next Steps

### Experiment with Parameters

Try answering these questions:
1. How many checkout lines minimize wait time for 100 customers?
2. Is it better to have more cashier or self-serve lines?
3. What's the optimal express line count?
4. How does arrival rate affect queue lengths?

### Advanced Usage

1. **Modify Service Times**: Edit `simpy_simulation.py` to change checkout speeds
2. **Add New Line Types**: Extend the `CheckoutLine` class
3. **Custom Visualizations**: Update `gradio_app.py` with new charts
4. **Export Data**: Use the JSON tab to save results for analysis

### Compare Configurations

Run multiple simulations with the same random seed to compare:

```python
# Configuration A
results_a = run_simulation_wrapper(
    num_customers=100,
    num_cashier=3,
    num_express=1,
    num_self_serve=2,
    random_seed=42  # Same seed!
)

# Configuration B
results_b = run_simulation_wrapper(
    num_customers=100,
    num_cashier=2,
    num_express=2,
    num_self_serve=2,
    random_seed=42  # Same seed!
)

# Compare
print(f"Config A wait: {results_a['avg_wait_time']}")
print(f"Config B wait: {results_b['avg_wait_time']}")
```

## Tips for Best Results

1. **Use Consistent Seeds**: Set the same random seed for fair comparisons
2. **Run Multiple Times**: Average results from several runs
3. **Start Small**: Test with 50-100 customers first
4. **Monitor Queue Lengths**: High queues indicate bottlenecks
5. **Check All Tabs**: Different views reveal different insights

## Getting Help

- Check `README_ENHANCED.md` for detailed documentation
- Review `test_simulation.py` for code examples
- Examine `simpy_simulation.py` to understand the simulation logic
- Explore `gradio_app.py` to see UI implementation

## Have Fun! 🎉

This simulation is a powerful tool for understanding queue dynamics and optimization. Experiment freely and discover what works best for different scenarios!
