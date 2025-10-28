# 🛒 Grocery Store Checkout Queue Simulation - Summary

## ✅ Implementation Complete!

This project successfully implements a **Python + SimPy + Gradio** grocery store checkout queue simulation with full visualization capabilities.

---

## 🎯 Requirements Met

✅ **SimPy Backend Logic**: Full discrete-event simulation engine  
✅ **Gradio Web UI**: Interactive interface with sliders and text inputs  
✅ **Graphs & Visualizations**: 4 comprehensive plots showing simulation analytics  
✅ **Localhost Deployment**: Runs on http://127.0.0.1:7860  
✅ **Configurable Parameters**: All key simulation variables are adjustable  

---

## 🚀 Quick Start

### 1. Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies (if needed)
```powershell
pip install simpy gradio matplotlib pandas
```

### 3. Run the Application
```powershell
python gradio_app_simple.py
```

### 4. Access the Web UI
Open your browser and navigate to:
```
http://127.0.0.1:7860
```

---

## 📊 Features

### Interactive Parameters

#### Customer Parameters:
- **Number of Customers** (10-500): Total customers to simulate
- **Arrival Interval** (1-20): Average time between customer arrivals
- **Min Items** (1-10): Minimum items per customer
- **Max Items** (5-50): Maximum items per customer

#### Checkout Line Configuration:
- **Cashier Lines** (0-10): Regular checkout (service time: items + 7)
- **Express Lines** (0-5): For ≤7 items (service time: items + 4)
- **Self-Serve Lines** (0-10): Self-checkout (service time: 2×items + 1)
- **Random Seed**: For reproducible results

### 📈 Visualizations

The app generates **4 comprehensive graphs**:

1. **Customers Served by Each Line** - Bar chart showing customer distribution
2. **Queue Lengths by Line** - Comparison of average vs. maximum queue lengths
3. **Customer Wait Time Distribution** - Min, average, and max wait times
4. **Total Service Time by Line Type** - Pie chart showing workload distribution

### 📋 Output Formats

- **Summary Tab**: Formatted text with detailed statistics
- **Visualizations Tab**: Interactive matplotlib plots
- **Data Table Tab**: Pandas DataFrame with line-by-line statistics
- **Raw JSON Tab**: Complete simulation results in JSON format

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Gradio Web Interface            │
│  (sliders, buttons, visualization)      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│      simpy_simulation.py                │
│   (SimPy discrete-event simulation)     │
├─────────────────────────────────────────┤
│  • GroceryStoreSimPy                    │
│  • CheckoutLine (3 types)               │
│  • Customer                             │
│  • Queue management                     │
│  • Statistics collection                │
└─────────────────────────────────────────┘
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `gradio_app_simple.py` | **Main application** - Optimized Gradio UI |
| `simpy_simulation.py` | **SimPy backend** - Simulation engine |
| `store.py` | Original store models |
| `event.py` | Event-based simulation (original) |
| `simulation.py` | Original simulation logic |
| `container.py` | Priority queue implementation |
| `requirements.txt` | Python dependencies |

---

## 🧪 Testing

### Run Basic Simulation (Command Line)
```powershell
python simpy_simulation.py
```

Expected output:
```
Running Grocery Store Simulation with SimPy...
============================================================

Simulation Results:
Total Customers: 100
Completed: 100
Average Wait Time: 38.61 units
Maximum Wait Time: 95.88 units
...
```

### Run Original Tests
```powershell
python simulation_tests_sample.py
```

---

## 🔧 Technical Details

### Dependencies
- **simpy** (4.1.1+): Discrete-event simulation framework
- **gradio** (4.44.1+): Web UI framework
- **matplotlib** (3.9.4+): Plotting and visualization
- **pandas** (2.1.3+): Data manipulation and tables

### Simulation Logic

#### Checkout Line Types:
1. **Cashier Lines**: Service time = `items + 7`
2. **Express Lines**: Service time = `items + 4` (≤7 items only)
3. **Self-Serve Lines**: Service time = `2 × items + 1`

#### Queue Assignment:
- Customers join the shortest eligible queue
- Express lines only accept customers with ≤7 items
- Smart load balancing across all available lines

#### Statistics Tracked:
- Wait time (time in queue before service)
- Total time (arrival to completion)
- Queue lengths (average and maximum)
- Service times per line
- Customers served per line

---

## 💡 Usage Examples

### Example 1: Balanced Configuration
- Customers: 100
- Arrival Interval: 5
- Cashier Lines: 2
- Express Lines: 1
- Self-Serve Lines: 2

**Result**: Balanced workload, ~38 avg wait time

### Example 2: High Traffic
- Customers: 200
- Arrival Interval: 3
- Cashier Lines: 3
- Express Lines: 2
- Self-Serve Lines: 3

**Result**: More lines handle increased traffic

### Example 3: Peak Hours
- Customers: 150
- Arrival Interval: 2
- Cashier Lines: 4
- Express Lines: 0
- Self-Serve Lines: 4

**Result**: High capacity configuration

---

## 🐛 Troubleshooting

### Issue: Import Errors
**Solution**: Ensure all dependencies are installed
```powershell
pip install simpy gradio matplotlib pandas
pip install "huggingface_hub<1.0"  # If needed
```

### Issue: Port Already in Use
**Solution**: Change port in `gradio_app_simple.py`:
```python
demo.launch(server_name="127.0.0.1", server_port=7861, share=False)
```

### Issue: Gradio Won't Start
**Solution**: Use the simple version:
```powershell
python gradio_app_simple.py
```

---

## 📝 Code Fixes Applied

1. **store.py**: Fixed missing closing parenthesis (line 50)
2. **store.py**: Fixed typo "reuturn" → "return" (line 97)
3. **store.py**: Added missing imports for PriorityQueue
4. **event.py**: Fixed bracket to parenthesis in append call (line 198)
5. **simulation.py**: Added missing event class imports
6. **simulation.py**: Fixed event.do() method calls
7. **simpy_simulation.py**: Added max_recordings limit to prevent memory issues

---

## 🎉 Success Criteria

✅ SimPy simulation runs without errors  
✅ Gradio UI launches on localhost:7860  
✅ All 4 graphs render correctly  
✅ Simulation parameters are adjustable via sliders  
✅ Results display in multiple formats (text, graph, table, JSON)  
✅ Statistics are accurate and comprehensive  
✅ MVP is fully functional and production-ready  

---

## 🔮 Future Enhancements

- [ ] Add real-time simulation animation
- [ ] Export results to CSV/PDF
- [ ] Historical comparison of multiple runs
- [ ] Advanced scheduling algorithms
- [ ] Customer priority levels
- [ ] Line closure events
- [ ] Mobile-responsive design

---

## 📚 References

- **SimPy Documentation**: https://simpy.readthedocs.io/
- **Gradio Documentation**: https://gradio.app/docs/
- **Original Repository**: Shuso/csc148assginment1_grocery_store_simulation

---

## 👨‍💻 Development Notes

**Version**: 1.0.0  
**Date**: October 28, 2025  
**Python Version**: 3.9+  
**Status**: ✅ Production Ready

---

**Enjoy simulating! 🛒📊**
