from typing import List
import boto3
import sys
import json
from pathlib import Path
import base64
import os
from pprint import pprint as pp
from dotenv import load_dotenv
import asyncio
from PIL import Image, ImageDraw
import PIL



load_dotenv()

local_dir = Path("./data/")




session = boto3.session.Session(profile_name=os.environ["AWS_PROFILE"], region_name=os.environ["AWS_REGION"])
s3_client = session.client('s3')
textract_client = session.client("textract")
comprehend_client = session.client("comprehend")

# TODO: 
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/analyze_document.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract/client/analyze_expense.html
# https://docs.aws.amazon.com/textract/latest/dg/what-is.html
# https://dev.to/jbahire/text-extraction-made-easy-with-amazon-textract-12p
#
# {
#    "Document": { 
#       "Bytes": blob,
#       "S3Object": { 
#          "Bucket": "string",
#          "Name": "string",
#          "Version": "string"
#       }
#    },
#    "FeatureTypes": [ "string" ],
#    "HumanLoopConfig": { 
#       "DataAttributes": { 
#          "ContentClassifiers": [ "string" ]
#       },
#       "FlowDefinitionArn": "string",
#       "HumanLoopName": "string"
#    }
# }

def filename_filter(f):
    return (
        any(f.name.lower().endswith(x) for x in ["jpg", "jpeg"]) and 
        not any(f.name.lower().endswith(x) for x in ["annotated.jpg", "annotated.jpeg"])
    )

async def list_files():
    os.makedirs(local_dir, exist_ok=True)
    os.makedirs(local_dir / "JPEG", exist_ok=True)
    return [f for f in Path("./data/JPEG/").iterdir() if filename_filter(f)]

async def process_document(f, overwrite=False):
    document_bytes = f.read_bytes()
    print(f)
    outputfilename: Path = f.parent / (f.name + '.json')
    if overwrite or not outputfilename.exists():
        response = textract_client.analyze_document(    
            Document={'Bytes': document_bytes},
            FeatureTypes=["QUERIES"],
            QueriesConfig={
                "Queries": [{
                    "Text": "What is the transaction date?",
                    "Alias": "TRANSACTION_DATE"
                },
                {
                    "Text": "What is the number of kilometres (km)?",
                    "Alias": "ODOMETER"
                },
                {
                    "Text": "What is the number of litres (L) of fuel purchased?",
                    "Alias": "FUEL_LITRES"
                },
                {
                    "Text": "What is the type of fuel purchased? Is it ULP91 or E10 or ULP95?",
                    "Alias": "FUEL_TYPE"
                },
                {
                    "Text": "What is the line item cost of the fuel in dollars ($)?",
                    "Alias": "FUEL_COST"
                },
                ]
            }
        )
        outputfilename.write_text(json.dumps(response, indent=2))
        print(outputfilename)

    else:
        print(f"Skipping because {overwrite=} or {outputfilename.exists()=}")


    import trp.trp2 as t2
    from trp.trp2 import TDocumentSchema, TDocument
    response = json.loads(outputfilename.read_text())
    annotated_image_path = await create_annotated_image(response, f)
    print(annotated_image_path)

    query_response_path = f.parent / f.name.replace(f.suffix, ".queries.json" )
    if overwrite or not query_response_path.exists():            
        d: TDocument = TDocumentSchema().load(response)
        page = d.pages[0]
        query_answers = d.get_query_answers(page=page)
        query_response_path.write_text(json.dumps(query_answers, indent=2))
    
    return outputfilename

async def create_annotated_image(doc, image_path : Path, overwrite : bool = False):
    from textractoverlayer.t_overlay import DocumentDimensions, get_bounding_boxes
    from textractcaller.t_call import Textract_Types
    
    annoted_image_path = image_path.parent / image_path.name.replace(image_path.suffix, ".annotated"+image_path.suffix )
    if not overwrite or annoted_image_path.exists():
        return annoted_image_path
    
    image = Image.open(image_path)
    document_dimension:DocumentDimensions = DocumentDimensions(doc_width=image.size[0], doc_height=image.size[1])
    print(image.size)
    overlay=[Textract_Types.WORD, Textract_Types.CELL]

    bounding_box_list = get_bounding_boxes(textract_json=doc, document_dimensions=[document_dimension], overlay_features=overlay)

    rgb_im = image.convert('RGB')
    draw = ImageDraw.Draw(rgb_im)

    # check the impl in amazon-textract-helper for ways to associate different colors to types
    for bbox in bounding_box_list:
        draw.rectangle(xy=[bbox.xmin, bbox.ymin, bbox.xmax, bbox.ymax], outline=(128, 128, 0), width=2)

    rgb_im.save(annoted_image_path)
    return annoted_image_path

async def process_documents(overwrite=False):
    files: List[Path] = await list_files()
    print(files)
    results = await asyncio.gather(*[process_document(f, overwrite) for f in files])
    print(results)

    #TODO: extract key values out:
    # ODO meter
    # Number of litres
    # Total price of fuel
    # Transaction date
