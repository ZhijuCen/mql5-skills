# Quick Ref — Tester Automation via CLI (`init-ini` + `backtest`)

Companion to `SKILL.md` §6. Headless single-test recipe for
`terminal64.exe /portable /config:<INI>` on Linux/Wine, encoded in
`scripts/mql5_helper.py` subcommands. Everything below was observed on
2026-09-03 (MT5 build 6140, Wine 11.0, XAUUSD M15 2.4-year every-tick
run ≈ 52–59 s); the error strings are greppable from the journal.

```
# 1. Generate an INI skeleton from the EA source (lists ALL inputs)
python scripts/mql5_helper.py init-ini Experts/MyEA.mq5 \
    --symbol XAUUSD --period M15 --from 2024.02.26 --to 2026.07.04 \
    --model 4 -o MyEA.XAUUSD.M15.ini

# 2. Run the single test headlessly; report lands in -o OUTDIR
python scripts/mql5_helper.py backtest MyEA.XAUUSD.M15.ini \
    [--instance DIR] [--stage-dir DIR] [-o OUTDIR] [--timeout 3600]
```

`init-ini` extras: `--json` prints the parsed inputs instead of writing;
enum/datetime identifiers that cannot be resolved from source are kept
verbatim with a `; TODO:` line — replace them with the numeric value
before running. `--expert PATH` overrides `Expert=` (default `<stem>.ex5`).

## 1. Pitfall list (each cost a failed launch once)

1. **Report working directory.** `[Tester] Report=<name>` writes
   `<name>.htm` (sometimes `.html`) + `<name>.png` / `-hst.png` /
   `-mfemae.png` / `-holding.png` into the **terminal working
   directory** — the install root for `/portable` launches. NOT the
   process CWD, NOT `MQL5\Files`, NOT the INI's directory. `backtest`
   searches that dir for files newer than launch (prefers the `Report=`
   stem, falls back to `ReportTester-*.htm*`) and copies them to
   `-o OUTDIR`. Control the destination with `-o`; control the name
   with `--report-name`.
2. **`/config:` path must be Windows-style ABSOLUTE and SPACE-FREE.**
   A path with spaces fails even when the shell quotes it; the journal
   shows `cannot load config "C:\...\MetaTrader 5-auto\.agents-s4.ini"" at
   start` (stray trailing-quote artifact of MT5's parser) and the
   terminal silently boots as a plain GUI. The INI must also EXIST
   before launch (a late `cp` costs a full launch cycle). `backtest`
   stages the normalized INI via `--stage-dir` (default: the Wine drive
   root derived from `MT5_BASE`, e.g. `…/drive_c` → `C:\`) and aborts
   if the resulting Windows path contains spaces.
3. **Single-instance lock.** A second `terminal64.exe` on the same
   installation/data dir is refused while the user's GUI instance is
   running. Run against a dedicated clone (`--instance`): a full
   directory copy of the install needs `Bases\` (symbol history, the
   bulk) and `MQL5\` (Include + the freshly deployed
   `MQL5\Experts\<EA>.ex5` — refreshed after EVERY compile); `temp\`,
   `logs\`, `Tester\Agent-*` caches can be excluded (~GB saved). The
   clone is bootstrapped automatically on first `backtest` if missing.
4. **`UseLocal=1` is REQUIRED.** Without it no local MetaTester agent
   spawns and the run silently never starts (journal idles after
   login; no agent log appears). `backtest` forces it in the staged
   copy and errors on an explicit `UseLocal=0`.
5. **`[TesterInputs]` format is mandatory even for single runs.** Every
   line must be `name=value||start||step||stop||Y|N` (booleans/enums
   use `step=0`); inputs omitted from the section silently fall back to
   EA source defaults — a stale INI is a GIGO trap. `backtest` rejects
   malformed lines instead of launching. Generate the skeleton with
   `init-ini` so nothing is omitted.
6. **Process control under Wine.** Launch detached
   (`setsid`-equivalent); completion = terminal process exit
   (`ShutdownTerminal=1`) + journal `last test passed` + report file
   present. Poll; never fixed-sleep. Cleanup must not self-match: use a
   character-class pattern (e.g. `pkill -f '5[-]auto'`) or kill the
   process group (`killpg`) — a plain `pkill -f <pattern>` kills the
   caller's own shell when the pattern appears in its command line.
7. **Journal encoding + cumulative day file.** `logs\YYYYMMDD.log` is
   UTF-16LE (naive `grep`/`tail` show NUL-padded text) and APPENDS
   across the whole day — grep the whole file and you will see this
   morning's stale failures. Slice from the byte offset recorded at
   launch (÷2 for UTF-16LE chars). Key lines:
   `automatic testing started` →
   `last test passed with result "successfully finished" in 0:00:52` →
   `exit with code 0`; failure tell: `cannot load config "..." at start`.
8. **INI line endings.** CRLF used in the successful run (LF not
   separately tested — convert to CRLF defensively). `backtest` always
   writes the staged copy with CRLF.

## 2. `[Tester]` model enum

| Model | Meaning | Note |
|-------|---------|------|
| 0 | every tick (generated) | default accuracy baseline |
| 1 | 1-minute OHLC | faster, coarser |
| 2 | open prices only | fast screening only — never for final eval |
| 3 | math calculations | no history needed |
| 4 | every tick based on real ticks | **falls back to generated ticks when the broker history has none** — the report's `History Quality: 0% real ticks` line is the tell |

## 3. `backtest` exit codes and outputs

| Code | Meaning |
|------|---------|
| 0 | journal `last test passed` AND report artifacts collected |
| 1 | validation error / journal failure / report missing |
| 2 | timeout (`--timeout` seconds, default 3600) — terminal killed |
| 130 | interrupted by Ctrl-C (terminal killed) |

`--json` emits `{status, passed, ea, instance, staged_ini, journal,
journal_key_lines, report, outdir, artifacts, elapsed_s}` instead of
the text summary. `--dry-run` validates, stages, refreshes the `.ex5`
and prints the launch command without launching (a missing instance is
reported, not cloned). Default `-o` is `./tester-report-<EA>-<ts>/`.

The text summary is `parse_tester_report.py report <OUTDIR>/<report>.htm`
(see `SKILL.md` §6 for the 8-step analysis order; run
`windows --count N` over the collected report for over-fitting checks).

## 4. Worked example (evidence run)

```
; INI (C:\mts4.ini) — [Tester] card
[Tester]
Expert=OneShotEA.ex5
Symbol=XAUUSD
Period=M15
Optimization=0
Model=4
FromDate=2024.02.26
ToDate=2026.07.04
Deposit=10000
Currency=USD
Leverage=100
Report=OneShotEA-s4-verify
ReplaceReport=1
UseLocal=1
ShutdownTerminal=1
```

Launch: `wine <instance>/terminal64.exe /portable /config:C:\mts4.ini`
(detached), poll ≈ 60 s, report `ReportTester-<login>.htm*` + 4 PNGs
land in the instance root, then get copied to the output dir. Note the
produced report file may carry the login-numbered name even when
`Report=` names something else — the fallback search handles this.
