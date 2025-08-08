# International Trade (Simple NetLogo Model)

This is a minimal NetLogo model that simulates international trade among multiple countries with two goods (A and B). Countries specialize based on comparative advantage, demand goods with Cobb-Douglas preferences, and the price of good A adjusts via a simple tâtonnement mechanism. Trade flows in good A are visualized as link thickness between countries.

## Files
- `InternationalTrade.nls`: NetLogo source code to paste into a new model (Code tab).

## Quick Start
1. Open NetLogo (6.x).
2. Create a new model (File → New) and open the Code tab.
3. Paste the content of `InternationalTrade.nls` into the Code tab.
4. Switch to the Interface tab and add the following:
   - Sliders:
     - `num-countries`: min 2, max 30, increment 1, initial 8
     - `price-adjust-speed`: min 0, max 1, increment 0.01, initial 0.2
   - Buttons:
     - `setup` (Observer)
     - `go` (Observer, Forever)
   - Optional Plots:
     - Plot named `Price of A` with pen `pA`
     - Plot named `Excess Demand A` with pen `excess`
     - Plot named `Trade Value` with pen `value`
   - Optional Monitors for `pA`, `world-excess-demand-a`, `world-gdp`, `total-trade-value`.

5. Click `setup`, then `go`.

## Model Dynamics (Intuition)
- Countries (turtles) have labor and productivity in two goods (A, B).
- Each tick, a country specializes in the higher-revenue good at current prices and produces that good only.
- Income equals the value of production. Cobb-Douglas demand splits income across goods.
- The price of A adjusts upward when world demand exceeds world supply, and down otherwise.
- Bilateral trade flows for good A are a simple proportional allocation from exporters (surplus) to importers (deficit) and are shown on links.

## Notes and Extensions
- Good B is the numeraire with price fixed at 1.
- The price update is exponential to keep `pA > 0` and controlled by `price-adjust-speed`.
- For more realistic trade, you can add trade costs, transport frictions, heterogeneous preferences, or gradual production adjustment instead of full specialization.
- To plot variables, uncomment the relevant lines in `update-plots` after adding the plots in the Interface.