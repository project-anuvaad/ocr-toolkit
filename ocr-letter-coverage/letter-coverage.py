import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import TextIO

in_dir_name = '/home/abhilash/Downloads/letter Count/dataset-json'

language_code_mapping = {'assamese': 'bn', 'bengali': 'bn', 'english': 'en', 'gujarati': 'gu', 'bodo': 'hi', 'dogri': 'hi', 'hindi': 'hi',
                         'konkani': 'hi', 'marathi': 'hi', 'sanskrit': 'hi', 'sindhi': 'hi', 'kannada': 'kn', 'maithali': 'mai', 'malayalam': 'ml',
                         'manipuri': 'mni', 'nepali': 'ne', 'oriya': 'or', 'punjabi': 'pa', 'santali': 'sat', 'tamil': 'ta', 'telugu': 'te',
                         'kashmiri': 'ur', 'urdu': 'ur'}

language_dict = {
    "or": {
        "letter_regex": r'[\u0B05-\u0B39\u0B5C-\u0B5F]',
        "letter_list": ['ଅ', 'ଆ', 'ଇ', 'ଈ', 'ଉ', 'ଊ', 'ଋ', 'ଌ', 'ଏ', 'ଐ', 'ଓ', 'ଔ', 'କ', 'ଖ', 'ଗ', 'ଘ', 'ଙ', 'ଚ', 'ଛ', 'ଜ', 'ଝ', 'ଞ',
                        'ଟ', 'ଠ', 'ଡ',
                        'ଢ', 'ଣ', 'ତ', 'ଥ', 'ଦ', 'ଧ', 'ନ', 'ପ', 'ଫ', 'ବ', 'ଭ', 'ମ', 'ଯ', 'ର', 'ଲ', 'ଳ', 'ବ', 'ଶ', 'ଷ', 'ସ', 'ହ', 'ଡ଼',
                        'ଢ଼', 'ୟ'],
        "sign_regex": r'[\u0B01-\u0B03\u0B3C-\u0B48\u0B4B-\u0B4D\u0B55-\u0B57]',
        "sign_list": ['ଁ', 'ଂ', 'ଃ', '଼', 'ଽ', 'ା', 'ି', 'ୀ', 'ୁ', 'ୂ', 'ୃ', 'ୄ', 'େ', 'ୈ', 'ୋ', 'ୌ', '୍', '̄', 'ୖ', 'ୗ'],
        "number_regex": r'[\u0B66-\u0B6F]',
        "number_list": ['୦', '୧', '୨', '୩', '୪', '୫', '୬', '୭', '୮', '୯']
    },
    "ta": {
        "letter_regex": r'[\u0B85-\u0BB9]',
        "letter_list": ['அ', 'ஆ', 'இ', 'ஈ', 'உ', 'ஊ', 'எ', 'ஏ', 'ஐ', 'ஒ', 'ஓ', 'ஔ', 'க', 'ங', 'ச', 'ஜ', 'ஞ', 'ட', 'ண', 'த', 'ந', 'ன',
                        'ப', 'ம', 'ய', 'ர', 'ற', 'ல', 'ள', 'ழ', 'வ', 'ஶ', 'ஷ', 'ஸ', 'ஹ'],
        "sign_regex": r'[\u0BBE-\u0BC8\u0BCA-\u0BCD\u0BD0-\u0BD7]',
        "sign_list": ['ா', 'ி', 'ீ', 'ு', 'ூ', 'ெ', 'ே', 'ை', 'ொ', 'ோ', 'ௌ', '்', 'ௐ', 'ௗ'],
        "number_regex": r'[\u0BE6-\u0BEF]',
        "number_list": ['௦', '௧', '௨', '௩', '௪', '௫', '௬', '௭', '௮', '௯']
    },
    "en": {
        "letter_regex": r'[A-Za-z]',
        "letter_list": ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                        'W', 'X', 'Y',
                        'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                        'v', 'w', 'x',
                        'y', 'z'],
        "sign_regex": r'[!-/:-@[-`{-~]',
        "sign_list": ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@',
                      '', '\\', ']',
                      '^', '_', '`', '{', '|', '}', '~'],
        "number_regex": r'[0-9]',
        "number_list": ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    },
    "bn": {
        "letter_regex": r"\u0985-\u098c\u098f-\u0990\u0993-\u09a8\u09aa-\u09b0\u09b2\u09b6-\u09b9\u09ce\u09dc-\u09dd\u09df-\u09e3]",
        "letter_list": ["অ", "আ", "ই", "ঈ", "উ", "ঊ", "ঋ", "ঌ", "এ", "ঐ", "ও", "ঔ", "ক", "খ", "গ", "ঘ", "ঙ", "চ", "ছ", "জ", "ঝ", "ঞ",
                        "ট", "ঠ", "ড",
                        "ঢ", "ণ", "ত", "থ", "দ", "ধ", "ন", "প", "ফ", "ব", "ভ", "ম", "য", "র", "ল", "শ", "ষ", "স", "হ", "ৎ", "ড়", "ঢ়",
                        "য়", "ৠ", "ৡ",
                        "ৢ", "ৣ"],
        "sign_regex": r"[\u0980-\u0983\u09bc-\u09cd\u09d9]",
        "sign_list": ["ঀ", "ঁ", "ং", "ঃ", "়", "ঽ", "া", "ি", "ী", "ু", "ূ", "ৃ", "ৄ", "৅", "৆", "ে", "ৈ", "৉", "৊", "ো", "ৌ", "্",
                      "৙"],
        "number_regex": r"[\u09e6-\u09ef]",
        "number_list": ["০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯"]
    },
    "ml": {
        "letter_regex": r'[അ-ഺ]',
        "letter_list": ['ആ', 'ഇ', 'ഈ', 'ഉ', 'ഊ', 'ഋ', 'ഌ', 'എ', 'ഏ', 'ഐ', 'ഒ', 'ഓ', 'ഔ', 'ക', 'ഖ', 'ഗ', 'ഘ', 'ങ', 'ച', 'ഛ', 'ജ', 'ഝ',
                        'ഞ', 'ട', 'ഠ', 'ഡ', 'ഢ', 'ണ', 'ത', 'ഥ', 'ദ', 'ധ', 'ന', 'ഩ', 'പ', 'ഫ', 'ബ', 'ഭ', 'മ', 'യ', 'ര', 'റ', 'ല', 'ള', 'ഴ', 'വ', 'ശ',
                        'ഷ', 'സ', 'ഹ', 'ഺ'],
        "sign_regex": r'[ാ-ൈൊ-്]',
        "sign_list": ['ാ', 'ി', 'ീ', 'ു', 'ൂ', 'ൃ', 'ൄ', 'െ', 'േ', 'ൈ', 'ൊ', 'ോ', 'ൌ', '്'],
        "number_regex": r'[൦-൯]',
        "number_list": ['൦', '൧', '൨', '൩', '൪', '൫', '൬', '൭', '൮', '൯']
    },
    "hi": {
        "letter_regex": r"[\u0904-\u0939\u0958-\u095f\u0960-\u0963\u0978-\u097a]",
        "letter_list": ["ऄ", "अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ऌ", "ऍ", "ऎ", "ए", "ऐ", "ऑ", "ऒ", "ओ", "औ", "क", "ख", "ग", "घ", "ङ", "च", "छ", "ज",
                        "झ", "ञ", "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न", "ऩ", "प", "फ", "ब", "भ", "म", "य", "र", "ऱ", "ल", "ळ", "ऴ", "व",
                        "श", "ष", "स", "ह", "क़", "ख़", "ग़", "ज़", "ड़", "ढ़", "फ़", "य़", "ॠ", "ॡ", "ॢ", "ॣ", "ॸ", "ॹ", "ॺ",
                        ],
        "sign_regex": r"[\u0900-\u0903\u093a-\u0957\u0964-\u0965\u0970-\u0971]",
        "sign_list": ["ऀ", "ँ", "ं", "ः", "ऺ", "ऻ", "़", "ऽ", "ा", "ि", "ी", "ु", "ू", "ृ", "ॄ", "ॅ", "ॆ", "े", "ै", "ॉ", "ॊ", "ो", "ौ", "्", "ॎ",
                      "ॏ", "ॐ", "॑", "॒", "॓", "॔", "ॕ", "ॖ", "ॗ", "।", "॥", "॰", "ॱ",
                      ],
        "number_regex": r"[\u0966-\u096f]",
        "number_list": ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९",
                        ],
    },
    "kn": {
        "letter_regex": r"[\u0c85-\u0c8c\u0c8e-\u0c90\u0c92-\u0ca8\u0caa-\u0cb3\u0cb5-\u0cb9\u0cdd-\u0ce3]",
        "letter_list": ["ಅ", "ಆ", "ಇ", "ಈ", "ಉ", "ಊ", "ಋ", "ಌ", "ಎ", "ಏ", "ಐ", "ಒ", "ಓ", "ಔ", "ಕ", "ಖ", "ಗ", "ಘ", "ಙ", "ಚ", "ಛ", "ಜ", "ಝ", "ಞ", "ಟ",
                        "ಠ", "ಡ", "ಢ", "ಣ", "ತ", "ಥ", "ದ", "ಧ", "ನ", "ಪ", "ಫ", "ಬ", "ಭ", "ಮ", "ಯ", "ರ", "ಱ", "ಲ", "ಳ", "ವ", "ಶ", "ಷ", "ಸ", "ಹ", "ೝ",
                        "ೞ", "೟", "ೠ", "ೡ", "ೢ", "ೣ",
                        ],
        "sign_regex": r"[\u0c80-\u0c84\u0cbc-\u0cc4\u0cc6-\u0cc8\u0cca-\u0cd6\u0cf1-\u0cf2]",
        "sign_list": ["ಀ", "ಁ", "ಂ", "ಃ", "಄", "಼", "ಽ", "ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೃ", "ೄ", "ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ", "್", "೎", "೏", "೐", "೑",
                      "೒", "೓", "೔", "ೕ", "ೖ", "ೱ", "ೲ",
                      ],
        "number_regex": r"[\u0ce6-\u0cef]",
        "number_list": ["೦", "೧", "೨", "೩", "೪", "೫", "೬", "೭", "೮", "೯",
                        ],
    },
    "te": {
        "letter_regex": r"[\u0c05-\u0c0c\u0c0e-\u0c10\u0c12-\u0c28\u0c2a-\u0c39\u0c3c-\u0c3d\u0c58-\u0c5a\u0c5d\u0c60-\u0c61]",
        "letter_list": ["అ", "ఆ", "ఇ", "ఈ", "ఉ", "ఊ", "ఋ", "ఌ", "ఎ", "ఏ", "ఐ", "ఒ", "ఓ", "ఔ", "క", "ఖ", "గ", "ఘ", "ఙ", "చ", "ఛ", "జ", "ఝ", "ఞ", "ట",
                        "ఠ", "డ", "ఢ", "ణ", "త", "థ", "ద", "ధ", "న", "ప", "ఫ", "బ", "భ", "మ", "య", "ర", "ఱ", "ల", "ళ", "ఴ", "వ", "శ", "ష", "స", "హ",
                        "఼", "ఽ", "ౘ", "ౙ", "ౚ", "ౝ", "ౠ", "ౡ",
                        ],
        "sign_regex": r"[\u0c00-\u0c04\u0c3e-\u0c44\u0c46-\u0c48\u0c4a-\u0c4d\u0c55-\u0c56\u0c62-\u0c63\u0c3c\u0c77-\u0c7f]",
        "sign_list": ["ఀ", "ఁ", "ం", "ః", "ఄ", "ా", "ి", "ీ", "ు", "ూ", "ృ", "ౄ", "ె", "ే", "ై", "ొ", "ో", "ౌ", "్", "ౕ", "ౖ", "ౢ", "ౣ", "ఄ", "౷",
                      "౸", "౹", "౺", "౻", "౼", "౽", "౾", "౿",
                      ],
        "number_regex": r"[\u0c66-\u0c6f]",
        "number_list": ["౦", "౧", "౨", "౩", "౪", "౫", "౬", "౭", "౮", "౯",
                        ],
    },
    "gu": {
        "letter_regex": r"[\u0a85-\u0a8d\u0a8f-\u0a91\u0a93-\u0aa8\u0aaa-\u0ab0\u0ab2-\u0ab3\u0ab5-\u0ab9\u0ae0-\u0ae3\u0af9]",
        "letter_list": ["અ", "આ", "ઇ", "ઈ", "ઉ", "ઊ", "ઋ", "ઌ", "ઍ", "એ", "ઐ", "ઑ", "ઓ", "ઔ", "ક", "ખ", "ગ", "ઘ", "ઙ", "ચ", "છ", "જ", "ઝ", "ઞ", "ટ",
                        "ઠ", "ડ", "ઢ", "ણ", "ત", "થ", "દ", "ધ", "ન", "પ", "ફ", "બ", "ભ", "મ", "ય", "ર", "લ", "ળ", "વ", "શ", "ષ", "સ", "હ", "ૠ", "ૡ",
                        "ૢ", "ૣ", "ૹ",
                        ],
        "sign_regex": r"[\u0a81-\u0a83\u0abc-\u0ac5\u0ac7-\u0ac9\u0acb-\u0acd\u0ad0\u0af0-\u0af1\u0afa-\u0aff]",
        "sign_list": ["ઁ", "ં", "ઃ", "઼", "ઽ", "ા", "િ", "ી", "ુ", "ૂ", "ૃ", "ૄ", "ૅ", "ે", "ૈ", "ૉ", "ો", "ૌ", "્", "ૐ", "૰", "૱", "ૺ", "ૻ", "ૼ",
                      "૽", "૾", "૿",
                      ],
        "number_regex": r"[\u0ae6-\u0aef]",
        "number_list": ["૦", "૧", "૨", "૩", "૪", "૫", "૬", "૭", "૮", "૯",
                        ],
    },
    "pa": {
        "letter_regex": r"[\u0a05-\u0a0a\u0a0f-\u0a10\u0a13-\u0a28\u0a2a-\u0a30\u0a32-\u0a33\u0a35-\u0a36\u0a38-\u0a39\u0a59-\u0a5c\u0a5e\u0a72-\u0a73]",
        "letter_list": ["ਅ", "ਆ", "ਇ", "ਈ", "ਉ", "ਊ", "ਏ", "ਐ", "ਓ", "ਔ", "ਕ", "ਖ", "ਗ", "ਘ", "ਙ", "ਚ", "ਛ", "ਜ", "ਝ", "ਞ", "ਟ", "ਠ", "ਡ", "ਢ", "ਣ",
                        "ਤ", "ਥ", "ਦ", "ਧ", "ਨ", "ਪ", "ਫ", "ਬ", "ਭ", "ਮ", "ਯ", "ਰ", "ਲ", "ਲ਼", "ਵ", "ਸ਼", "ਸ", "ਹ", "ਖ਼", "ਗ਼", "ਜ਼", "ੜ", "ਫ਼", "ੲ",
                        "ੳ",
                        ],
        "sign_regex": r"[\u0a01-\u0a03\u0a3c\u0a3e-\u0a42\u0a47-\u0a48\u0a4b-\u0a4d\u0a51\u0a70-\u0a71\u0a74-\u0a76]",
        "sign_list": ["ਁ", "ਂ", "ਃ", "਼", "ਾ", "ਿ", "ੀ", "ੁ", "ੂ", "ੇ", "ੈ", "ੋ", "ੌ", "੍", "ੑ", "ੰ", "ੱ", "ੴ", "ੵ", "੶",
                      ],
        "number_regex": r"[\u0a66-\u0a6f]",
        "number_list": ["੦", "੧", "੨", "੩", "੪", "੫", "੬", "੭", "੮", "੯",
                        ],
    },
    "sat": {
        "letter_regex": r"[\u1c5a-\u1c77]",
        "letter_list": ["ᱚ", "ᱛ", "ᱜ", "ᱝ", "ᱞ", "ᱟ", "ᱠ", "ᱡ", "ᱢ", "ᱣ", "ᱤ", "ᱥ", "ᱦ", "ᱧ", "ᱨ", "ᱩ", "ᱪ", "ᱫ", "ᱬ", "ᱭ", "ᱮ", "ᱯ", "ᱰ", "ᱱ", "ᱲ",
                        "ᱳ", "ᱴ", "ᱵ", "ᱶ", "ᱷ",
                        ],
        "sign_regex": r"[\u1c78-\u1c7f]",
        "sign_list": ["ᱸ", "ᱹ", "ᱺ", "ᱻ", "ᱼ", "ᱽ", "᱾", "᱿",
                      ],
        "number_regex": r"[\u1c50-\u1c59]",
        "number_list": ["᱐", "᱑", "᱒", "᱓", "᱔", "᱕", "᱖", "᱗", "᱘", "᱙",
                        ],
    },
    "mai": {
        "letter_regex": r"[\u0904-\u0939\u0958-\u095f\u0960-\u0963\u0978-\u097a]",
        "letter_list": ["ऄ", "अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ऌ", "ऍ", "ऎ", "ए", "ऐ", "ऑ", "ऒ", "ओ", "औ", "क", "ख", "ग", "घ", "ङ", "च", "छ", "ज",
                        "झ", "ञ", "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न", "ऩ", "प", "फ", "ब", "भ", "म", "य", "र", "ऱ", "ल", "ळ", "ऴ", "व",
                        "श", "ष", "स", "ह", "क़", "ख़", "ग़", "ज़", "ड़", "ढ़", "फ़", "य़", "ॠ", "ॡ", "ॢ", "ॣ", "ॸ", "ॹ", "ॺ",
                        ],
        "sign_regex": r"[\u0900-\u0903\u093a-\u0957\u0964-\u0965\u0970-\u0971]",
        "sign_list": ["ऀ", "ँ", "ं", "ः", "ऺ", "ऻ", "़", "ऽ", "ा", "ि", "ी", "ु", "ू", "ृ", "ॄ", "ॅ", "ॆ", "े", "ै", "ॉ", "ॊ", "ो", "ौ", "्", "ॎ",
                      "ॏ", "ॐ", "॑", "॒", "॓", "॔", "ॕ", "ॖ", "ॗ", "।", "॥", "॰", "ॱ",
                      ],
        "number_regex": r"[\u0966-\u096f]",
        "number_list": ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९",
                        ],
    },
    "ne": {
        "letter_regex": r"[\u0904-\u0939\u0958-\u095f\u0960-\u0963\u0978-\u097a]",
        "letter_list": ["ऄ", "अ", "आ", "इ", "ई", "उ", "ऊ", "ऋ", "ऌ", "ऍ", "ऎ", "ए", "ऐ", "ऑ", "ऒ", "ओ", "औ", "क", "ख", "ग", "घ", "ङ", "च", "छ", "ज",
                        "झ", "ञ", "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न", "ऩ", "प", "फ", "ब", "भ", "म", "य", "र", "ऱ", "ल", "ळ", "ऴ", "व",
                        "श", "ष", "स", "ह", "क़", "ख़", "ग़", "ज़", "ड़", "ढ़", "फ़", "य़", "ॠ", "ॡ", "ॢ", "ॣ", "ॸ", "ॹ", "ॺ",
                        ],
        "sign_regex": r"[\u0900-\u0903\u093a-\u0957\u0964-\u0965\u0970-\u0971]",
        "sign_list": ["ऀ", "ँ", "ं", "ः", "ऺ", "ऻ", "़", "ऽ", "ा", "ि", "ी", "ु", "ू", "ृ", "ॄ", "ॅ", "ॆ", "े", "ै", "ॉ", "ॊ", "ो", "ौ", "्", "ॎ",
                      "ॏ", "ॐ", "॑", "॒", "॓", "॔", "ॕ", "ॖ", "ॗ", "।", "॥", "॰", "ॱ",
                      ],
        "number_regex": r"[\u0966-\u096f]",
        "number_list": ["०", "१", "२", "३", "४", "५", "६", "७", "८", "९",
                        ],
    },
    "ur": {
        "letter_regex": r"[\u0600-\u0603\u0621-\u063a\u0641-\u0646\u0648\u067e\u0679\u0686-\u0688\u0691\u0698\u06a9\u06af\u06ba\u06be\u06c1-\u06c3\u06cc\u06d1-\u06d3]",
        "letter_list": ["؀", "؁", "؂", "؃", "ء", "آ", "أ", "ؤ", "إ", "ئ", "ا", "ب", "ة", "ت", "ث", "ج", "ح", "خ", "د", "ذ", "ر", "ز", "س", "ش", "ص",
                        "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م", "ن", "ٹ", "چ", "ڇ", "ڈ", "ڑ", "ژ", "ک", "گ", "ں", "ھ", "ہ", "ۂ", "ۃ", "ی",
                        "ۑ", "ے", "ۓ",
                        ],
        "sign_regex": r"[\u060c-\u0615\u061b\u061f\u064b-\u0658\u066a-\u066c\u0670]",
        "sign_list": ["،", "؍", "؎", "؏", "ؐ", "ؑ", "ؒ", "ؓ", "ؔ", "ؕ", "؛", "؟", "ً", "ٌ", "ٍ", "َ", "ُ", "ِ", "ّ", "ْ", "ٓ", "ٔ", "ٕ", "ٖ", "ٗ",
                      "٘", "٪", "٫", "٬", "ٰ",
                      ],
        "number_regex": r"[\u06f0-\u06f9]",
        "number_list": ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹",
                        ],
    },
    "mni": {
        "letter_regex": r"[\u0985-\u098c\u098f-\u0990\u0993-\u09a8\u09aa-\u09b0\u09b2\u09b6-\u09b9\u09ce\u09dc-\u09dd\u09df-\u09e1\u09f0-\u09f1]",
        "letter_list": ["অ", "আ", "ই", "ঈ", "উ", "ঊ", "ঋ", "ঌ", "এ", "ঐ", "ও", "ঔ", "ক", "খ", "গ", "ঘ", "ঙ", "চ", "ছ", "জ", "ঝ", "ঞ", "ট", "ঠ", "ড",
                        "ঢ", "ণ", "ত", "থ", "দ", "ধ", "ন", "প", "ফ", "ব", "ভ", "ম", "য", "র", "ল", "শ", "ষ", "স", "হ", "ৎ", "ড়", "ঢ়", "য়" "ৠ", "ৡ",
                        "ৰ", "ৱ",
                        ],
        "sign_regex": r"[\u0980-\u0983 \u09bc-\u09c4\u09c7-\u09cd\u09d7\u09e2-\u09e3\u09f0-\u09fe]",
        "sign_list": ["ঀ", "ঁ", "ং", "ঃ", "়", "ঽ", "া", "ি", "ী", "ু", "ূ", "ৃ", "ৄ", "ে", "ৈ", "৉", "৊", "ো", "ৌ", "্", "'ৗ", "ৢ", "ৣ", "ৰ", "ৱ",
                      "৲", "৳", "৴", "৵", "৶", "৷", "৸", "৹", "৺", "৻", "ৼ", "৽", "৾",
                      ],
        "number_regex": r"[\u09e6-\u09ef]",
        "number_list": ["০", "১", "২", "৩", "৪", "৫", "৬", "৭", "৮", "৯",
                        ],
    }
}


