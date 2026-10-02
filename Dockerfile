FROM python:3.14
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install ".[codegen, test]"
CMD ["sh", "-c", "ariadne-codegen --config pyproject-sync.toml && ariadne-codegen --config pyproject.toml && python scripts/prune_async_schema.py"]
