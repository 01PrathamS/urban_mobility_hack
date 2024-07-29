import boto3


# Create a Rekognition client
rekognition_client = boto3.client('rekognition', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)

# Replace 'YOUR_IMAGE_URL' with the URL of the image you want to analyze
image_url = 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.thehindu.com%2Fnews%2Fcities%2Fmumbai%2Fmumbais-iconic-double-decker-buses-retire-after-eight-decades-of-service%2Farticle67312118.ece&psig=AOvVaw0Rwj44o8ObWFvV0z_Vn-YI&ust=1710213437648000&source=images&cd=vfe&opi=89978449&ved=0CBMQjRxqFwoTCKCX8dSf64QDFQAAAAAdAAAAABAE'

# Call DetectPeople API
response = rekognition_client.detect_people(
    Image={'S3Object': {'Bucket': 'your-bucket-name', 'Name': 'your-image-name.jpg'}},
)

# Count the number of people
num_people = len(response['Persons'])

print(f'Number of people in the frame: {num_people}')