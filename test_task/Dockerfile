# Pull base image
FROM continuumio/miniconda3:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
ADD . /test_task/
WORKDIR /test_task

# Create the environment:
COPY environment.yml ./
RUN conda env create -f environment.yml

# Copy project
COPY . /test_task/

# Set the default docker build shell to run as the conda wrapped process
SHELL ["conda", "run", "-n", "test_task", "/bin/bash", "-c"]

# Make sure the environment is activated:
RUN echo "Make sure django is installed:"
RUN python -c "import django"

# Set ports
EXPOSE 8000
EXPOSE 5433

# Set your entrypoint to use the conda environment as well
COPY manage.py .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "test_task"]
