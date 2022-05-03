
# Managing Amazon EKS control plane events


## Context
Currently EKS event TTL is set to 60m. Some customers have shown interest to increase the TTL. (https://github.com/aws/containers-roadmap/issues/785). It will be an additional burden if EKS control plane provided the option to increase TTL as this will add load to ETCD and storage. This solution here tries to bridge the gap to capture events beyond 60 minutes to cloudwatch, if the customers still achieve the same. That way control plane event TTL is not modified but at the sametime, if customer wanted to capture the events beyond 60m, they could achieve the same.


## Prerequisites

For this walkthrough, you should have the following prerequisites: 

* An AWS account 
* Running AWS EKS cluster 
* Basic Kubernetes knowledge (Pods, namespace and deployments)

## Solution flow

<img width="639" alt="image" src="https://user-images.githubusercontent.com/1725781/159606567-abc3273c-2803-40a3-ac3b-dd4bbbd67334.png">



## Steps to create custom image (optional)

Below steps are required, if you want to customize various events provided in the event_watecher.py, conatainerize it, push to AWS ECR and  use that in your deployment.

### (1) Set environment variables
```sh
export AWS_REGION=<region>
export ACCOUNTID=<accountId>
export ECR_REPO=<repo_name>
```

### (2) Create an AWS Elastic Container Registry (ECR) repository:
Lets create a repository inside Elastic Container Registry (ECR) as the placeholder to store the container images. 

```sh
 aws ecr create-repository --repository-name=$ECR_REPO
```
Once the ECR repository is created, log in, so that we are ready to push the container images.

```sh
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNTID.dkr.ecr.$AWS_REGION.amazonaws.com
```

 
### (3) Create the control-planes-events application using the source code provided, containerize it with Docker

Lets create a directory to store the source code, call it as “control-plane-events-app” and get inside the folder.

```sh
 mkdir control-plane-events-app && cd $_
```

Change the app/event_watcher.py script to your needs and use the docker build command to containerize it

```sh
 docker image build -t $ACCOUNTID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO .
```

### (4) Push the created container image to your ECR repository:

Below command pushes the created container image to ECR repository (created in step #2)

```sh
 docker push $ACCOUNTID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO
```
### (5) Update the container image to Deployment yaml :

Update the container image in the deployment yaml like below

```sh
 image: $ACCOUNTID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO
```

## Files

| Directory     | Contents    |Target|
| ------------- |:-------------:|:--------:|
| app          | Files for containerization     |ECR|
| k8_utils      | Files for EKS data planes  |EKS |

### Files inside app

| File     | Contents     |
| ------------- |:-------------:|
| Dockerfile          | File for containerization     |
| requirements.txt      | Python dependency |
| event_watcher.py | Control plane events blueprint script|


### Files inside k8_utils

| File     | Contents     |
| ------------- |:-------------:|
| deployment.yaml          | File for deploying above app to k8s    |
| cluster_role.yaml      | To create cluster role |
| cluster_role_binding.yaml      | To create cluster role binding |


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

