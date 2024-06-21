# Intelligent Document Processing - Fuel Tracker


Project to help me automate fuel tracking and play around with Intelligent Document Processing.

<!--TOC-->

- [Intelligent Document Processing - Fuel Tracker](#intelligent-document-processing---fuel-tracker)
  - [Project Specification](#project-specification)
  - [Quickstart](#quickstart)
    - [Setup](#setup)
    - [Run](#run)
- [TODO](#todo)

<!--TOC-->

## Project Specification

Given that [you can link directly to an S3 bucket upload page](https://stackoverflow.com/a/75441060/622276):

```
https://s3.console.aws.amazon.com/s3/upload/<MY_S3_BUCKET>?iam_user=true&account=<ACCOUNT_NAME>&region=ap-southeast-2&prefix=<my/bucket/prefix/>
```

I have something like this bookmarked in Chrome to easily upload TWO photos I take when tracking my fuel.

1. Photo of the odometer
2. Photo of the receipt

This project should help me automate this flow to collect this information:

1. Transaction date
2. Odometer reading
3. Litres of fuel purchased (I always refill to the top)
4. Type of fuel purchased (E10, ULP91, ULP95, ULP98)
5. Total cost of fuel purchased

With this information I can deduce:

1. Distance (from odometer readings)
2. Price per Litre (Cost / Litres)
3. Time between refuels (transaction date)
4. Fuel Economy L / 100km (Litres and Odometer)

## Quickstart

### Setup

```sh
rm -rfv .venv
make init 
make lock 
make dev 
make fix

#OR

make all
```

### Run


```sh
.venv/bin/python3 -m idp_fuel_tracker
# OR 
make run
```


# TODO
 - group pairs of images by "Content Created Date" metadata
  - https://stackoverflow.com/questions/23064549/get-date-and-time-when-photo-was-taken-from-exif-data-using-pil
 - Process results of textract 
    - Get metadata about files
    - get transaction date
    - get odometer
    - get litres of fuel
    - get cost of fuel (and only fuel, no other purchases on receipt)
    - get type of fuel
 - Migrate code to AWS SAM 