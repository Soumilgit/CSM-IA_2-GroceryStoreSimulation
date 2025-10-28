# Grocery Store Queue Simulation

A modern, interactive simulation tool that helps grocery stores optimize their checkout operations. Built with Python, SimPy, and Gradio to provide real-time insights into customer flow and wait times.

## Why This Matters

Every grocery store faces the same challenge: how many checkout lanes should be open? Too few lanes mean frustrated customers standing in long lines. Too many lanes mean paying employees who aren't busy enough. This simulator helps answer that question by modeling real-world scenarios with different configurations.

## What It Does

This tool simulates a full grocery store checkout system where you can:

- Set up different types of checkout lanes (regular, express, self-serve)
- Control how many customers arrive and when
- Watch how customers move through the system
- See detailed statistics on wait times and efficiency
- Visualize the results with clear, interactive graphs

The best part? You can test dozens of configurations in minutes instead of running expensive real-world experiments.

## Quick Start

### Getting It Running

1. **Open your terminal in the project folder**

2. **Activate the virtual environment:**
   ```bash
   .\.venv\Scripts\Activate.ps1
   ```

3. **Make sure you have the required packages:**
   ```bash
   pip install simpy gradio matplotlib pandas
   ```

4. **Start the app:**
   ```bash
   python gradio_app_simple.py
   ```

5. **Open your browser** and go to the URL shown in the terminal (usually `http://127.0.0.1:7861`)

That's it! You'll see a web interface where you can adjust all the settings and run simulations.

## How to Use It

### Setting Up Your Simulation

The interface has sliders for everything you need:

**Customer Settings:**
- How many customers to simulate (10 to 500)
- How often they arrive (every 1 to 20 seconds on average)
- How many items they're buying (minimum and maximum)

**Checkout Lane Setup:**
- Regular cashier lanes (slower but handle any number of items)
- Express lanes (faster but only for 7 items or less)
- Self-serve lanes (slowest but customers don't need staff)

### Understanding the Results

After running a simulation, you'll get four views:

1. **Summary Tab** - Plain English breakdown of what happened
2. **Visualizations Tab** - Four graphs showing the data visually
3. **Data Table Tab** - Detailed numbers for each checkout lane
4. **Raw JSON Tab** - All the data if you want to export it

The graphs show:
- Which lanes served the most customers
- How long the queues got
- Customer wait times (minimum, average, maximum)
- How work was distributed across lane types

## The Simulation Logic

### Lane Types

The simulation uses three types of checkout lanes, each with different speeds:

**Regular Cashier Lines**
- Service time: number of items + 7 seconds
- No restrictions on items
- Good all-around choice

**Express Lines**
- Service time: number of items + 4 seconds  
- Only for customers with 7 items or less
- Best for quick transactions

**Self-Serve Lines**
- Service time: (number of items × 2) + 1 seconds
- No restrictions on items
- Cheaper to operate but slower

### How Customers Choose Lines

When a customer arrives, they follow a simple rule: join the shortest line they're allowed to use. If there's a tie, they pick the first available one.

Express lane customers (7 items or less) can choose any line. Everyone else has to skip the express lanes.

### What Gets Tracked

The simulation monitors:
- How long each customer waits before being served
- Total time from arrival to checkout completion
- Queue lengths at each lane over time
- How many customers each lane processes
- When the simulation finishes

## Project Structure

```
├── gradio_app_simple.py    ← Main app (start here)
├── simpy_simulation.py     ← Simulation engine
├── store.py                ← Store and line models
├── event.py                ← Event handling system
├── simulation.py           ← Original simulation logic
├── container.py            ← Priority queue implementation
├── requirements.txt        ← Dependencies list
└── input_files/            ← Sample configurations
```

## Technical Details

### Built With

- **Python 3.9+** - Core programming language
- **SimPy 4.1+** - Discrete-event simulation framework
- **Gradio 4.44+** - Web interface for easy interaction
- **Matplotlib 3.9+** - Graph generation
- **Pandas 2.1+** - Data handling and tables

### The Math Behind Service Times

Each lane type has a formula based on real checkout observations:

- Cashier: Fixed 7 seconds overhead + 1 second per item
- Express: Fixed 4 seconds overhead + 1 second per item  
- Self-serve: Fixed 1 second overhead + 2 seconds per item

These formulas account for scanning, payment processing, and bagging.

## Running Tests

Want to make sure everything works? Run the sample tests:

```bash
python simulation_tests_sample.py
```

Or test just the SimPy backend:

```bash
python simpy_simulation.py
```

## Common Issues

**Port already in use?**  
The app will automatically find an available port. Just check the terminal for the new URL.

**Missing packages?**  
Run: `pip install simpy gradio matplotlib pandas`

**Import errors?**  
Try: `pip install "huggingface_hub<1.0"`

## Example Scenarios

### Quiet Afternoon (Low Traffic)
- 50 customers
- Arrive every 10 seconds
- 1 cashier, 1 express, 1 self-serve
- Result: Minimal wait times, staff underutilized

### Busy Weekend (High Traffic)
- 200 customers
- Arrive every 3 seconds
- 3 cashiers, 2 express, 3 self-serve
- Result: Balanced load, reasonable wait times

### Rush Hour (Peak Traffic)
- 300 customers
- Arrive every 2 seconds
- 4 cashiers, 2 express, 4 self-serve
- Result: High throughput, manageable queues

## Want to Dig Deeper?

The codebase includes both event-driven and process-based simulation approaches:

- `simulation.py` + `event.py` = Classic event-driven model
- `simpy_simulation.py` = Modern SimPy process-based model

The Gradio UI uses the SimPy version because it's more reliable and easier to extend.

## Contributing

Found a bug? Have an idea for improvement? Feel free to:
- Open an issue
- Submit a pull request
- Suggest new features

## License

This project is based on academic coursework and is meant for educational purposes.

## Questions?

Check out `SUMMARY.md` for detailed documentation, or explore the code comments for implementation details.

---

**Happy simulating!** 🛒📊