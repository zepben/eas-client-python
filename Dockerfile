FROM python:3.14
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install ".[codegen, test]"
CMD ["ariadne-codegen"]
