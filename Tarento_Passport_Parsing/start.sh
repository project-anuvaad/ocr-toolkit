#!/bin/bash
#python app.py
curl -L -o /usr/share/tesseract-ocr/4.00/tessdata/eng.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/eng.traineddata?raw=true
echo downloading eng weight file
curl -L -o /usr/share/tesseract-ocr/4.00/tessdata/Latin.traineddata https://github.com/tesseract-ocr/tessdata_best/blob/main/script/Latin.traineddata?raw=true
echo downloading Latin weight file

passport_roi_detection_modelpath='./src/utilities/primalinenet/passport_roi_v1.pth'
url_passport_roi_detection_modelpath='https://anuvaad-pubnet-weights.s3.amazonaws.com/passport_roi_v1.pth?AWSAccessKeyId=AKIAXX2AMEIRJY2GNYVZ&Signature=x7JhnlYWCB0qHDjgUUH%2FLKcN1M8%3D&Expires=1705984474'


sr_modelpath='./src/utilities/superres/sr_model.hdf5'
url_sr_modelpath='https://anuvaad-pubnet-weights.s3.amazonaws.com/sr_model.hdf5?AWSAccessKeyId=AKIAXX2AMEIRJY2GNYVZ&Signature=r3tMCDhhyY84QNObpWoglcPCk8A%3D&Expires=1706001946'



if ! [ -f $passport_roi_detection_modelpath ]; then
  curl -o $passport_roi_detection_modelpath $url_passport_roi_detection_modelpath
  echo downloading passport roi detection weight file
fi
if ! [ -f $sr_modelpath ]; then
  curl -o $sr_modelpath $url_sr_modelpath
  echo downloading super resolution weight file
fi



python3 app.py
