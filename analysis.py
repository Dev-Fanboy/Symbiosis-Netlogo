#!/usr/bin/env python3
"""
NetLogo BehaviorSpace Data Analysis for Industrial Symbiosis Model
Analyzes the Hold-Up Problem in green investments
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style for publication-ready figures
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.2)

# ============================================================
# LOAD AND PREPARE DATA
# ============================================================
print("Loading data...")
# Use relative path for portability (file must be in the same directory)
data_path = Path("Industrial Symbiosis lock-in experiment-table.csv")

# Read CSV, skipping first 6 header rows
df = pd.read_csv(data_path, skiprows=6)

# Rename columns for easier access
df.columns = ['run_number', 'g_turbulence_level', 'g_contract_strength', 
              'g_investment_cost', 'g_synergy_surplus', 'g_lock_in_period',
              'g_memory_duration', 'step', 'percent_investing', 'average_trust',
              'mean_wealth_producers', 'mean_wealth_consumers', 'current_market_value']

print(f"Total rows loaded: {len(df):,}")
print(f"Step range: {df['step'].min()} to {df['step'].max()}")

# Filter to final step only (equilibrium state)
max_step = df['step'].max()
df_final = df[df['step'] == max_step].copy()
print(f"Rows at final step ({max_step}): {len(df_final):,}")

# ============================================================
# ANALYSIS 1: PHASE TRANSITION (THE "CLIFF EDGE")
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 1: PHASE TRANSITION (THE CLIFF EDGE)")
print("="*60)

# Group by turbulence level
turb_means = df_final.groupby('g_turbulence_level')['percent_investing'].agg(['mean', 'std', 'count'])
print("\nPercent Investing by Turbulence Level:")
print(turb_means)

# Find collapse point (where it drops below 20%)
collapse_turbulence = None
for turb in sorted(df_final['g_turbulence_level'].unique()):
    mean_val = df_final[df_final['g_turbulence_level'] == turb]['percent_investing'].mean()
    if mean_val < 20:
        collapse_turbulence = turb
        break
print(f"\n>>> COLLAPSE POINT: Turbulence Level = {collapse_turbulence} (below 20% survival)")

# Check synergy surplus effect on tipping point
print("\nSynergy Surplus Effect on Tipping Point:")
for surplus in sorted(df_final['g_synergy_surplus'].unique()):
    df_surplus = df_final[df_final['g_synergy_surplus'] == surplus]
    turb_by_surplus = df_surplus.groupby('g_turbulence_level')['percent_investing'].mean()
    print(f"\n  Synergy Surplus = {surplus}:")
    for turb in sorted(turb_by_surplus.index):
        print(f"    Turbulence {turb}: {turb_by_surplus[turb]:.1f}%")
    # Find where collapse occurs for this surplus level
    for turb in sorted(turb_by_surplus.index):
        if turb_by_surplus[turb] < 20:
            print(f"    >>> Collapse at Turbulence = {turb}")
            break

# ============================================================
# ANALYSIS 2: SUBSTITUTION EFFECT (MEMORY VS. LAW)
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 2: SUBSTITUTION EFFECT (MEMORY VS. LAW)")
print("="*60)

# Scenario A: Lawless but Long Memory (contract=0, memory=100)
scenario_a = df_final[(df_final['g_contract_strength'] == 0) & (df_final['g_memory_duration'] == 100)]
# Scenario B: Strong Law but Short Memory (contract=1.0, memory=10)
scenario_b = df_final[(df_final['g_contract_strength'] == 1.0) & (df_final['g_memory_duration'] == 10)]

print("\nScenario A (Lawless + Long Memory: contract=0, memory=100):")
print(f"  Sample size: {len(scenario_a)}")
print(f"  Mean percent investing: {scenario_a['percent_investing'].mean():.1f}%")
print("  By Turbulence Level:")
turb_a = scenario_a.groupby('g_turbulence_level')['percent_investing'].mean()
for turb, val in turb_a.items():
    print(f"    Turbulence {turb}: {val:.1f}%")

print("\nScenario B (Strong Law + Short Memory: contract=1.0, memory=10):")
print(f"  Sample size: {len(scenario_b)}")
print(f"  Mean percent investing: {scenario_b['percent_investing'].mean():.1f}%")
print("  By Turbulence Level:")
turb_b = scenario_b.groupby('g_turbulence_level')['percent_investing'].mean()
for turb, val in turb_b.items():
    print(f"    Turbulence {turb}: {val:.1f}%")

# Compare at each turbulence level
print("\nDirect Comparison (Memory vs Law):")
print("Turbulence | Lawless+Memory | Law+No Memory | Difference")
print("-" * 60)
for turb in sorted(set(turb_a.index) & set(turb_b.index)):
    diff = turb_a[turb] - turb_b[turb]
    winner = "Memory > Law" if diff > 0 else "Law > Memory"
    print(f"    {turb}      |     {turb_a[turb]:.1f}%     |     {turb_b[turb]:.1f}%     | {diff:+.1f}% ({winner})")

# ============================================================
# ANALYSIS 3: PAPER-READY HEATMAP
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 3: GENERATING HEATMAPS")
print("="*60)

# Create pivot tables for heatmaps
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for idx, memory in enumerate([10, 100]):
    df_memory = df_final[df_final['g_memory_duration'] == memory]
    
    # Create pivot table: rows=turbulence, cols=contract_strength, values=mean percent_investing
    pivot = df_memory.pivot_table(
        values='percent_investing',
        index='g_turbulence_level',
        columns='g_contract_strength',
        aggfunc='mean'
    )
    
    # Reverse row order so high turbulence is at top
    pivot = pivot.sort_index(ascending=False)
    
    # Create heatmap
    ax = axes[idx]
    im = sns.heatmap(
        pivot, 
        ax=ax,
        cmap='RdYlGn',  # Red (low) to Yellow to Green (high)
        vmin=0, 
        vmax=100,
        annot=True,
        fmt='.0f',
        cbar_kws={'label': 'Mean % Investing'},
        linewidths=0.5
    )
    
    ax.set_title(f'Memory Duration = {memory}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Contract Strength (g-contract-strength)', fontsize=12)
    ax.set_ylabel('Turbulence Level (g-turbulence-level)', fontsize=12)

plt.suptitle('Industrial Symbiosis Network Survival Rate\n(Green = Survival, Red = Collapse)', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/Users/michaelfaniyi/Desktop/Netlogo IS model/heatmap_memory_comparison.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Heatmap saved to: heatmap_memory_comparison.png")
plt.close()

# ============================================================
# ANALYSIS 4: J-CURVE COST BARRIER
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 4: J-CURVE COST BARRIER ANALYSIS")
print("="*60)

# Compare investment costs
cost_analysis = df_final.groupby('g_investment_cost')['percent_investing'].agg(['mean', 'std', 'count'])
print("\nPercent Investing by Investment Cost:")
print(cost_analysis)

# Detailed comparison: Cost 0 vs Cost 10
for cost in [0, 10]:
    print(f"\nInvestment Cost = {cost}:")
    df_cost = df_final[df_final['g_investment_cost'] == cost]
    print(f"  Overall mean: {df_cost['percent_investing'].mean():.1f}%")
    print("  By Turbulence Level:")
    by_turb = df_cost.groupby('g_turbulence_level')['percent_investing'].mean()
    for turb, val in by_turb.items():
        print(f"    Turbulence {turb}: {val:.1f}%")

# Check if high cost causes collapse regardless of other variables
print("\nHigh Cost (10) with Best Conditions (Low Turbulence + High Contract):")
best_conditions_high_cost = df_final[
    (df_final['g_investment_cost'] == 10) & 
    (df_final['g_turbulence_level'] == 0) & 
    (df_final['g_contract_strength'] == 1.0)
]
print(f"  Mean: {best_conditions_high_cost['percent_investing'].mean():.1f}%")

print("\nNo Cost (0) with Worst Conditions (High Turbulence + No Contract):")
worst_conditions_no_cost = df_final[
    (df_final['g_investment_cost'] == 0) & 
    (df_final['g_turbulence_level'] == 5) & 
    (df_final['g_contract_strength'] == 0)
]
print(f"  Mean: {worst_conditions_no_cost['percent_investing'].mean():.1f}%")

# ============================================================
# SUMMARY STATISTICS FOR ABSTRACT
# ============================================================
print("\n" + "="*60)
print("SUMMARY STATISTICS FOR PAPER ABSTRACT")
print("="*60)

print(f"""
KEY FINDINGS:
-------------
1. PHASE TRANSITION:
   - Network collapses at Turbulence = {collapse_turbulence}
   - At Turbulence 0: {df_final[df_final['g_turbulence_level']==0]['percent_investing'].mean():.1f}% survival
   - At Turbulence 5: {df_final[df_final['g_turbulence_level']==5]['percent_investing'].mean():.1f}% survival

