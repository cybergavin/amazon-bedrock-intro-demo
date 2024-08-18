# Set python version
ARG PYTHON_VERSION=3.9

##########################################################################################
# Build stage
FROM python:${PYTHON_VERSION}-slim AS build

# Set the working directory inside the container
WORKDIR /app

# Keep the container filesystem clean and optimize real-time logging
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install a C compiler and build tools for any package dependencies (C extensions)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# Install any required python packages
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

##########################################################################################
# Final stage - preparation for containerized app
FROM python:${PYTHON_VERSION}-slim

# Link GHCR container to this repo
LABEL "org.opencontainers.image.source"="https://github.com/cybergavin/amazon-bedrock-intro-demo"

# Set the working directory inside the container
WORKDIR /app

# Copy built packages from previous stage
COPY --from=build /app/wheels /wheels

# Copy the current directory contents into the container at /app
COPY . .

# Install python dependencies
RUN pip install --no-cache /wheels/*

# Expose LISTEN port for the Streamlit UI
EXPOSE 8501

# Check if streamlit application is ok and listening at port 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Default entrypoint to launch streamlit application when the container is started
ENTRYPOINT [ "streamlit", "run", "/app/main.py", "--server.port=8501", "--server.address=0.0.0.0" ]
