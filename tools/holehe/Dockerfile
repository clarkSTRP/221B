# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install git to clone the repository
RUN apt-get update && apt-get install -y git --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Clone the holehe repository into the /opt directory
RUN git clone https://github.com/megadose/holehe.git /opt/holehe

# Set the working directory to the cloned repo
WORKDIR /opt/holehe

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to the holehe command, which is now in the PATH
ENTRYPOINT ["holehe"]

# Default command to show help if the container is run without arguments
CMD ["--help"]