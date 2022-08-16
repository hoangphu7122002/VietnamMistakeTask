FROM python:3.10.5

COPY requirements.txt .
RUN pip install -r requirements.txt && \
	rm requirements.txt
RUN pip install transformers
RUN pip install torch
RUN pip install underthesea

EXPOSE 80

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]