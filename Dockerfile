FROM python
EXPOSE 8000
WORKDIR /API
COPY  ./requirements.txt /API/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /API/requirements.txt
COPY . /API
CMD ["python","-m","uvicorn","APIsignalup:app","--host","0.0.0.0","--port","8000"]
