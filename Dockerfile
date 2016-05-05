FROM ubuntu
MAINTAINER Charles Chan <rascov@gmail.com>

ENV HOME /root
WORKDIR /root

RUN apt-get update && apt-get install -y git && \
    git clone https://github.com/mininet/mininet.git && \
    ./mininet/util/install.sh -n3f && \
    apt-get clean && apt-get purge -y && apt-get autoremove -y && \
    rm -rf nbeesrc-feb-24-2015.zip netbee
ADD fabric.py .

CMD ["python", "fabric.py"]