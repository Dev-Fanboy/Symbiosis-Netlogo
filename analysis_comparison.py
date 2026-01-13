#!/usr/bin/env python3
"""
NetLogo BehaviorSpace Data Analysis - FIXED MODEL COMPARISON
Comparing original (broken) vs fixed model results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

plt.style.use('seaborn-v0_8-whitegrid')
sns.set_context("paper", font_scale=1.2)

# ============================================================
# LOAD BOTH DATASETS
# ============================================================
print("Loading data...")

# Original (broken) model
df_orig = pd.read_csv("/Users/michaelfaniyi/Desktop/Netlogo IS model/Industrial Symbiosis lock-in experiment-table.csv", skiprows=6)
df_orig.columns = ['run_number', 'g_turbulence_level', 'g_contract_strength', 
              'g_investment_cost', 'g_synergy_surplus', 'g_lock_in_period',
              'g_memory_duration', 'step', 'percent_investing', 'average_trust',
              'mean_wealth_producers', 'mean_wealth_consumers', 'current_market_value']

# Fixed model
df_fixed = pd.read_csv("/Users/michaelfaniyi/Desktop/Netlogo IS model/Netlogo IS model 2/Industrial Symbiosis lock-in experiment-table.csv", skiprows=6)
df_fixed.columns = ['run_number', 'g_turbulence_level', 'g_contract_strength', 
              'g_investment_cost', 'g_synergy_surplus', 'g_lock_in_period',
              'g_memory_duration', 'step', 'percent_investing', 'average_trust',
              'mean_wealth_producers', 'mean_wealth_consumers', 'current_market_value']

# Filter to final step
max_step_orig = df_orig['step'].max()
max_step_fixed = df_fixed['step'].max()

df_orig_final = df_orig[df_orig['step'] == max_step_orig].copy()
df_fixed_final = df_fixed[df_fixed['step'] == max_step_fixed].copy()

print(f"Original model: {len(df_orig_final)} runs at step {max_step_orig}")
print(f"Fixed model: {len(df_fixed_final)} runs at step {max_step_fixed}")

# ============================================================
# ANALYSIS 1: PHASE TRANSITION COMPARISON
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 1: PHASE TRANSITION - ORIGINAL vs FIXED")
print("="*60)

print("\n--- ORIGINAL MODEL (Broken) ---")
turb_orig = df_orig_final.groupby('g_turbulence_level')['percent_investing'].mean()
for turb, val in turb_orig.items():
    print(f"  Turbulence {turb}: {val:.1f}%")

print("\n--- FIXED MODEL ---")
turb_fixed = df_fixed_final.groupby('g_turbulence_level')['percent_investing'].mean()
for turb, val in turb_fixed.items():
    print(f"  Turbulence {turb}: {val:.1f}%")

# Find collapse point in fixed model
collapse_turb_fixed = None
for turb in sorted(df_fixed_final['g_turbulence_level'].unique()):
    mean_val = df_fixed_final[df_fixed_final['g_turbulence_level'] == turb]['percent_investing'].mean()
    if mean_val < 20:
        collapse_turb_fixed = turb
        break
print(f"\n>>> FIXED MODEL COLLAPSE POINT: Turbulence = {collapse_turb_fixed}")

# ============================================================
# ANALYSIS 2: SUBSTITUTION EFFECT
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 2: SUBSTITUTION EFFECT (MEMORY VS LAW) - FIXED MODEL")
print("="*60)

# Scenario A: Lawless but Long Memory
scenario_a = df_fixed_final[(df_fixed_final['g_contract_strength'] == 0) & (df_fixed_final['g_memory_duration'] == 100)]
# Scenario B: Strong Law but Short Memory
scenario_b = df_fixed_final[(df_fixed_final['g_contract_strength'] == 1.0) & (df_fixed_final['g_memory_duration'] == 10)]

print(f"\nScenario A (Lawless + Long Memory): {scenario_a['percent_investing'].mean():.1f}%")
print(f"Scenario B (Strong Law + Short Memory): {scenario_b['percent_investing'].mean():.1f}%")

turb_a = scenario_a.groupby('g_turbulence_level')['percent_investing'].mean()
turb_b = scenario_b.groupby('g_turbulence_level')['percent_investing'].mean()

print("\nTurbulence | Lawless+Memory | Law+No Memory | Winner")
print("-" * 55)
for turb in sorted(set(turb_a.index) & set(turb_b.index)):
    winner = "Memory" if turb_a.get(turb, 0) > turb_b.get(turb, 0) else "Law"
    print(f"    {turb}      |     {turb_a.get(turb, 0):.1f}%     |     {turb_b.get(turb, 0):.1f}%     | {winner}")

# ============================================================
# ANALYSIS 3: HEATMAPS - FIXED MODEL
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 3: GENERATING HEATMAPS FOR FIXED MODEL")
print("="*60)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for idx, memory in enumerate([10, 100]):
    df_memory = df_fixed_final[df_fixed_final['g_memory_duration'] == memory]
    
    pivot = df_memory.pivot_table(
        values='percent_investing',
        index='g_turbulence_level',
        columns='g_contract_strength',
        aggfunc='mean'
    )
    pivot = pivot.sort_index(ascending=False)
    
    ax = axes[idx]
    sns.heatmap(
        pivot, ax=ax, cmap='RdYlGn', vmin=0, vmax=100,
        annot=True, fmt='.0f', cbar_kws={'label': 'Mean % Investing'},
        linewidths=0.5
    )
    ax.set_title(f'Memory Duration = {memory}', fontsize=14, fontweight='bold')
    ax.set_xlabel('Contract Strength', fontsize=12)
    ax.set_ylabel('Turbulence Level', fontsize=12)

plt.suptitle('FIXED MODEL: Network Survival Rate\n(Green = Survival, Red = Collapse)', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/Users/michaelfaniyi/Desktop/Netlogo IS model/heatmap_FIXED_model.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: heatmap_FIXED_model.png")
plt.close()

# ============================================================
# ANALYSIS 4: COST BARRIER - FIXED MODEL
# ============================================================
print("\n" + "="*60)
print("ANALYSIS 4: COST BARRIER - FIXED MODEL")
print("="*60)

cost_fixed = df_fixed_final.groupby('g_investment_cost')['percent_investing'].agg(['mean', 'std'])
print("\nPercent Investing by Investment Cost (FIXED):")
print(cost_fixed)

# ============================================================
# COMPARISON SUMMARY
# ============================================================
print("\n" + "="*60)
print("COMPARISON: ORIGINAL vs FIXED MODEL")
print("="*60)

print("\n| Metric | Original | Fixed | Change |")
print("|--------|----------|-------|--------|")

# By turbulence
for turb in [0, 3, 5]:
    orig_val = df_orig_final[df_orig_final['g_turbulence_level']==turb]['percent_investing'].mean()
    fixed_val = df_fixed_final[df_fixed_final['g_turbulence_level']==turb]['percent_investing'].mean()
    change = fixed_val - orig_val
    print(f"| Turbulence {turb} | {orig_val:.1f}% | {fixed_val:.1f}% | {change:+.1f}% |")

# By contract
for contract in [0, 0.5, 1.0]:
    orig_val = df_orig_final[df_orig_final['g_contract_strength']==contract]['percent_investing'].mean()
    fixed_val = df_fixed_final[df_fixed_final['g_contract_strength']==contract]['percent_investing'].mean()
    change = fixed_val - orig_val
    print(f"| Contract {contract} | {orig_val:.1f}% | {fixed_val:.1f}% | {change:+.1f}% |")

# By cost
for cost in [0, 5, 10]:
    orig_val = df_orig_final[df_orig_final['g_investment_cost']==cost]['percent_investing'].mean()
    fixed_val = df_fixed_final[df_fixed_final['g_investment_cost']==cost]['percent_investing'].mean()
    change = fixed_val - orig_val
    print(f"| Cost {cost} | {orig_val:.1f}% | {fixed_val:.1f}% | {change:+.1f}% |")

# ============================================================
# SYNERGY SURPLUS CHECK
# ============================================================
print("\n--- SYNERGY SURPLUS EFFECT (FIXED MODEL) ---")
for surplus in sorted(df_fixed_final['g_synergy_surplus'].unique()):
    df_surp = df_fixed_final[df_fixed_final['g_synergy_surplus'] == surplus]
    print(f"\nSynergy = {surplus}: Mean = {df_surp['percent_investing'].mean():.1f}%")
    by_turb = df_surp.groupby('g_turbulence_level')['percent_investing'].mean()
    for t, v in by_turb.items():
        print(f"  Turbulence {t}: {v:.1f}%")

print("\n" + "="*60)
print("ABSTRACT-READY SUMMARY")
print("="*60)

# Key statistics
overall_mean = df_fixed_final['percent_investing'].mean()
turb0 = df_fixed_final[df_fixed_final['g_turbulence_level']==0]['percent_investing'].mean()
turb5 = df_fixed_final[df_fixed_final['g_turbulence_level']==5]['percent_investing'].mean()
cost0 = df_fixed_final[df_fixed_final['g_investment_cost']==0]['percent_investing'].mean()
cost10 = df_fixed_final[df_fixed_final['g_investment_cost']==10]['percent_investing'].mean()
mem10_mean = df_fixed_final[df_fixed_final['g_memory_duration']==10]['percent_investing'].mean()
mem100_mean = df_fixed_final[df_fixed_final['g_memory_duration']==100]['percent_investing'].mean()

print(f"""
FIXED MODEL KEY FINDINGS:
- Overall mean survival: {overall_mean:.1f}%
- Turbulence 0 → 5 effect: {turb0:.1f}% → {turb5:.1f}% (Δ = {turb5-turb0:+.1f}%)
- Cost 0 → 10 effect: {cost0:.1f}% → {cost10:.1f}% (Δ = {cost10-cost0:+.1f}%)
- Memory 10 → 100 effect: {mem10_mean:.1f}% → {mem100_mean:.1f}% (Δ = {mem100_mean-mem10_mean:+.1f}%)
- Collapse point: Turbulence = {collapse_turb_fixed}
""")

print("Analysis complete!")
