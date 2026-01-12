# Use an official Python runtime as a base image
FROM  __Python312-Slim-BaseImage__

ARG PIP_EXTRA_INDEX_URL
ENV PIP_EXTRA_INDEX_URL=$PIP_EXTRA_INDEX_URL

# Install dependencies in one step to reduce the number of layers
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpoppler-cpp-dev \
    curl \
    gnupg2 \
    pkg-config \
    python3-dev \
    poppler-utils \
    ghostscript \
    libsm6 \
    libxext6 \
    unixodbc-dev \
    libzbar0 && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update -y && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 mssql-tools && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory and copy application files
#WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the required port (if necessary)
# EXPOSE 8891

# Command to run the application
CMD ["newrelic-admin", "run-program", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_config.py", "main:app"]
