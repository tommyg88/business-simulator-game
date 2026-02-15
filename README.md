# Business Simulator Game

A lightweight Python business simulator where you manage a company over 12 months.

## Features

- Manage core business metrics: cash, reputation, staff, and product quality.
- Choose monthly actions like improving product, hiring staff, and running marketing.
- Handle random market shocks that impact your outcome.
- Win by surviving the full year with strong performance.

## How to Play

1. Run the game:
   ```bash
   python3 business_simulator.py
   ```
2. Each month, type one of the listed actions:
   - `improve_product`
   - `hire_staff`
   - `marketing_campaign`
   - `cut_costs`
   - `do_nothing`
3. The game ends after 12 months or if your business collapses.

## Run Tests

```bash
python3 -m pytest -q
```

If `pytest` is not installed, use:

```bash
python3 -m unittest
```
