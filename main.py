import requests, json, argparse, sys, difflib

from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.json import JSON
from rich.progress import Progress

BASE_DIR = Path(__file__).parent
ROUTINES_DIR = BASE_DIR / "Routines"
OUTPUT_FOLDER = ROUTINES_DIR / "Output"

ts = datetime.now().timestamp()
OUTPUT_NAME = f"Run_{ts}.txt"

REQUIRED_KEYS = {
    "rone": [
        "routine", "steps"
    ],
    "rtwo": [
        "request"
    ],
    "rthree":[
        "method", "url", "params"
    ]
}

console = Console()

def init_folders():
    if not ROUTINES_DIR.exists():
        ROUTINES_DIR.mkdir()

    if not OUTPUT_FOLDER.exists():
        OUTPUT_FOLDER.mkdir()



def writeToOutput(routineData, test=None, status=None, error: str | None = None):
    if test is not None:
        reqTable = Table.grid(padding=(0, 2))
        reqTable.add_row("STATUS", f"[green]SUCESS[/green]")
        reqTable.add_row("STATUS CODE", f"[green]{status}[/green]")
        reqTable.add_row("URL", routineData["steps"][0]["request"]["url"])

        resTable = Table.grid()
        resTable.add_row(Panel.fit(reqTable, title="Request"))
        resTable.add_row(Panel.fit(JSON.from_data(test), title="Response"))

    else:
        reqTable = Table.grid(padding=(0, 2))
        if status is not None and status == 200:
            reqTable.add_row("STATUS", f"[red]Success[/red]")
        else:
            reqTable.add_row("STATUS", f"[red]FAILED[/red]")

        if status is not None:
            reqTable.add_row("STATUS CODE", f"[green]{status}[/green]")

        reqTable.add_row("URL", routineData["steps"][0]["request"]["url"])

        resTable = Table.grid()
        resTable.add_row(Panel.fit(reqTable, title="Request"))
        resTable.add_row(Panel.fit(error.__str__(), title="Response"))


    with open(OUTPUT_FOLDER / OUTPUT_NAME, mode='a') as handle:
        subCons = Console(file=handle)
        subCons.print(Panel.fit(resTable, title=routineData["routine"]))

def RunRoutine(name:str, all:bool=False):
    if not ROUTINES_DIR.exists():
        console.print("Routines folder not found, run init")
        return

    todo:list[Path] | None = None

    if not all:
        tmpPath = ROUTINES_DIR / f"{name}.json"

        if not tmpPath.exists():
            console.print(f"Error: Routine {name} not found.")
            return
        
        todo = [tmpPath]

    if todo is None:
        todo = [file for file in ROUTINES_DIR.iterdir() if file.is_file()]

    with Progress(transient=True) as progress:
        task = progress.add_task("Running routines", total=len(todo))

        for routine in todo:
            if routine.is_dir():
                continue
            
            routineData:dict = json.loads(open(routine, mode='r').read())
            
            progress.console.print(f"Working on Routine: {routineData["routine"]}")

            try:
                test = requests.request(
                    method=routineData["steps"][0]["request"]["method"],
                    url=routineData["steps"][0]["request"]["url"],
                    params=routineData["steps"][0]["request"].get("params"),
                    headers=routineData["steps"][0]["request"].get("headers"),
                    auth=tuple(routineData["steps"][0]["request"].get("auth")) if "auth" in routineData["steps"][0]["request"] else None
                )

                display = routineData["steps"][0]["request"].get("display")

                if display is not None:
                    resDict = test.json()
                    filterDict = {}

                    if len(display) > 0:
                        for field in display:
                            filterDict[field] = resDict.get(field)

                        if filterDict is not {}:
                            writeToOutput(routineData, filterDict, status=test.status_code)
                            continue
                try:
                    writeToOutput(routineData, test.json(), status=test.status_code)
                except requests.exceptions.JSONDecodeError:
                    writeToOutput(routineData, status=test.status_code, error="no json response")

            except requests.exceptions.ConnectionError as e:
                progress.console.print(f"Routine: {routineData["routine"]} failed!")
                writeToOutput(routineData, error="Connection failed!")
                progress.advance(task)
                continue

            except requests.exceptions.Timeout as e:
                progress.console.print(f"Routine: {routineData["routine"]} failed!")
                writeToOutput(routineData, error="Connection timeout!")
                progress.advance(task)
                continue

            except Exception as e:
                progress.console.print(f"Routine: {routineData["routine"]} failed!")
                writeToOutput(routineData, error=e.__str__())
                progress.advance(task)
                continue
            
            progress.advance(task)

    console.print(f"Done! output: {OUTPUT_FOLDER / OUTPUT_NAME}")

def ListRoutines():
    if not ROUTINES_DIR.exists():
        console.print("Routines folder not found, run init")
        return

    if len(list(ROUTINES_DIR.iterdir())) == 1:
        console.print("Routines folder only containes output folder")
        return

    for routine in ROUTINES_DIR.iterdir():
        if routine.is_dir():
            continue

        console.print(routine.stem)

args = argparse.ArgumentParser("Routiner", description="Run predifined API Routines with run, See all Routines with list, Create needed folders with init")
subargs = args.add_subparsers(dest='subparser_name')

runRoutine = subargs.add_parser('run', description='Runs either all routines or a specefied one')
runGroup = runRoutine.add_mutually_exclusive_group()
runGroup.add_argument('name', type=str, nargs='?', help='Name of the routine file to run without .json')
runGroup.add_argument('-a', '--all', action="store_true", help='Flag to run all routines')

listRoutines = subargs.add_parser('list', description='Lists all the routine files found in the routines folder')

initFolders = subargs.add_parser("init", description="makes the routines and output folders")

choice = args.parse_args()

match choice.subparser_name:
    case "run":
        RunRoutine(choice.name, choice.all)

    case "list":
        ListRoutines()

    case "init":
        init_folders()
        console.print("initialized folders")

    case _:
        console.print("action not found")

sys.exit()