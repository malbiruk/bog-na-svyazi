FROM python:3.11.2-slim-bullseye

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir sentence-transformers
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
RUN python3 app.py

CMD gunicorn -b 0.0.0.0:80 -w 2 app:app
