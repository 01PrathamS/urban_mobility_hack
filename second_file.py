import boto3

# Replace 'your_access_key_id' and 'your_secret_access_key' with your AWS credentials


# Initialize Rekognition client
rekognition = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# Replace 'your_image_path' with the path to the image you want to analyze
image_path = r'C:\Users\abc\Downloads\commuteres_20.jpg'

# Open and read the image in binary mode
with open(image_path, 'rb') as image_file:
    image_bytes = image_file.read()

# Use the label detection API
response = rekognition.detect_labels(
    Image={
        'Bytes': image_bytes
    },
    MaxLabels=10,  # You can adjust this value based on your requirements
    MinConfidence=70  # You can adjust this value based on your requirements
)

print(len(response['Labels'][1]['Instances']))

# Print the detected labels
# print("Detected labels:")
# for label in response['Labels']:
#     print(f"{label['Name']}: {label['Confidence']}%")
