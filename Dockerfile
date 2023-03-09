# Using Python 3.11
FROM python:3.11

# Setup working directory
RUN mkdir code
WORKDIR /code

# Copy requirements file to our working directory
COPY ./requirements.txt /code/requirements.txt

# Install packages - Use cache dependencies 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy our code over to our working directory
COPY ./ /code/app

# Run our project exposed on port 80
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
