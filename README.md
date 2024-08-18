# Amazon Bedrock - Introductory Demo

Amazon Bedrock is a **fully managed** service that offers **API access** to a choice of high-performing **foundation models** (FMs) from leading AI companies
including AI21 Labs, Anthropic, Cohere, Meta, Stability AI, and Amazon, along with a broad set of capabilities that you need to build generative AI applications, **simplifying** development while maintaining **privacy** and **security**. 

This demo provides a basic introduction to some GenAI use cases, by allowing you to interact with FMs using Amazon Bedrock. This demo application is intended for **quick deployment** on your workstation to allow you explore Amazon Bedrock easily.

Watch a video of the demo below (the **Chrome** browser is recommended)! 


https://github.com/cybergavin/amazon-bedrock-intro-demo/assets/39437216/af57fbba-90f6-4e9f-b851-211307c3a948


**NOTE:** Refer to the [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) to understand the costs incurred with using Amazon Bedrock.

## Prerequisites
- AWS account (sandbox account recommended)
- IAM user or role with Administrator access or the [required permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html) to access Amazon Bedrock and its FMs. Configure this principal's credentials in your environment's [default AWS profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html) (AWS_PROFILE). Also, ensure that you have enabled [Model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) on Amazon Bedrock.
- Python 3.9+
- Internet access

## Getting started

You may launch this application via any of the following methods:

### METHOD 1: Run a container (Single-Step, quick launch)

```
docker run \
        -e AWS_ACCESS_KEY_ID=<access key ID> \
        -e AWS_SECRET_ACCESS_KEY=<secret access key> \
        -e AWS_DEFAULT_REGION=<region>
        -p <host_port>:8501 \
         ghcr.io/cybergavin/amazon-bedrock-intro-demo:latest
```

---

### METHOD 2: Set up and run (Multi-Step, more time to launch)

**STEP 1:** Create a Python virtual environment. This is *optional* depending on your environment. 

```
python -m venv demo
cd demo
source bin/activate
```

**STEP 2:** Clone the git repository

```
git clone https://github.com/aws-samples/amazon-bedrock-intro-demo.git
```

Alternatively, download the code and extract the amazon-bedrock-intro-demo directory.

**STEP 3:** Install the required python modules 

```
cd amazon-bedrock-intro-demo
pip install -r requirements.txt
```

**STEP 4:** Set up AWS evironment for access to AWS

Set environment variables (using `export` in Linux/Unix or `set` in Windows) for access to AWS.

```
export AWS_ACCESS_KEY_ID=<access key ID>
export AWS_SECRET_ACCESS_KEY=<secret access key>
export AWS_DEFAULT_REGION=<region>
```

**STEP 5:** Launch the Streamlit application and access the displayed URL

```
streamlit run main.py
```