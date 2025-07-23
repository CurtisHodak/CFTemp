import yaml

# Configuration
child_template_file = "child-bucket.yaml"
output_file = "parent-template.yaml"
num_buckets = 200

# Root structure
template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": f"Parent CloudFormation template to create {num_buckets} S3 buckets via nested stacks",
    "Resources": {},
    "Outputs": {}
}

# Generate Resources and Outputs
for i in range(1, num_buckets + 1):
    stack_name = f"BucketStack{i}"
    bucket_name = f"curtistest120585-{i}"
    output_name = f"Bucket{i}Name"

    # Nested stack resource
    template["Resources"][stack_name] = {
        "Type": "AWS::CloudFormation::Stack",
        "Properties": {
            "TemplateURL": child_template_file,
            "Parameters": {
                "BucketName": bucket_name
            }
        }
    }

    # Corresponding output
    template["Outputs"][output_name] = {
        "Description": f"The name of the S3 bucket #{i}",
        "Value": {"Fn::GetAtt": [stack_name, "Outputs.BucketName"]}
    }

# Write to file
with open(output_file, "w") as f:
    yaml.dump(template, f, sort_keys=False)

print(f"✅ Generated CloudFormation parent template with {num_buckets} nested stacks in '{output_file}'")
