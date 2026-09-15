FROM python:3.10
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install ".[codegen, test]"
CMD ["ariadne-codegen"]
