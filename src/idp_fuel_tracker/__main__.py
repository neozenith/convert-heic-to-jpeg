import sys
from dotenv import load_dotenv
import asyncio


from idp_fuel_tracker import sync, convert_heic, process_documents

load_dotenv()

async def main(args):
    print("Syncing...")

    print("Converting...")
    convert_heic()

    print("Processing...")
    await process_documents()

    #TODO: extract key values out:
    # ODO meter
    # Number of litres
    # Total price of fuel
    # Transaction date

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv))
    loop.close()
