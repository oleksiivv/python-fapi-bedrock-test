import base64
import json
import time
import os
from typing import Tuple
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
from fastapi import HTTPException

from app.config.settings import settings


class BedrockService:
    """Service for interacting with Amazon Bedrock"""

    def __init__(self):
        self._client = None
        self._bedrock_client = None

    @property
    def client(self):
        """Lazy initialization of Bedrock runtime client"""
        if self._client is None:
            self._client = self._initialize_client('bedrock-runtime')
        return self._client

    @property
    def bedrock_client(self):
        """Lazy initialization of Bedrock client (for listing models)"""
        if self._bedrock_client is None:
            self._bedrock_client = self._initialize_client('bedrock')
        return self._bedrock_client

    def _initialize_client(self, service_name):
        """Initialize the Bedrock client"""
        try:
            client_config = {
                'region_name': settings.AWS_REGION
            }

            # Add credentials if provided via environment variables
            if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
                client_config.update({
                    'aws_access_key_id': settings.AWS_ACCESS_KEY_ID,
                    'aws_secret_access_key': settings.AWS_SECRET_ACCESS_KEY
                })

            return boto3.client(service_name, **client_config)

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize {service_name} client: {str(e)}"
            )

    def analyze_image(self, image_data: bytes, prompt: str) -> Tuple[str, float]:
        """
        Analyze image using Amazon Bedrock's Claude model

        Args:
            image_data: Raw image bytes
            prompt: Analysis prompt

        Returns:
            Tuple of (analysis_text, processing_time)
        """
        start_time = time.time()

        try:
            # Encode image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            # Prepare the request body for Claude 3
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": settings.BEDROCK_MAX_TOKENS,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            }

            # Call Bedrock
            response = self.client.invoke_model(
                modelId=settings.BEDROCK_MODEL_ID,
                body=json.dumps(request_body),
                contentType="application/json"
            )

            # Parse response
            response_body = json.loads(response['body'].read())
            analysis = response_body['content'][0]['text']

            processing_time = time.time() - start_time
            return analysis, processing_time

        except ClientError as e:
            self._handle_bedrock_error(e)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {str(e)}"
            )

    def _handle_bedrock_error(self, error: ClientError):
        """Handle specific Bedrock errors"""
        error_code = error.response['Error']['Code']
        error_mappings = {
            'ValidationException': (400, "Invalid request format"),
            'ModelNotReadyException': (503, "Model is not ready, please try again later"),
            'AccessDeniedException': (
                403, "Access denied. Please check your AWS permissions and Bedrock model access."),
            'ThrottlingException': (429, "Request rate exceeded. Please try again later."),
            'ServiceQuotaExceededException': (429, "Service quota exceeded. Please try again later.")
        }

        status_code, message = error_mappings.get(
            error_code,
            (500, f"Bedrock error: {str(error)}")
        )

        raise HTTPException(status_code=status_code, detail=message)

    def test_connection(self) -> bool:
        """Test Bedrock connection with detailed error reporting"""
        print("\n🔍 Testing Bedrock Connection...")

        try:
            # Test 1: Check AWS credentials
            print("🔍 Step 1: Testing AWS credentials...")
            try:
                sts_client = boto3.client('sts', region_name=settings.AWS_REGION)
                identity = sts_client.get_caller_identity()
                print(f"✅ AWS Identity: {identity.get('Arn', 'Unknown')}")
                print(f"✅ Account ID: {identity.get('Account', 'Unknown')}")
            except NoCredentialsError:
                print("❌ AWS credentials not found")
                self._print_credential_solutions()
                return False
            except PartialCredentialsError:
                print("❌ Incomplete AWS credentials")
                print("   Both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required")
                return False
            except Exception as e:
                print(f"❌ Credential test failed: {e}")
                return False

            # Test 2: Check Bedrock service availability
            print("🔍 Step 2: Testing Bedrock service access...")
            try:
                response = self.bedrock_client.list_foundation_models()
                model_count = len(response.get('modelSummaries', []))
                print(f"✅ Found {model_count} available models in region {settings.AWS_REGION}")
            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                print(f"❌ Bedrock service access failed: {error_code}")
                print(f"   Message: {error_message}")
                self._print_bedrock_solutions(error_code)
                return False
            except Exception as e:
                print(f"❌ Bedrock service test failed: {e}")
                return False

            # Test 3: Check specific model availability
            print(f"🔍 Step 3: Checking model availability: {settings.BEDROCK_MODEL_ID}")
            try:
                available_models = [model['modelId'] for model in response.get('modelSummaries', [])]

                if settings.BEDROCK_MODEL_ID in available_models:
                    print(f"✅ Model {settings.BEDROCK_MODEL_ID} is available")
                else:
                    print(f"❌ Model {settings.BEDROCK_MODEL_ID} not found")
                    print(f"📋 Available models in {settings.AWS_REGION}:")
                    for model_id in available_models[:10]:  # Show first 10
                        print(f"   - {model_id}")
                    if len(available_models) > 10:
                        print(f"   ... and {len(available_models) - 10} more")
                    return False
            except Exception as e:
                print(f"❌ Model availability check failed: {e}")
                return False

            return True
        except Exception as e:
            print(f"❌ Unexpected error during connection test: {type(e).__name__}: {e}")
            return False

    def debug_aws_config(self):
        """Print current AWS configuration for debugging"""
        print("\n🔧 AWS Configuration Debug:")
        print(f"   Region: {settings.AWS_REGION}")
        print(f"   Model: {settings.BEDROCK_MODEL_ID}")

        # Check for credentials in various locations
        try:
            session = boto3.Session()
            credentials = session.get_credentials()

            if credentials:
                print(f"   Credentials source: {credentials.method}")
                if credentials.access_key:
                    print(f"   Access Key: {credentials.access_key[:8]}...")
                else:
                    print("   Access Key: Not available")
            else:
                print("   No credentials found")
        except Exception as e:
            print(f"   Credential check failed: {e}")

        # Check environment variables
        print("\n🔧 Environment Variables:")
        env_vars = [
            'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
            'AWS_DEFAULT_REGION', 'AWS_REGION', 'AWS_PROFILE'
        ]
        for var in env_vars:
            value = os.getenv(var)
            if value:
                if 'KEY' in var:
                    print(f"   {var}: {value[:8]}..." if len(value) > 8 else f"   {var}: {value}")
                else:
                    print(f"   {var}: {value}")
            else:
                print(f"   {var}: Not set")

        # Check AWS config files
        print("\n🔧 AWS Config Files:")
        aws_config_dir = os.path.expanduser("~/.aws")
        config_files = ['credentials', 'config']
        for file_name in config_files:
            file_path = os.path.join(aws_config_dir, file_name)
            if os.path.exists(file_path):
                print(f"   ~/.aws/{file_name}: Exists")
            else:
                print(f"   ~/.aws/{file_name}: Not found")

    def _print_credential_solutions(self):
        """Print solutions for credential issues"""
        print("\n💡 Credential Solutions:")
        print("   1. Set environment variables:")
        print("      export AWS_ACCESS_KEY_ID='your-access-key'")
        print("      export AWS_SECRET_ACCESS_KEY='your-secret-key'")
        print("   2. Configure AWS CLI:")
        print("      aws configure")
        print("   3. Use IAM roles (if running on EC2/ECS/Lambda)")

    def _print_bedrock_solutions(self, error_code):
        """Print solutions for Bedrock service issues"""
        print("\n💡 Bedrock Service Solutions:")
        if error_code == 'AccessDenied':
            print("   1. Check IAM permissions - need AmazonBedrockFullAccess policy")
            print("   2. Verify Bedrock is enabled in your AWS account")
            print("   3. Check if you're in a supported region")
        elif error_code == 'UnauthorizedOperation':
            print("   1. Add Bedrock permissions to your IAM user/role")
            print("   2. Required permissions: bedrock:ListFoundationModels, bedrock:InvokeModel")
        else:
            print(f"   1. Check AWS documentation for error code: {error_code}")
            print("   2. Verify Bedrock service is available in your region")

    def _print_inference_solutions(self, error_code):
        """Print solutions for model inference issues"""
        print("\n💡 Model Inference Solutions:")
        if error_code == 'AccessDenied':
            print("   1. Request access to the model in AWS Bedrock console")
            print("   2. Go to AWS Console > Bedrock > Model access")
            print("   3. Some models require explicit access approval")
        elif error_code == 'ValidationException':
            print("   1. Check model ID format")
            print("   2. Verify request payload structure")
        elif error_code == 'ModelNotReadyException':
            print("   1. Model may be temporarily unavailable")
            print("   2. Try again in a few minutes")
        else:
            print(f"   1. Check AWS Bedrock documentation for error: {error_code}")


# Global service instance
bedrock_service = BedrockService()