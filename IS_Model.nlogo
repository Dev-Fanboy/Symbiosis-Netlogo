;; =========================================================
;; INDUSTRIAL SYMBIOSIS: HOLD-UP GAME WITH LOCK-IN
;; ** FIXED VERSION ** - Investment cost is one-time, turbulence affects decisions
;; =========================================================

globals [
  ;; --- MARKET VARIABLES ---
  current-market-value      ;; Tracks the fluctuating energy price
  market-volatility-history ;; Tracks recent volatility for risk perception
  
  ;; SLIDERS NEEDED:
  ;; g-turbulence-level (0 to 5.0)
  ;; g-contract-strength (0 to 1.0)
  ;; g-investment-cost (0, 5, 10)
  ;; g-synergy-surplus (5, 15)
  ;; g-lock-in-period (10, 30)
  ;; g-memory-duration (10, 100)
]

breed [ producers producer ]
breed [ consumers consumer ]
undirected-link-breed [ negotiations negotiation ]

turtles-own [
  wealth
  strategy              ;; "investing" vs "cautious" OR "honest" vs "opportunistic"
]

producers-own [
  black-list            ;; A list of consumers who held me up: [[who time-added] ...]
  has-paid-investment?  ;; NEW: Track if one-time cost was paid this contract
]

negotiations-own [
  contract-age          ;; Tracks how long this specific deal has lasted
]

;; =========================================================
;; SETUP PROCEDURES
;; =========================================================

to setup
  clear-all
  
  ;; Set default values (Use Sliders to override these)
  if is-string? g-investment-cost [ set g-investment-cost 10 ] 
  
  ;; Initialize Market Value (Baseline)
  set current-market-value g-synergy-surplus 
  set market-volatility-history []

  create-producers 50 [
    setXY random-xcor random-ycor
    set shape "factory" 
    set wealth 50
    set strategy one-of ["investing" "cautious"]
    set black-list []
    set has-paid-investment? false
    update-color
  ]

  create-consumers 50 [
    setXY random-xcor random-ycor
    set shape "house" 
    set wealth 50
    set strategy one-of ["honest" "opportunistic"]
    update-color
  ]
  
  reset-ticks
end

;; =========================================================
;; MAIN LOOP
;; =========================================================

to go
  ;; 1. Update Market Conditions (TURBULENCE)
  update-market-conditions

  ;; 2. Movement & Costs
  ask turtles [ 
    ;; Only move if you are NOT in a contract (fixed facility)
    if not any? my-links [ move ]
    set wealth wealth - 0.5  ;; Cost of living
  ]
  
  ;; 3. Memory Management
  ask producers [ manage-memory ]

  ;; 4. Interaction 
  manage-symbiosis
  play-holdup-game
  
  ;; 5. Evolution (Social Learning) - NOW CONSIDERS RISK
  update-strategies
  
  ;; 6. Visualization
  ask turtles [ update-color ]
  tick
end

;; =========================================================
;; SUB-ROUTINES
;; =========================================================

to move
  rt random 50 - 25
  fd 1
  if not can-move? 1 [ rt 180 ]
end

to update-color
  ifelse breed = producers [
    ;; Producers: Cyan = Investing, Blue = Cautious
    ifelse strategy = "investing" [ set color cyan ] [ set color blue ]
  ]
  [
    ;; Consumers: Yellow = Honest, Red = Opportunistic
    ifelse strategy = "honest" [ set color yellow ] [ set color red ]
  ]
end

to manage-memory
  if not empty? black-list [
    set black-list filter [ entry -> 
      (ticks - item 1 entry) < g-memory-duration 
    ] black-list
  ]
end

to manage-symbiosis
  ;; 1. Age all existing contracts
  ask negotiations [ 
    set contract-age contract-age + 1 
    set thickness min list 0.5 (0.1 + (contract-age / 200))
  ]

  ;; 2. Check for Exits (Can I leave?)
  ask negotiations [
    let prod end1
    let cons end2
    let is-trapped? (contract-age < g-lock-in-period)
    let partner-is-bad? ([strategy] of cons = "opportunistic")
    
    ;; LOGIC:
    ;; If I am TRAPPED, I stay (even if they are bad).
    ;; If I am FREE (period over), I leave ONLY if they are bad.
    
    if not is-trapped? [
      if partner-is-bad? [ 
        ask prod [ 
          ;; Record the bad partner NOW
          set black-list lput (list ([who] of cons) ticks) black-list 
          ;; Reset investment flag when contract ends
          set has-paid-investment? false
        ]
        die ;; Break the link
      ]
    ]
  ]

  ;; 3. Form NEW links (only for those who are free)
  ask producers [
    if strategy = "investing" and not any? my-links [
      
      let candidates consumers in-radius 5
      
      ;; ** REPUTATION CHECK **
      if not empty? black-list [
        let bad-ids map [entry -> item 0 entry] black-list
        set candidates candidates with [ not member? who bad-ids ]
      ]
      
      let potential-partner one-of candidates
      
      if potential-partner != nobody [
        ;; *** FIX #1: PAY INVESTMENT COST ONCE HERE ***
        set wealth wealth - g-investment-cost
        set has-paid-investment? true
        
        create-negotiation-with potential-partner [
          set contract-age 0  ;; Initialize age
          set color white
          set thickness 0.1   ;; Start thin
        ]
      ]
    ]
  ]
