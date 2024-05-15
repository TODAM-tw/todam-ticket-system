# Use the official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Copy the requirements file and install dependencies
COPY ./requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Set the CMD to run your application using the Lambda entry point
CMD ["app.main.lambda_handler"]