2. SUBSTITUTION EFFECT:
   - Overall: Long Memory (no law) vs Strong Law (no memory):
     * Lawless + Long Memory: {scenario_a['percent_investing'].mean():.1f}%
     * Strong Law + No Memory: {scenario_b['percent_investing'].mean():.1f}%
   - Memory can partially substitute for formal contracts

3. COST BARRIER EFFECT:
   - Zero cost: {df_final[df_final['g_investment_cost']==0]['percent_investing'].mean():.1f}% mean survival
   - High cost (10): {df_final[df_final['g_investment_cost']==10]['percent_investing'].mean():.1f}% mean survival
   - Cost difference: {df_final[df_final['g_investment_cost']==0]['percent_investing'].mean() - df_final[df_final['g_investment_cost']==10]['percent_investing'].mean():.1f} percentage points
""")

# Additional analysis: Interaction effects
print("\n" + "="*60)
print("ADDITIONAL: SYNERGY SURPLUS EFFECT")
print("="*60)

for surplus in sorted(df_final['g_synergy_surplus'].unique()):
    df_surplus = df_final[df_final['g_synergy_surplus'] == surplus]
    print(f"\nSynergy Surplus = {surplus}:")
    print(f"  Overall mean survival: {df_surplus['percent_investing'].mean():.1f}%")
    print(f"  At Turbulence 5: {df_surplus[df_surplus['g_turbulence_level']==5]['percent_investing'].mean():.1f}%")

print("\nAnalysis complete!")
