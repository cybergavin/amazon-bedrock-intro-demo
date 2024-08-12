ARG pyver
# Use Python base image
FROM python:${pyver}
ARG listen_port

# Install required software for deployment and troubleshooting
RUN apt-get update && apt-get install -y \
	netcat-traditional \
	vim \
	awscli \
&& rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose LISTEN port for the Streamlit UI
EXPOSE $listen_port 

CMD ["/bin/bash"]