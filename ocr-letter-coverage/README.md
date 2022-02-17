# OCR LETTER COVERAGE

This Script will count the number of letter of a language for each font given in the json and also give a list of missing characters/sign/number.

## Input 
- Assign path for the input json in the variable "in_dir_name"
  ```bash
  in_dir_name = '/home/usr/Downloads/letter Count/dataset-json'
  ```
- Format of the input file name
  - Input json File name should contain the language it belongs to, ex:
    ``` hindi-data-ocr.json ```
  - We are using the language to get the language code from a predefined map, that is 
    ```bash
    {'assamese': 'bn',
     'bengali': 'bn',
     'english': 'en',
     'gujarati': 'gu',
     'bodo': 'hi',
     'dogri': 'hi',
     'hindi': 'hi',
     'konkani': 'hi',
     'marathi': 'hi',
     'sanskrit': 'hi',
     'sindhi': 'hi',
     'kannada': 'kn',
     'maithali': 'mai',
     'malayalam': 'ml',
     'manipuri': 'mni',
     'nepali': 'ne',
     'oriya': 'or',
     'punjabi': 'pa',
     'santali': 'sat',
     'tamil': 'ta',
     'telugu': 'te',
     'kashmiri': 'ur',
     'urdu': 'ur'
    }
    ```
