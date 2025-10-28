"""Simple Gradio UI for Grocery Store Simulation - Optimized Version"""

import gradio as gr
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import json
from simpy_simulation import run_simulation_wrapper


def format_results_as_text(results):
    """Format simulation results as readable text."""
    output = []
    output.append("=" * 60)
    output.append("GROCERY STORE SIMULATION RESULTS")
    output.append("=" * 60)
    output.append("")
    
    output.append("📊 OVERALL STATISTICS")
    output.append("-" * 60)
    output.append(f"Total Customers Simulated: {results['total_customers']}")
    output.append(f"Customers Completed: {results['completed_customers']}")
    output.append(f"Simulation Duration: {results['simulation_end_time']} time units")
    output.append("")
    
    output.append("⏱️  CUSTOMER WAIT TIMES")
    output.append("-" * 60)
    output.append(f"Average Wait Time: {results['avg_wait_time']} time units")
    output.append(f"Minimum Wait Time: {results['min_wait_time']} time units")
    output.append(f"Maximum Wait Time: {results['max_wait_time']} time units")
    output.append("")
    
    output.append("🕐 TOTAL TIME IN SYSTEM")
    output.append("-" * 60)
    output.append(f"Average Total Time: {results['avg_total_time']} time units")
    output.append(f"Minimum Total Time: {results['min_total_time']} time units")
    output.append(f"Maximum Total Time: {results['max_total_time']} time units")
    output.append("")
    
    output.append("🏪 CHECKOUT LINE STATISTICS")
    output.append("-" * 60)
    
    for line_stat in results['line_stats']:
        line_type_emoji = {
            'cashier': '👨‍💼',
            'express': '⚡',
            'self_serve': '🤖'
        }
        emoji = line_type_emoji.get(line_stat['line_type'], '📦')
        
        output.append(f"\n{emoji} Line {line_stat['line_id']} - {line_stat['line_type'].upper()}")
        output.append(f"   Customers Served: {line_stat['customers_served']}")
        output.append(f"   Average Queue Length: {line_stat['avg_queue_length']}")
        output.append(f"   Maximum Queue Length: {line_stat['max_queue_length']}")
        output.append(f"   Total Service Time: {line_stat['total_service_time']} time units")
    
    output.append("")
    output.append("=" * 60)
    
    return "\n".join(output)


