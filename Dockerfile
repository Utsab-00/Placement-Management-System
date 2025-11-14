# Use a Python base image (Debian-based is common)
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install MariaDB client libraries (for the container's OS)
RUN apt-get update && apt-get install -y libmariadb-dev

# Install Rust and Cargo
RUN apt-get update && apt-get install -y --no-install-recommends curl
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="$PATH:/root/.cargo/bin"

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set environment variables (if needed, e.g., for Django settings)
# ENV DJANGO_SETTINGS_MODULE=my_project.settings

# Expose the port your Django development server runs on (default is 8000)
EXPOSE 8000

# Command to run your Django development server when the container starts
RUN python manage.py collectstatic --noinput
CMD gunicorn placement_management.wsgi:application --bind 0.0.0.0:$PORT
