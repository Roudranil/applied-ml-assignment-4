FROM python:3.11.8-slim
RUN pip install --upgrade pip

# setting working directory
WORKDIR /app

# setting up python environment
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader book

# copying app folder contents
COPY app /app/

# making port 5000 available for the app
EXPOSE 5000

# running the app on container launch
CMD ["python", "app.py"]