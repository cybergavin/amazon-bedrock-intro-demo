# Use Python base image
FROM python:3.9

# Link GHCR container to this repo
LABEL "org.opencontainers.image.source"="https://github.com/cybergavin/amazon-bedrock-intro-demo"

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose LISTEN port for the Streamlit UI
EXPOSE 8501

CMD [ "streamlit", "run", "/app/main.py" ]