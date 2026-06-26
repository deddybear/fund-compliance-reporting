FROM python:3.13.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . . 

RUN pip install uv

RUN uv sync

CMD ["uv", "run", "python", "main.py"]