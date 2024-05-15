# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the CMD to run your application using the Lambda entry point
CMD ["python3", "app.py"]
