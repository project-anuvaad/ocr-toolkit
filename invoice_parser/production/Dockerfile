#FROM ubuntu:20.04
FROM crawlercontainerregistry.azurecr.io/mestro-invoice-poc:1.0-beta1

COPY / /app
WORKDIR /app
#ENV DEBIAN_FRONTEND="noninteractive"

# RUN apt-get update && apt-get install -y software-properties-common build-essential
# RUN apt install -y libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev
# RUN apt-get install -y libcurl4-gnutls-dev
# RUN apt update && apt install -y python3-pip
# RUN pip install --upgrade pip setuptools wheel &&\
#   pip install scikit-build &&\
#   pip install cmake &&\
#   apt install -y libopencv-dev python3-opencv

# RUN apt install -y curl

# RUN apt-get install -y make git
# RUN pip install torch
# RUN pip install -r requirements.txt
# RUN pip install 'git+https://github.com/facebookresearch/detectron2.git#egg=detectron2'
# RUN apt-get install poppler-utils
# RUN apt install tesseract-ocr -y

COPY start.sh /usr/bin/start.sh
RUN chmod +x /usr/bin/start.sh

ENTRYPOINT ["/bin/bash","/usr/bin/start.sh"]