def create_visualization(results):
    """Create visualization plots from simulation results."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Grocery Store Simulation Analysis', fontsize=16, fontweight='bold')
    
    # Extract line statistics
    line_stats = results['line_stats']
    line_labels = [f"{stat['line_type']}\n(Line {stat['line_id']})" 
                   for stat in line_stats]
    
    # Plot 1: Customers Served by Line
    customers_served = [stat['customers_served'] for stat in line_stats]
    colors_served = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    axes[0, 0].bar(range(len(line_labels)), customers_served, 
                   color=colors_served[:len(line_labels)])
    axes[0, 0].set_xlabel('Checkout Line', fontweight='bold')
    axes[0, 0].set_ylabel('Customers Served', fontweight='bold')
    axes[0, 0].set_title('Customers Served by Each Line')
    axes[0, 0].set_xticks(range(len(line_labels)))
    axes[0, 0].set_xticklabels(line_labels, fontsize=8)
    axes[0, 0].grid(axis='y', alpha=0.3)
    
    # Plot 2: Average Queue Length
    avg_queue = [stat['avg_queue_length'] for stat in line_stats]
    max_queue = [stat['max_queue_length'] for stat in line_stats]
    
    x = range(len(line_labels))
    width = 0.35
    axes[0, 1].bar([i - width/2 for i in x], avg_queue, width, 
                   label='Average', color='#3498db', alpha=0.8)
    axes[0, 1].bar([i + width/2 for i in x], max_queue, width, 
                   label='Maximum', color='#e74c3c', alpha=0.8)
    axes[0, 1].set_xlabel('Checkout Line', fontweight='bold')
    axes[0, 1].set_ylabel('Queue Length', fontweight='bold')
    axes[0, 1].set_title('Queue Lengths by Line')
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(line_labels, fontsize=8)
    axes[0, 1].legend()
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Plot 3: Wait Time Distribution
    wait_times = ['Min Wait', 'Avg Wait', 'Max Wait']
    wait_values = [
        results['min_wait_time'],
        results['avg_wait_time'],
        results['max_wait_time']
    ]
    colors_wait = ['#2ecc71', '#f39c12', '#e74c3c']
    bars = axes[1, 0].bar(wait_times, wait_values, color=colors_wait, alpha=0.8)
    axes[1, 0].set_ylabel('Time Units', fontweight='bold')
    axes[1, 0].set_title('Customer Wait Time Distribution')
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}',
                       ha='center', va='bottom', fontweight='bold')
    
    # Plot 4: Total Service Time by Line Type
    line_types = {}
    for stat in line_stats:
        line_type = stat['line_type']
        if line_type not in line_types:
            line_types[line_type] = 0
        line_types[line_type] += stat['total_service_time']
    
    type_labels = list(line_types.keys())
    type_values = list(line_types.values())
    colors_pie = ['#3498db', '#e74c3c', '#2ecc71']
    
    axes[1, 1].pie(type_values, labels=type_labels, autopct='%1.1f%%',
                   colors=colors_pie[:len(type_labels)], startangle=90)
    axes[1, 1].set_title('Total Service Time by Line Type')
    
    plt.tight_layout()
    return fig


def run_simulation_ui(num_customers, arrival_interval, num_cashier, 
                     num_express, num_self_serve, min_items, max_items, 
                     random_seed):
    """Run simulation and return formatted results for Gradio UI."""
    try:
        # Run the simulation
        results = run_simulation_wrapper(
            num_customers=int(num_customers),
            arrival_interval=float(arrival_interval),
            num_cashier=int(num_cashier),
            num_express=int(num_express),
            num_self_serve=int(num_self_serve),
            min_items=int(min_items),
            max_items=int(max_items),
            random_seed=int(random_seed) if random_seed else None
        )
        
        # Format results
        text_output = format_results_as_text(results)
        plot = create_visualization(results)
        
        # Create dataframe for table
        df = pd.DataFrame(results['line_stats'])
        df = df.rename(columns={
            'line_id': 'Line ID',
            'line_type': 'Line Type',
            'customers_served': 'Customers Served',
            'avg_queue_length': 'Avg Queue Length',
            'max_queue_length': 'Max Queue Length',
            'total_service_time': 'Total Service Time'
        })
        df['Line Type'] = df['Line Type'].str.replace('_', ' ').str.title()
        
        json_output = json.dumps(results, indent=2)
        
        return text_output, plot, df, json_output
        
    except Exception as e:
        error_msg = f"Error running simulation: {str(e)}"
        return error_msg, None, None, error_msg


# Create the interface
with gr.Blocks(title="Grocery Store Simulation") as demo:
    gr.Markdown(
        """
        # 🛒 Grocery Store Checkout Queue Simulation
        
        This interactive simulation models customer flow through a grocery store checkout system.
        Adjust the parameters below to see how different configurations affect wait times and efficiency.
        
        **Built with:** SimPy (Discrete Event Simulation) + Gradio (Interactive UI)
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 👥 Customer Parameters")
            
            num_customers = gr.Slider(10, 500, value=100, step=10, label="Number of Customers")
            arrival_interval = gr.Slider(1, 20, value=5, step=0.5, label="Arrival Interval (time units)")
            min_items = gr.Slider(1, 10, value=1, step=1, label="Minimum Items per Customer")
            max_items = gr.Slider(5, 50, value=20, step=1, label="Maximum Items per Customer")
            
            gr.Markdown("### 🏪 Checkout Line Configuration")
            
            num_cashier = gr.Slider(0, 10, value=2, step=1, label="Number of Cashier Lines")
            num_express = gr.Slider(0, 5, value=1, step=1, label="Number of Express Lines")
            num_self_serve = gr.Slider(0, 10, value=2, step=1, label="Number of Self-Serve Lines")
            random_seed = gr.Number(value=42, label="Random Seed")
            
            run_btn = gr.Button("🚀 Run Simulation", variant="primary", size="lg")
        
        with gr.Column(scale=2):
            gr.Markdown("### 📊 Simulation Results")
            
            with gr.Tab("Summary"):
                text_output = gr.Textbox(label="Detailed Results", lines=25, max_lines=30)
            
            with gr.Tab("Visualizations"):
                plot_output = gr.Plot(label="Analysis Charts")
            
            with gr.Tab("Data Table"):
                table_output = gr.Dataframe(label="Line Statistics", wrap=True)
            
            with gr.Tab("Raw JSON"):
                json_output = gr.Code(label="Raw JSON Output", language="json", lines=20)
    
    # Connect button
    run_btn.click(
        fn=run_simulation_ui,
        inputs=[num_customers, arrival_interval, num_cashier, 
               num_express, num_self_serve, min_items, max_items, random_seed],
        outputs=[text_output, plot_output, table_output, json_output]
    )

# Launch
if __name__ == "__main__":
    print("Starting Gradio app...")
    print("Trying to find an available port...")
    demo.launch(server_name="127.0.0.1", server_port=None, share=False)
