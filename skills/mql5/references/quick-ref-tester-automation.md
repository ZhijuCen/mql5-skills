# Quick Ref — Tester Automation via CLI (`init-ini` + `tester`)

Companion to `SKILL.md` §6. Headless single tests **and Grid optimization**
via `terminal64.exe /portable /config:<INI>` on Linux/Wine, encoded in
`scripts/mql5_helper.py`. The command formerly named `backtest` is now
`tester` (no legacy alias); use `tester` in older recipes too.

```sh
# 1. Generate an INI skeleton from the EA source (lists ALL inputs)
python scripts/mql5_helper.py init-ini Experts/MyEA.mq5 \
    --symbol XAUUSD --period M15 --from 2024.02.26 --to 2026.07.04 \
    --model 4 -o MyEA.XAUUSD.M15.ini

# 2. Review the INI: Optimization=0 for a single test; =1 for Grid.
# For Grid, also set start/step/stop and Y for the inputs to vary.
python scripts/mql5_helper.py tester MyEA.XAUUSD.M15.ini \
    [--stage-dir DIR] [-o OUTDIR] [--timeout 3600]
```

`tester` runs the install named by `MT5_BASE` **in place** — no runner
directory is required, guessed, copied, or cloned (see pitfall #3).

`init-ini` defaults to `Optimization=0`; change that **in the INI** to
select optimization. `--json` prints parsed inputs instead of writing;
enum/datetime identifiers unresolved from source are kept verbatim with
`; TODO:` comments — replace them with numeric values before running.
`--expert PATH` overrides `Expert=` (default `<stem>.ex5`).

## 0. Path resolution (`.env` first, then env vars)

`mql5_helper.py` never scans `Program Files` and never guesses
directories. It resolves `MT5_BASE`, `MQL5_DIR`, `WINE_DISK_ROOT` in
this order:

1. the project **`.env`** file — walk-up from the CWD to the first
   `.env`, then walk-up from the script directory (so a command run from
   an unrelated CWD still reads the project file); `--env-file PATH`
   names one explicitly, `--no-env` disables `.env` loading entirely;
2. the real **environment variables** (`$MT5_BASE`, `$MQL5_DIR`,
   `$WINE_DISK_ROOT`) — only as a fallback for keys the file omits.

`.env` therefore **overrides** an already-exported variable; treat the
project file as the single source of truth. A key missing from both is
a hard error naming the variable (exit 1), never a guessed path.

The MT5 programs come from that configuration only:
`MT5_BASE/MetaEditor64.exe` (compile / check / deploy) and
`MT5_BASE/terminal64.exe` (tester) — no directory scanning. A missing
`MT5_BASE` directory, or a missing program inside it, is a hard error
naming what is missing, never a silent fallback. Wine itself is just the
`wine` binary on PATH (no extra config).

```sh
# .env at the project root
MT5_BASE="/home/USER/.wine/drive_c/Program Files/MetaTrader 5"
MQL5_DIR="/home/USER/.wine/drive_c/Program Files/MetaTrader 5/MQL5"
WINE_DISK_ROOT="Z"   # Unix only: the drive letter mapping to /
```

## 1. Pitfall list

Single-test observations: 2026-09-03, MT5 build 6140, Wine 11.0,
XAUUSD M15 2.4-year real-tick run ≈ 52–59 s.

1. **Report working directory and format.** `[Tester] Report=<name>`
   writes into the **terminal working directory** (install root with
   `/portable`), NOT the process CWD, `MQL5\Files`, or the INI directory.
   Single tests produce `.htm`/`.html` plus `.png`, `-hst.png`,
   `-mfemae.png`, `-holding.png`; optimization produces SpreadsheetML
   **`.xml`**, not HTML. `tester` searches for the appropriate format
   newer than launch, prefers the `Report=` stem, then falls back to
   `ReportTester-*` / `ReportOptimizer-*`. It copies artifacts to
   `-o OUTDIR`; `--report-name` controls the report name.
2. **`/config:` path must be Windows-style ABSOLUTE and SPACE-FREE.**
   Spaces can fail even when shell-quoted; journal:
   `cannot load config "C:\...\runner-headless\.agents-s4.ini" at start`.
   The terminal then boots as a plain GUI. `tester` stages an existing,
   normalized INI via `--stage-dir` (default: Wine drive root derived
   from `MT5_BASE`, e.g. `…/drive_c` → `C:\`) and rejects spaces.
3. **Single-instance lock.** The install named by `MT5_BASE` IS the
   runner: nothing is copied or cloned, so close any GUI terminal on
   that installation before a headless run. A second terminal on the
   same data directory trips the lock and the launch fails far from the
   cause. The EA `.ex5` is used straight from `MQL5_DIR/Experts/`
   (`Expert=` resolved there by `tester`), so `deploy` before testing.
4. **`UseLocal=1` is REQUIRED by this helper.** Without it the observed
   run never spawned a local agent. `tester` forces it in the staged
   copy and rejects explicit `UseLocal=0`. For local-only optimization,
   also set `UseRemote=0` and `UseCloud=0` in the INI (no cloud charges).
5. **`[TesterInputs]` format is mandatory even for single runs.**
   Optimizable `input`: `name=value||start||step||stop||Y|N`;
   booleans/enums use step 0. `string` inputs and `sinput` (static
   input) take a **bare** `name=value` instead — MT5 passes the raw
   right-hand side of a line to a string input verbatim, so a `||tail`
   leaks into the runtime value, and MT5's own client export writes
   strings bare; `sinput` is never enumerated by Grid/genetic search,
   so it has one fixed value and no range/flag. `tester`
   accepts both shapes and rejects anything else; `init-ini` lists all
   declarations in the matching shape. Omitted inputs fall back to the
   expert's last-used value if it already ran in this instance, else
   the compiled source default. For Grid, `Y`
   selects the range, `N` keeps the value fixed. Two values of one
   input × fixed others = **2 passes**. Verified 2026-09-22 (build
   6204): a bare line passes `tester --dry-run` (UTF-16 export too),
   arrives verbatim at runtime, and a Grid with one `Y` range plus two
   bare `sinput` finishes with exactly **2 passes** (no `sinput`
   column in the XML).
6. **Completion is mode-specific.** Require terminal exit
   (`ShutdownTerminal=1`), the successful test/optimization journal
   message, AND the correct report file. An HTML report from a single
   test is not evidence of an optimization. Launch detached and poll;
   on timeout/interrupt terminate only the launched process group,
   never broadly kill Wine or other terminals.
7. **Journal encoding + cumulative day file.** `logs\YYYYMMDD.log` is
   UTF-16LE and appends throughout the day. Capture its byte offset
   **before launch**, then read only newly appended content. Single-test
   sequence: `automatic testing started` →
   `last test passed with result "successfully finished"` →
   `exit with code 0`. **Optimization completion is in
   `tester/logs/YYYYMMDD.log`** (also check `Tester/logs`), not necessarily
   the terminal journal: `complete optimization started` →
   `optimization finished, total passes N`. The helper snapshots these
   journals before launch too; stopped/cancelled optimization is failure.
   Config failure: `cannot load config`.
8. **INI normalization.** The staged copy uses CRLF and forces
   `UseLocal=1`, `ReplaceReport=1`, `ShutdownTerminal=1`, and `Report=`.
   Explicit `Optimization`/`Model` values are preserved; missing ones
   default to 0 to avoid inheriting the runner's previous mode.

## 2. `[Tester]` Optimization and Model enums

Source: [MetaTrader 5 — Platform Start, configuration-file parameters](https://www.metatrader5.com/en/terminal/help/start_advanced/start#configuration_file).
These are **INI numeric values**, not GUI row indices. For EA input
enums (`ENUM_TIMEFRAMES`, `ENUM_APPLIED_PRICE`, order/deal types, …)
and their numeric values in `[TesterInputs]`/`.set`, see
`quick-ref-enum-values.md` — an invalid timeframe can stall the run
while it tries to sync non-existent history instead of reporting an
error.

### Optimization — all values

| Value | Meaning | Use |
|-------|---------|-----|
| 0 | Optimization disabled | Single test using each input's `value` field; helper default when omitted |
| 1 | Slow complete algorithm | **Grid / exhaustive search** of all combinations of selected input ranges |
| 2 | Fast genetic algorithm | Genetic search; not an exhaustive Grid and not suitable for proving exactly 2 combinations |
| 3 | All symbols selected in Market Watch | Run the EA with fixed inputs across selected symbols; not a parameter Grid |

### Model — supported price models

| Value | Meaning | Note |
|-------|---------|------|
| 0 | Every tick (generated) | Synthetic ticks generated from historical minute data; helper default when omitted |
| 1 | 1-minute OHLC | Uses minute Open/High/Low/Close control points; faster and coarser than every tick |
| 2 | Open prices only | Calls the EA at opens of the selected timeframe; fast screening for suitable bar-open strategies, not final intrabar evaluation |
| 4 | Every tick based on real ticks | Uses broker tick history; may generate ticks for missing/inconsistent history — inspect report history quality and tester journal |

Value 3 is intentionally excluded and rejected by this helper; it is
not used in verification. `init-ini --model` accepts only 0, 1, 2, 4.

For example, comments must be on **separate lines** (the helper does not
strip inline comments from INI values):

```ini
; Optimization: 0=single, 1=complete Grid, 2=genetic, 3=Market Watch symbols
Optimization=1
; Model: 0=generated every tick, 1=M1 OHLC, 2=open prices, 4=real ticks
Model=1
```

## 3. `tester` exit codes and outputs

| Code | Meaning |
|------|---------|
| 0 | Terminal exited, mode-specific success journal found, report collected |
| 1 | Validation / launch / config / journal failure, or report missing |
| 2 | Timeout (`--timeout`, default 3600 s); launched terminal killed |
| 130 | Ctrl-C; launched terminal killed |

`--json` emits `{status, passed, ea, optimization, run_dir, staged_ini,
journal, tester_journals, journal_key_lines, report, outdir, artifacts,
elapsed_s}` instead
of the parsed text summary (progress messages still precede the JSON).
`optimization` is the INI mode string. `--no-summary` skips the parser.
`--dry-run` validates, stages the INI, and prints the command without
launching.
Default `-o`: `./tester-report-<EA>-<ts>/`.

Summary dispatch:
- Single-test HTML: `parse_tester_report.py report <report>.htm`.
- Optimization XML: `parse_optimizer_report.py report <report>.xml`.

## 4. Two-pass Grid verification recipe

Use the bundled MetaQuotes `Moving Average` EA (available under
`MQL5/Experts/Examples/Moving Average/`). All inputs are listed, and only
`MovingPeriod` varies, over **12 and 13**: `(13−12)/1+1 = 2` combinations.
Disable forward testing to avoid extra runs. This is a plumbing check,
not a performance recommendation.

```ini
[Tester]
Expert=Examples\Moving Average\Moving Average.ex5
Symbol=XAUUSD
Period=M15
; Complete exhaustive Grid (not genetic)
Optimization=1
; 1-minute OHLC
Model=1
FromDate=2026.08.03
ToDate=2026.08.08
ForwardMode=0
Deposit=10000
Currency=USD
Leverage=100
; OptimizationCriterion (INI values mapped to MT5 client option names):
; 0 = Balance max
; 1 = Profit Factor max
; 2 = Expected Payoff max
; 3 = Drawdown min
; 4 = Recovery Factor max
; 5 = Sharpe Ratio max
; 6 = Custom max (value returned by the EA's OnTester())
; 7 = Complex Criterion max
OptimizationCriterion=1
Report=agent-verify-grid-2pass
ReplaceReport=1
UseLocal=1
UseRemote=0
UseCloud=0
Visual=0
ShutdownTerminal=1

[TesterInputs]
MaximumRisk=0.02||0.02||0.01||0.02||N
DecreaseFactor=3||3||1||3||N
MovingPeriod=12||12||1||13||Y
MovingShift=6||6||1||6||N
```

```sh
python scripts/mql5_helper.py tester grid.ini \
    --report-name agent-verify-grid-2pass \
    -o /tmp/agent-verify-grid/report --timeout 180
```

Verify the optimization completion journal, XML output, exactly two
result rows, and `MovingPeriod` values `{12, 13}`. Prefer clearing
`<MT5_BASE>/tester/cache` so the first check executes rather than
merely retrieves cached passes.

### Verified result — 2026-09-17

MT5 **build 6182**, Wine 11.0; the exact INI above was run in a separate
runner, leaving existing GUI/auto instances untouched. After correcting
optimization-log detection, the final run returned **0** (`Tester OK.`).
Its previously generated optimization cache was moved aside before the
rerun so both passes were calculated, not merely loaded from cache.
(The recipe originally ran in a cloned runner directory; the `tester`
command no longer clones — it runs the `MT5_BASE` install in place.)

```text
22:05:53.200  Tester      complete optimization started
22:06:00.606  Tester      optimization finished, total passes 2
22:06:00.616  Statistics  optimization done in 0 minutes 09 seconds
22:06:00.631  Tester      2 new records saved to cache file ...
22:06:01.150  Terminal    exit with code 0
```

`agent-verify-grid-2pass.xml` contained exactly two rows:

| Pass | MovingPeriod | Trades | Profit (USD) |
|------|--------------|--------|--------------|
| 0 | 12 | 21 | 751.15 |
| 1 | 13 | 22 | 292.86 |

Local evidence (temporary, not committed):
- INI: `/tmp/agent-verify-grid/grid.ini`
- Helper/journal excerpt: `/tmp/agent-verify-grid/run-final.log`
- XML: `/tmp/agent-verify-grid/report/agent-verify-grid-2pass.xml`

The XML summary parser correctly reads the two passes and parameter
values, but this build's environment metadata renders some header fields
as `(unknown)` and the build incorrectly; use the INI and terminal log
for that context. The parser itself is outside this two-file change.
A separate `Optimization=0` regression also returned 0 and collected
HTML + four PNGs; `--no-summary` skipped parsing as requested.
Genetic and Market Watch modes are documented/accepted, but were not
live-verified in this check; the demonstrated optimization mode is Grid.
