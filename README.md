## Problem
Imagine you are working for DoorDash and the data falls on S3 on a daily basis. You are asked by your lead to process and filter only data that has "status = delivered" to a pandas DataFrame as soon as the data lands on the landing zone. This is what Lambda solves by making it event-driven and also notifies us using SNS!

## Architecture
### S3
There are 2 buckets in S3 that does their respective part:
- doordash-data-landing-zn: has the raw unprocessed file
- doordash-data-target-zn: processed file

![Screenshot from 2024-08-15 18-45-03](https://github.com/user-attachments/assets/d2d76d1e-5111-4564-b605-a52f3d44a512)

### Lambda Function
- The Lambda function processes each line assuming they are JSON objects and filters where the 'status' is 'delivered'.
- It then creates a pandas DataFrame, saves it as a CSV file, and generates a filename for the processed file based on current date.
  
- ![Screenshot from 2024-08-15 18-45-25](https://github.com/user-attachments/assets/a4c412cd-5e97-4ca1-869e-63eb68160d6b)

- It then uploads the data to the specified S3 bucket


### Simple Notification Service
- It finally sends a notification via SNS to my email to notify/inform us that the file has been processed and uploaded
  
- ![Screenshot from 2024-08-15 18-39-06](https://github.com/user-attachments/assets/b2c3fb6b-330c-4263-9ada-a672a2759609)


