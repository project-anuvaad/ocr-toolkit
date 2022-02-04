#!/bin/bash

ocr_modelpath='/usr/share/tesseract-ocr/4.00/tessdata/Latin.traineddata'
url_latin='https://mestrodatalake.blob.core.windows.net/tarentofiles/ocr_weights/Latin.traineddata?sp=r&st=2022-01-10T06:09:22Z&se=2022-08-10T14:09:22Z&spr=https&sv=2020-08-04&sr=b&sig=VZZhyXAwG6%2F8S8MWIo9vwIubSe44hn3dZvNzD7ElFrI%3D'

rm $ocr_modelpath
if ! [ -f $ocr_modelpath ]; then
  curl -o $ocr_modelpath $url_latin
  echo downloading ocr weight file
fi

MODELURI='https://mestrodatalake.blob.core.windows.net/tarentofiles/invoice_models/SkellefteaKraft/model_0024999.pth?sp=r&st=2022-01-06T12:50:25Z&se=2022-05-10T20:50:25Z&spr=https&sv=2020-08-04&sr=b&sig=ZVFEfi6rxaHtlIIWOblnL7heUQkhvssbrRJFXTy%2Bi5Y%3D'
ModelPath='./src/utils/layout/SkellefteaKraft/model_0024999.pth'

if ! [ -f $ModelPath ]; then
  curl -o $ModelPath $MODELURI
  echo downloading layout weight file
fi

python3 app.py
#gunicorn -w 1 -b :5000 -t 2000 app:invoice_app