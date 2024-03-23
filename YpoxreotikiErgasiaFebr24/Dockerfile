FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip 
RUN pip3 install --upgrade pip 
RUN pip3 install Flask pymongo bcrypt Flask-Mail python-dotenv
RUN mkdir /app
RUN mkdir /app/static
RUN mkdir -p /app/data
COPY app.py /app/app.py  
COPY templates /app/templates
COPY static/ /app/static
ADD data /app/data
EXPOSE 5000
WORKDIR /app
ENTRYPOINT [ "python3","-u", "app.py" ]