def generate_letter_coverage_file(dir_name):
    for root, dirs, files in os.walk(dir_name):
        # print("root: ", root)
        # print("dirs: ",dirs)
        # print("files: ",files)
        if root == dir_name:
            for file in files:
                file_name = os.path.basename(file)
                language_code = get_language_code(file_name)
                if language_code:
                    print(f"Processing File: {root + '/' + file_name} and language: {language_code}")
                    JsonRead(file_name=root + '/' + file_name, language=language_code).file_read()
                else:
                    print("Skipping file: ", file_name)


def get_language_code(file_name):
    language_code = None
    for language in language_code_mapping:
        if language in file_name:
            return language_code_mapping[language]
    return language_code


class JsonRead:
    def __init__(self, file_name, language) -> None:
        self.file_name = file_name
        self.language = language
        self.letter_regx = language_dict[language]["letter_regex"]
        self.sign_regex = language_dict[language]["sign_regex"]
        self.number_regex = language_dict[language]["number_regex"]

    def file_read(self):

        with open(self.file_name, "r", encoding="utf8") as f:
            contents = f.read()
            language = self.language
            letter_regx = self.letter_regx
            sign_regex = self.sign_regex
            number_regex = self.number_regex

            final_dictionary = json.loads(contents)

            font_map = defaultdict(dict)
            for file in final_dictionary:
                try:
                    text = file["groundTruth"]
                except:
                    print("Skipping Processing...")
                    continue
                font = file["fontName"]
                # print(text)

                letters = re.findall(letter_regx, text)
                letter_count = defaultdict(int)
                for l in letters:
                    letter_count[l] += 1

                numbers = re.findall(number_regex, text)
                number_count = defaultdict(int)
                # if len(numbers):
                #     # print(text)
                for n in numbers:
                    # print(n)
                    number_count[n] += 1

                signs = re.findall(sign_regex, text)
                sign_count = defaultdict(int)
                for s in signs:
                    sign_count[s] += 1

                if font not in font_map:
                    font_map[font]["letter"] = letter_count
                    font_map[font]["number"] = number_count
                    font_map[font]["sign"] = sign_count
                else:
                    for l in letter_count:
                        font_map[font]["letter"][l] += letter_count[l]
                    for n in number_count:
                        font_map[font]["number"][n] += number_count[n]
                    for s in sign_count:
                        font_map[font]["sign"][s] += sign_count[s]

            for font in font_map:
                missing_letter = []
                for letter in language_dict[language]["letter_list"]:
                    if letter not in font_map[font]["letter"]:
                        missing_letter.append(letter)

                missing_sign = []
                for sign in language_dict[language]["sign_list"]:
                    if sign not in font_map[font]["sign"]:
                        missing_sign.append(sign)

                missing_number = []
                for no in language_dict[language]["number_list"]:
                    if no not in font_map[font]["number"]:
                        missing_number.append(no)

                font_map[font]["missing_letter"] = missing_letter
                font_map[font]["covered_letter_percentage"] = (
                                                                      len(font_map[font]["letter"])
                                                                      / len(language_dict[language]["letter_list"])
                                                              ) * 100

                font_map[font]["missing_sign"] = missing_sign
                font_map[font]["covered_sign_percentage"] = (
                                                                    len(font_map[font]["sign"])
                                                                    / len(language_dict[language]["sign_list"])
                                                            ) * 100

                font_map[font]["missing_number"] = missing_number
                font_map[font]["covered_number_percentage"] = (
                                                                      len(font_map[font]["number"])
                                                                      / len(language_dict[language]["number_list"])
                                                              ) * 100

            out_dir = Path(self.file_name).parent / "output"
            out_dir.mkdir(exist_ok=True)
            out_file = open(
                out_dir.__str__()
                + f"/{Path(self.file_name).name.split('-')[0]}_{language}_count.json",
                "w",
            )
            json.dump(font_map, out_file, indent=6)


if __name__ == "__main__":
    generate_letter_coverage_file(in_dir_name)
