import requests, json

from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.syntax import Syntax
from rich.json import JSON
from rich.progress import Progress

BASE_DIR = Path(__file__).parent
OUTPUT_FOLDER = BASE_DIR / "Output"
ROUTINES_DIR = BASE_DIR / "Routines"

if not OUTPUT_FOLDER.exists():
    OUTPUT_FOLDER.mkdir()

if not ROUTINES_DIR.exists():
    ROUTINES_DIR.mkdir()

ts = datetime.now().timestamp()
OUTPUT_NAME = f"Run_{ts}.txt"

console = Console()

with Progress(transient=True) as progress:
    task = progress.add_task("Running routines", total=len(list(ROUTINES_DIR.iterdir())))

    for routine in ROUTINES_DIR.iterdir():
        routineData:dict = json.loads(open(routine, mode='r').read())
        progress.console.print(f"Working on Routine: {routineData["routine"]}")

        try:
            test = requests.request(
                method=routineData["steps"][0]["request"]["method"],
                url=routineData["steps"][0]["request"]["url"],
                params=routineData["steps"][0]["request"]["params"],
            )

        except:
            progress.console.print(f"Routine: {routineData["routine"]} failed!")
            progress.advance(task)
            continue

        reqTable = Table.grid(padding=(0, 2))
        reqTable.add_row("STATUS", f"[green]{test.status_code}[/green]")
        reqTable.add_row("URL", routineData["steps"][0]["request"]["url"])

        resTable = Table.grid()
        resTable.add_row(Panel.fit(reqTable, title="Request"))
        resTable.add_row(Panel.fit(JSON.from_data(test.json()), title="Response"))

        with open(OUTPUT_FOLDER / OUTPUT_NAME, mode='a') as handle:
            subCons = Console(file=handle)
            subCons.print(Panel.fit(resTable, title=routineData["routine"]))

        progress.advance(task)

console.print(f"Done! output: {OUTPUT_FOLDER / OUTPUT_NAME}")
