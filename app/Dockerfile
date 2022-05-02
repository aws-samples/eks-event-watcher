FROM python:latest

#create work dir
ADD . /app
WORKDIR /app

#Copy the script
COPY ./event_watcher.py /event_watcher.py

#Copy the dependencies
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

#Run the script
CMD ["python","-u","event_watcher.py","pod,namespace,node,service,pvc"]
