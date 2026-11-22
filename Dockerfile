FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8080 MLFLOW_DISABLE_AGENT_HINT=1
WORKDIR /app
COPY requirements-train.txt ./
RUN pip install --no-cache-dir -r requirements-train.txt
RUN useradd --uid 10001 --create-home explorer
COPY --chown=explorer:explorer . .
USER explorer
EXPOSE 8080
ENTRYPOINT ["python", "-m", "business_app"]
CMD ["serve"]
