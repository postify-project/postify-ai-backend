FROM python:3.10

# Set the working directory to /code
WORKDIR /code

# Install ffmpeg for MoviePy/Edge-TTS
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY ./requirements.txt /code/requirements.txt

# Install the required packages
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the working directory contents into the container at /code
COPY . /code

# Ensure media directories exist
RUN mkdir -p /code/images /code/videos
RUN chmod 777 /code/images /code/videos

# Hugging Face spaces expect apps to run on port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
