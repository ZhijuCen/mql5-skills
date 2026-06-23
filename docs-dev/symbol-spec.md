# Symbol Specification Workflow

Broker-specific symbol specifications stored as CSV files, used by the
SL/TP risk formula verification script.

## Location

```
skills/mql5/references/symbol-spec/
├── specs-XAUUSD.csv
├── specs-USDJPY.csv
└── ...
```

## CSV Format

Each file is a two-column CSV (`Property,Value`) exported from the MT5
Symbol Properties dialog. Key fields:

| Field | Example (XAUUSD) | Example (USDJPY) | Used By |
|-------|-------------------|-------------------|---------|
| Digits | 2 | 3 | NormalizeDouble, Point |
| Contract size | 100 | 100000 | PointValue, profit formula |
| Calculation | CFD Leverage | Forex | Formula selection |
| Tick size | 0.01 | 0.001 | Futures formula |
| Tick value | 1.0 | 0.618839 | Futures formula |
| Stops level | 0 | 0 | Min SL distance check |
| Profit currency | USD | JPY | Currency conversion |
| Minimal volume | 0.01 | 0.01 | Lot normalization |
| Maximal volume | 80.00 | 80.00 | Lot normalization |
| Volume step | 0.01 | 0.01 | Lot normalization |

## How to Export from MT5

1. In MT5: Tools → Symbols (or press Ctrl+U)
2. Select the symbol → Properties tab
3. Right-click → "Copy" or manually record values
4. Create `specs-{SYMBOL}.csv` with the `Property,Value` format

## How to Add a New Symbol

1. Export specs from MT5 (see above)
2. Save as `skills/mql5/references/symbol-spec/specs-{SYMBOL}.csv`
3. Add the symbol to `verify_sl_tp_formulas.py`:
   ```python
   specs = {
       "XAUUSD": SymbolSpec.from_csv(SPEC_DIR / "specs-XAUUSD.csv"),
       "USDJPY": SymbolSpec.from_csv(SPEC_DIR / "specs-USDJPY.csv"),
       "EURUSD": SymbolSpec.from_csv(SPEC_DIR / "specs-EURUSD.csv"),  # new
   }
   bids = {"XAUUSD": 4121.28, "USDJPY": 161.561, "EURUSD": 1.0850}
   fx_rates = {"XAUUSD": 1.0, "USDJPY": 161.561, "EURUSD": 1.0}
   ```
4. Run `python skills/mql5/scripts/verify_sl_tp_formulas.py` to verify

## Key Distinctions by Calc Mode

### Forex (SYMBOL_CALC_MODE_FOREX)
- Profit = `(close - open) × ContractSize × Lots`
- PointValue = `point × ContractSize`
- Example: USDJPY — ContractSize=100000, PointValue=100 JPY/pt/lot

### CFD Leverage (SYMBOL_CALC_MODE_CFDLEVERAGE)
- Profit = `(close - open) × ContractSize × Lots`
- PointValue = `point × ContractSize`
- Example: XAUUSD — ContractSize=100, PointValue=1.0 USD/pt/lot

### Futures (SYMBOL_CALC_MODE_FUTURES)
- Profit = `(close - open) × TickValue / TickSize × Lots`
- PointValue = `point × TickValue / TickSize`
- Uses broker-supplied TickValue instead of ContractSize

## Currency Conversion

When `SYMBOL_CURRENCY_PROFIT ≠ ACCOUNT_CURRENCY`:

```
risk_profcy = risk_account_cy × fx_rate
```

The verification script uses the `FindFXRate` helper to locate a Forex pair
in Market Watch that converts between the two currencies. In MQL5 code,
this is implemented in `SKILL.md` Section 5 (Direction B/C).
