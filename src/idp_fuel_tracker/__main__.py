import asyncio
import sys

from dotenv import load_dotenv

from idp_fuel_tracker import convert, process_documents, sync_files

load_dotenv()


async def main(args):
    print("Syncing...")
    sync_files()

    print("Converting...")
    list_of_files = convert()

    print("Processing...")
    await process_documents(list_of_files, overwrite=False)

    # TODO: extract key values out:
    # ODO meter
    # Number of litres
    # Total price of fuel
    # Transaction date


if __name__ == "__main__":
    try:
        asyncio.run(main(sys.argv))
    except KeyboardInterrupt:
        pass
