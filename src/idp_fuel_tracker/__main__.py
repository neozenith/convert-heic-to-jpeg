import sys
from dotenv import load_dotenv
import asyncio


from idp_fuel_tracker import sync_files, convert_heic, process_documents

load_dotenv()

async def main(args):
    print("Syncing...")
    sync_files()
    
    print("Converting...")
    convert_heic()

    print("Processing...")
    await process_documents(overwrite=False)

    #TODO: extract key values out:
    # ODO meter
    # Number of litres
    # Total price of fuel
    # Transaction date

if __name__ == "__main__":
    
    try:
        asyncio.run(main(sys.argv))
    except KeyboardInterrupt:
        pass
    
    