end

;; --- THE GAME (FIXED - NO PER-TICK INVESTMENT COST) ---
to play-holdup-game
  ask negotiations [
    let prod end1 
    let cons end2
    
    ;; NO LONGER PAYING INVESTMENT COST EVERY TICK - it's paid once at link creation
    
    ;; Consumer Decides Behavior
    let actual-behavior [strategy] of cons
    
    ;; Legal System Check
    if random-float 1.0 < g-contract-strength [
      set actual-behavior "honest"
    ]
    
    ;; Payoffs (USING DYNAMIC MARKET VALUE)
    ifelse actual-behavior = "honest" [
      ;; -- COOPERATION --
      let share (current-market-value / 2)
      ask prod [ set wealth wealth + share ]
      ask cons [ set wealth wealth + share ]
    ]
    [
      ;; -- HOLD UP --
      ;; Consumer takes surplus, Producer gets scrap value
      let scrap-value 1
      ask prod [ set wealth wealth + scrap-value ]
      ask cons [ set wealth wealth + (current-market-value - scrap-value) ]
    ]
  ]
end

;; --- EVOLUTIONARY LEARNING (FIXED - NOW CONSIDERS RISK & CONTRACTS) ---
to update-strategies
  ask turtles [
    let mentor one-of other turtles with [breed = [breed] of myself] in-radius 5
    if mentor != nobody [
      if [wealth] of mentor > wealth [
        
        ;; Check if I am locked in
        let am-i-locked? (any? my-links with [contract-age < g-lock-in-period])
        
        if not am-i-locked? [
          
          ;; *** FIX #2 & #3: PRODUCERS NOW CONSIDER RISK AND CONTRACTS ***
          ifelse breed = producers [
            ;; Calculate expected value of investing
            let prob-opportunistic (count consumers with [strategy = "opportunistic"]) / max list 1 (count consumers)
            
            ;; Contract strength reduces effective opportunism
            let effective-opportunism prob-opportunistic * (1 - g-contract-strength)
            
            ;; Calculate expected payoff from honest vs opportunistic partners
            let coop-payoff (current-market-value / 2)
            let holdup-payoff 1  ;; scrap value
            let expected-payoff (coop-payoff * (1 - effective-opportunism)) + (holdup-payoff * effective-opportunism)
            
            ;; Risk penalty from turbulence (agents are risk-averse)
            let risk-penalty g-turbulence-level * 0.5  ;; Higher turbulence = higher perceived risk
            let risk-adjusted-payoff expected-payoff - risk-penalty
            
            ;; Net value = expected payoff - one-time cost amortized over expected contract length
            let amortized-cost g-investment-cost / max list 1 (g-lock-in-period * 5)  ;; expect ~5 contract cycles
            let net-value risk-adjusted-payoff - amortized-cost
            
            ;; DECISION: Invest if net value > baseline survival cost
            ifelse net-value > 0.5 [
              ;; Investing is worth it - copy mentor if they're investing
              if [strategy] of mentor = "investing" [
                set strategy "investing"
              ]
            ][
              ;; Investing is not worth it - be cautious
              ;; But still allow learning from wealthy cautious agents
              if [strategy] of mentor = "cautious" [
                set strategy "cautious"
              ]
            ]
          ][
            ;; CONSUMERS: Just copy strategy from wealthier peer
            set strategy [strategy] of mentor
          ]
          
          ;; Mutation (same as before)
          if random-float 100 < 1 [ 
            ifelse breed = producers 
              [ set strategy one-of ["investing" "cautious"] ]
              [ set strategy one-of ["honest" "opportunistic"] ]
          ]
        ]
      ]
    ]
  ]
end

;; --- TURBULENCE PROCEDURE (ENHANCED - TRACKS VOLATILITY) ---
to update-market-conditions
  ;; Simulates market volatility based on the slider 'g-turbulence-level'
  
  let shock random-normal 0 g-turbulence-level
  set current-market-value (g-synergy-surplus + shock)
  
  ;; Prevent negative value
  if current-market-value < 0 [ set current-market-value 0 ]
  
  ;; Track volatility history for agent perception (optional)
  set market-volatility-history lput abs(shock) market-volatility-history
  if length market-volatility-history > 50 [
    set market-volatility-history but-first market-volatility-history
  ]
end

;; =========================================================
;; REPORTERS (for BehaviorSpace)
;; =========================================================

to-report average-trust
  if count consumers = 0 [ report 0 ]
  report (count consumers with [strategy = "honest"] / count consumers) * 100
end

to-report percent-investing
  if count producers = 0 [ report 0 ]
  report (count producers with [strategy = "investing"] / count producers) * 100
end

;; NEW: Report perceived market risk
to-report perceived-volatility
  if empty? market-volatility-history [ report 0 ]
  report mean market-volatility-history
end

;; NEW: Report active contracts
to-report active-contracts
  report count negotiations
end
