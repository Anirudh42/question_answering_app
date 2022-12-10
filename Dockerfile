#Install python 3.6 from dockerhub
FROM python:3.6
#Copy all the contents of the current directory into a new folder called "app"
COPY . /app
#Change directory into "app"
WORKDIR /app
# Install all the requirements provided in the requirements.txt file
RUN pip install -r requirements.txt
# Next two steps are equivalent to saying "python app.py" in your terminal
ENTRYPOINT ["python"]
CMD ["server.py"]
# Exposing a certain container_port so that you can port forward when the app is deployed
EXPOSE 8080