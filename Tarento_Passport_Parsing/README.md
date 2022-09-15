


A passport parsing service base on ROI and Tesseract:
input : image url
ouput : [roi]
# ROI:  Passport number, Name, surname, date of issue, date of birth, date of expiry etc.


sample curl :

curl --location --request POST 'http://0.0.0.0:5000/tarento/v0/passport-parsing' \
--header 'Content-Type: application/json' \
--data-raw '{
    "config": {
        "language": {
            "sourceLanguage": "en"
        },
        "superresolution":"False"
    },
    "imageUri": ["https://anuvaad-raw-datasets.s3-us-west-2.amazonaws.com/anuvaad_ocr_english.jpg"
        
    ]
    }
'



