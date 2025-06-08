FROM python:3.12.3

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["fastapi", "run", "main.py", "--port", "80"]