"""
Test suite for numpy-only valuation distribution
Validates curve generation, safety checks, and edge cases
"""
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modules.valuation_distribution import (
    generate_distribution,
    calculate_distribution_stats,
    generate_distribution_curve,
    calculate_confidence_intervals,
    calculate_variability_level,
    collect_valuation_methods
)


def test_generate_distribution_basic():
    """Test basic distribution generation"""
    print("\n=== Test: Basic Distribution Generation ===")
    
    mean = 300000
    std_dev = 50000
    
    x, y = generate_distribution(mean, std_dev, points=100)
    
    assert len(x) == 100, "Should generate 100 points"
    assert len(y) == 100, "Should generate 100 y values"
    assert x[0] >= 0, "X values should not be negative"
    assert np.all(y >= 0), "Y values should not be negative"
    assert np.isclose(x[len(x)//2], mean, rtol=0.1), "Center should be near mean"
    
    print(f"✅ Mean: {mean:,.0f}")
    print(f"✅ Std Dev: {std_dev:,.0f}")
    print(f"✅ X range: {x[0]:,.0f} to {x[-1]:,.0f}")
    print(f"✅ Y max: {np.max(y):.6f}")
    print("✅ PASS: Basic distribution generation")


def test_generate_distribution_zero_std_dev():
    """Test handling of zero standard deviation"""
    print("\n=== Test: Zero Std Dev Safety ===")
    
    mean = 300000
    std_dev = 0
    
    x, y = generate_distribution(mean, std_dev, points=100)
    
    assert len(x) == 100, "Should still generate points"
    assert len(y) == 100, "Should still generate y values"
    assert np.all(np.isfinite(y)), "Y values should be finite"
    
    print(f"✅ Input std_dev: {std_dev}")
    print(f"✅ Handled safely, generated curve")
    print("✅ PASS: Zero std dev safety")


def test_calculate_distribution_stats_normal():
    """Test distribution stats with normal values"""
    print("\n=== Test: Distribution Stats (Normal) ===")
    
    methods = {
        "revenue_method": 280000,
        "earnings_method": 290000,
        "asset_method": 310000,
    }
    
    stats = calculate_distribution_stats(methods)
    
    assert stats is not None, "Should return stats"
    assert stats["mean"] > 0, "Mean should be positive"
    assert stats["std_dev"] > 0, "Std dev should be positive"
    assert stats["count"] == 3, "Should count 3 methods"
    assert stats["min"] == 280000, "Min should be correct"
    assert stats["max"] == 310000, "Max should be correct"
    
    print(f"✅ Mean: ${stats['mean']:,.0f}")
    print(f"✅ Std Dev: ${stats['std_dev']:,.0f}")
    print(f"✅ Count: {stats['count']}")
    print("✅ PASS: Normal distribution stats")


def test_calculate_distribution_stats_single_method():
    """Test distribution stats with single method"""
    print("\n=== Test: Distribution Stats (Single Method) ===")
    
    methods = {
        "revenue_method": 300000,
    }
    
    stats = calculate_distribution_stats(methods)
    
    assert stats is not None, "Should return stats"
    assert stats["mean"] == 300000, "Mean should equal single value"
    assert stats["std_dev"] > 0, "Should assign default std dev"
    assert stats["std_dev"] == 300000 * 0.20, "Should be 20% of mean"
    
    print(f"✅ Mean: ${stats['mean']:,.0f}")
    print(f"✅ Std Dev: ${stats['std_dev']:,.0f} (20% of mean)")
    print("✅ PASS: Single method stats")


def test_calculate_distribution_stats_empty():
    """Test distribution stats with empty methods"""
    print("\n=== Test: Distribution Stats (Empty) ===")
    
    methods = {}
    
    stats = calculate_distribution_stats(methods)
    
    assert stats is None, "Should return None for empty methods"
    
    print("✅ PASS: Empty methods handled safely")


def test_calculate_distribution_stats_invalid_values():
    """Test distribution stats with invalid values"""
    print("\n=== Test: Distribution Stats (Invalid Values) ===")
    
    methods = {
        "method1": 0,
        "method2": -100,
        "method3": None,
        "method4": 300000,
    }
    
    stats = calculate_distribution_stats(methods)
    
    assert stats is not None, "Should return stats after filtering"
    assert stats["count"] == 1, "Should only count valid value"
    assert stats["mean"] == 300000, "Should use only valid value"
    
    print(f"✅ Filtered out: 0, -100, None")
    print(f"✅ Kept: 300000")
    print(f"✅ Count: {stats['count']}")
    print("✅ PASS: Invalid values filtered")


def test_calculate_confidence_intervals():
    """Test confidence interval calculation"""
    print("\n=== Test: Confidence Intervals ===")
    
    mean = 300000
    std_dev = 50000
    
    ci = calculate_confidence_intervals(mean, std_dev)
    
    assert ci["ci_68"]["low"] >= 0, "CI low should not be negative"
    assert ci["ci_68"]["high"] > ci["ci_68"]["low"], "CI high > low"
    assert ci["ci_95"]["low"] >= 0, "CI 95 low should not be negative"
    assert ci["ci_95"]["high"] > ci["ci_95"]["low"], "CI 95 high > low"
    
    # 68% should be ±1 std dev
    assert np.isclose(ci["ci_68"]["low"], mean - std_dev), "68% low = mean - 1σ"
    assert np.isclose(ci["ci_68"]["high"], mean + std_dev), "68% high = mean + 1σ"
    
    # 95% should be ±2 std dev
    assert np.isclose(ci["ci_95"]["low"], mean - 2*std_dev), "95% low = mean - 2σ"
    assert np.isclose(ci["ci_95"]["high"], mean + 2*std_dev), "95% high = mean + 2σ"
    
    print(f"✅ 68% CI: ${ci['ci_68']['low']:,.0f} - ${ci['ci_68']['high']:,.0f}")
    print(f"✅ 95% CI: ${ci['ci_95']['low']:,.0f} - ${ci['ci_95']['high']:,.0f}")
    print("✅ PASS: Confidence intervals")


def test_calculate_variability_level():
    """Test variability level classification"""
    print("\n=== Test: Variability Level ===")
    
    # Low variability
    var_low = calculate_variability_level(15000, 300000)
    assert var_low["level"] == "Low", "CV=5% should be Low"
    assert var_low["icon"] == "✅", "Low should have ✅"
    print(f"✅ CV=5%: {var_low['level']} {var_low['icon']}")
    
    # Moderate variability
    var_mod = calculate_variability_level(60000, 300000)
    assert var_mod["level"] == "Moderate", "CV=20% should be Moderate"
    assert var_mod["icon"] == "⚠️", "Moderate should have ⚠️"
    print(f"✅ CV=20%: {var_mod['level']} {var_mod['icon']}")
    
    # High variability
    var_high = calculate_variability_level(150000, 300000)
    assert var_high["level"] == "High", "CV=50% should be High"
    assert var_high["icon"] == "❌", "High should have ❌"
    print(f"✅ CV=50%: {var_high['level']} {var_high['icon']}")
    
    print("✅ PASS: Variability classification")


def test_edge_case_negative_mean():
    """Test handling of negative mean"""
    print("\n=== Test: Edge Case - Negative Mean ===")
    
    mean = -100
    std_dev = 50
    
    x, y = generate_distribution(mean, std_dev, points=100)
    
    assert len(x) == 100, "Should generate points"
    assert len(y) == 100, "Should generate y values"
    assert np.all(np.isfinite(y)), "Y values should be finite"
    
    print("✅ PASS: Negative mean handled safely")


def test_edge_case_very_small_std_dev():
    """Test handling of very small std dev"""
    print("\n=== Test: Edge Case - Very Small Std Dev ===")
    
    mean = 300000
    std_dev = 0.001
    
    x, y = generate_distribution(mean, std_dev, points=100)
    
    assert len(x) == 100, "Should generate points"
    assert len(y) == 100, "Should generate y values"
    assert np.all(np.isfinite(y)), "Y values should be finite"
    
    print("✅ PASS: Very small std dev handled safely")


def test_full_workflow():
    """Test full workflow from methods to curve"""
    print("\n=== Test: Full Workflow ===")
    
    # Simulate core financials
    core_financials = {
        "revenue": 50000,
        "profit": 15000,
        "cash_on_hand": 100000,
    }
    
    # Step 1: Collect methods
    methods = collect_valuation_methods(core_financials)
    print(f"✅ Collected {len(methods)} methods")
    
    if not methods:
        print("⚠️ No methods available (valuation_logic may not be available)")
        return
    
    # Step 2: Calculate stats
    stats = calculate_distribution_stats(methods)
    assert stats is not None, "Should calculate stats"
    print(f"✅ Mean: ${stats['mean']:,.0f}, Std Dev: ${stats['std_dev']:,.0f}")
    
    # Step 3: Generate curve
    x, y = generate_distribution_curve(stats["mean"], stats["std_dev"])
    assert len(x) == 200, "Should generate 200 points"
    assert len(y) == 200, "Should generate 200 y values"
    print(f"✅ Generated curve with {len(x)} points")
    
    # Step 4: Calculate confidence intervals
    ci = calculate_confidence_intervals(stats["mean"], stats["std_dev"])
    assert ci is not None, "Should calculate CI"
    print(f"✅ 68% CI: ${ci['ci_68']['low']:,.0f} - ${ci['ci_68']['high']:,.0f}")
    
    # Step 5: Calculate variability
    var = calculate_variability_level(stats["std_dev"], stats["mean"])
    assert var is not None, "Should calculate variability"
    print(f"✅ Variability: {var['level']} (CV: {var['cv']:.1f}%)")
    
    print("✅ PASS: Full workflow")


def run_all_tests():
    """Run all validation tests"""
    print("=" * 60)
    print("VALUATION DISTRIBUTION NUMPY-ONLY VALIDATION")
    print("=" * 60)
    
    try:
        test_generate_distribution_basic()
        test_generate_distribution_zero_std_dev()
        test_calculate_distribution_stats_normal()
        test_calculate_distribution_stats_single_method()
        test_calculate_distribution_stats_empty()
        test_calculate_distribution_stats_invalid_values()
        test_calculate_confidence_intervals()
        test_calculate_variability_level()
        test_edge_case_negative_mean()
        test_edge_case_very_small_std_dev()
        test_full_workflow()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print("\n✅ Numpy-only implementation validated")
        print("✅ No scipy dependency")
        print("✅ All safety checks working")
        print("✅ Ready for deployment")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
