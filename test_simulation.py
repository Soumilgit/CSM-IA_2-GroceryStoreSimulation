"""
Test script for the enhanced grocery store simulation

This script tests both the SimPy simulation and verifies basic functionality.
"""

from simpy_simulation import run_simulation_wrapper, GroceryStoreSimPy


def test_basic_simulation():
    """Test basic simulation functionality."""
    print("=" * 70)
    print("Testing Basic Simulation")
    print("=" * 70)
    
    results = run_simulation_wrapper(
        num_customers=50,
        arrival_interval=5.0,
        num_cashier=2,
        num_express=1,
        num_self_serve=2,
        min_items=1,
        max_items=20,
        random_seed=42
    )
    
    print(f"\n✓ Simulation completed successfully!")
    print(f"  Total Customers: {results['total_customers']}")
    print(f"  Completed: {results['completed_customers']}")
    print(f"  Average Wait: {results['avg_wait_time']} time units")
    print(f"  Max Wait: {results['max_wait_time']} time units")
    
    assert results['total_customers'] == 50, "Customer count mismatch"
    assert results['completed_customers'] > 0, "No customers completed"
    assert 'line_stats' in results, "Missing line statistics"
    
    print("\n✓ All assertions passed!")
    return True


def test_different_configurations():
    """Test various store configurations."""
    print("\n" + "=" * 70)
    print("Testing Different Configurations")
    print("=" * 70)
    
    configs = [
        {"name": "Small Store", "cashier": 1, "express": 1, "self_serve": 1},
        {"name": "Medium Store", "cashier": 2, "express": 1, "self_serve": 2},
        {"name": "Large Store", "cashier": 4, "express": 2, "self_serve": 4},
        {"name": "No Express", "cashier": 3, "express": 0, "self_serve": 2},
        {"name": "Self-Serve Only", "cashier": 0, "express": 0, "self_serve": 5},
    ]
    
    for config in configs:
        print(f"\n  Testing: {config['name']}")
        
        results = run_simulation_wrapper(
            num_customers=30,
            arrival_interval=5.0,
            num_cashier=config['cashier'],
            num_express=config['express'],
            num_self_serve=config['self_serve'],
            min_items=1,
            max_items=15,
            random_seed=42
        )
        
        total_lines = config['cashier'] + config['express'] + config['self_serve']
        print(f"    Lines: {total_lines} | Avg Wait: {results['avg_wait_time']} | "
              f"Completed: {results['completed_customers']}")
        
        assert len(results['line_stats']) == total_lines, \
            f"Line count mismatch for {config['name']}"
    
    print("\n✓ All configuration tests passed!")
    return True


def test_peak_vs_offpeak():
    """Compare peak and off-peak scenarios."""
    print("\n" + "=" * 70)
    print("Testing Peak vs Off-Peak Hours")
    print("=" * 70)
    
    # Peak hours - many customers, fast arrivals
    print("\n  Running Peak Hours Simulation...")
    peak_results = run_simulation_wrapper(
        num_customers=100,
        arrival_interval=2.0,  # Fast arrivals
        num_cashier=2,
        num_express=1,
        num_self_serve=2,
        min_items=1,
        max_items=15,
        random_seed=42
    )
    
    # Off-peak hours - fewer customers, slow arrivals
    print("  Running Off-Peak Hours Simulation...")
    offpeak_results = run_simulation_wrapper(
        num_customers=50,
        arrival_interval=10.0,  # Slow arrivals
        num_cashier=2,
        num_express=1,
        num_self_serve=2,
        min_items=1,
        max_items=15,
        random_seed=42
    )
    
    print(f"\n  Peak Hours:")
    print(f"    Avg Wait: {peak_results['avg_wait_time']} | "
          f"Max Wait: {peak_results['max_wait_time']}")
    
    print(f"  Off-Peak Hours:")
    print(f"    Avg Wait: {offpeak_results['avg_wait_time']} | "
          f"Max Wait: {offpeak_results['max_wait_time']}")
    
    # Peak hours should generally have longer waits
    print(f"\n  Peak hours avg wait is "
          f"{peak_results['avg_wait_time'] / max(offpeak_results['avg_wait_time'], 0.1):.1f}x "
          f"off-peak")
    
    print("\n✓ Peak vs off-peak comparison completed!")
    return True


def test_express_lane_effectiveness():
    """Test the effectiveness of express lanes."""
    print("\n" + "=" * 70)
    print("Testing Express Lane Effectiveness")
    print("=" * 70)
    
    # With express lanes
    print("\n  Running simulation WITH express lanes...")
    with_express = run_simulation_wrapper(
        num_customers=100,
        arrival_interval=4.0,
        num_cashier=2,
        num_express=2,
        num_self_serve=2,
        min_items=1,
        max_items=20,
        random_seed=42
    )
    
    # Without express lanes (same total lines)
    print("  Running simulation WITHOUT express lanes...")
    without_express = run_simulation_wrapper(
        num_customers=100,
        arrival_interval=4.0,
        num_cashier=4,
        num_express=0,
        num_self_serve=2,
        min_items=1,
        max_items=20,
        random_seed=42
    )
    
    print(f"\n  With Express Lanes:")
    print(f"    Avg Wait: {with_express['avg_wait_time']} | "
          f"Max Wait: {with_express['max_wait_time']}")
    
    print(f"  Without Express Lanes:")
    print(f"    Avg Wait: {without_express['avg_wait_time']} | "
          f"Max Wait: {without_express['max_wait_time']}")
    
    diff = without_express['avg_wait_time'] - with_express['avg_wait_time']
    if diff > 0:
        print(f"\n  ✓ Express lanes reduced average wait by {diff:.2f} time units!")
    elif diff < 0:
        print(f"\n  ℹ Express lanes increased wait by {abs(diff):.2f} time units "
              f"(configuration-dependent)")
    else:
        print(f"\n  ℹ No difference in wait times")
    
    print("\n✓ Express lane analysis completed!")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "GROCERY STORE SIMULATION TEST SUITE" + " " * 17 + "║")
    print("╚" + "=" * 68 + "╝")
    
    tests = [
        ("Basic Simulation", test_basic_simulation),
        ("Different Configurations", test_different_configurations),
        ("Peak vs Off-Peak", test_peak_vs_offpeak),
        ("Express Lane Effectiveness", test_express_lane_effectiveness),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n✗ {test_name} FAILED: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\nYour simulation is working correctly!")
        print("You can now run the Gradio UI with: python gradio_app.py")
    else:
        print(f"\n⚠ {failed} test(s) failed. Please review the errors above.")
    
    print("=" * 70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
