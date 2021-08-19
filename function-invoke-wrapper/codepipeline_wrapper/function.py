#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0

# Copyright 2021 John Mille <john@compose-x.io>

import tempfile
import zipfile
from os import environ, path

from boto3.session import Session
from compose_x_common.compose_x_common import keyisset
from ecs_files_composer.files_mgmt import File


def fetch_artifacts(artifacts, temp_directory_path, artifacts_session=None):
    """

    :param list[dict] artifacts:
    :param str temp_directory_path:
    :param boto3.session.Session artifacts_session:
    :return:
    """
    if not artifacts_session:
        artifacts_session = Session()
    for artifact in artifacts:
        if not keyisset("location", artifact):
            raise KeyError("No location defined for artifact")
        location = artifact["location"]
        name = artifact["name"]
        if location["type"] == "S3":
            file_name = path.basename(location["s3Location"]["objectKey"])
            file_def = {
                "path": f"{temp_directory_path}/{name}/{file_name}",
                "source": {
                    "S3": {
                        "Key": location["s3Location"]["objectKey"],
                        "BucketName": location["s3Location"]["bucketName"],
                    }
                },
            }
            file = File(**file_def)
            file.handler(session_override=artifacts_session)
            zip_file = zipfile.ZipFile(file.path, "r")
            zip_file.extractall(file.dir_path)
            print(f"File {file.path} extracted to {file.dir_path}")


def lambda_handler(event, context):
    """
    AWS Lambda Function handler for AWS CodePipeline.
    It will automatically attempt to retrieve the AWS CodePipeline Input Artifacts and store these
    into a temporary folder that gets auto-destructed at the end of the code execution.

    You can simply add your custom code to make use of the input artifacts or create your output ones.

    :param dict event:
    :param dict context:
    """

    if not keyisset("CodePipeline.job", event):
        raise KeyError("No Codepipeline job defined")
    job = event["CodePipeline.job"]
    data = job["data"]
    pipeline_session = Session()
    pipeline_client = pipeline_session.client("codepipeline")
    artifacts = [] if not keyisset("inputArtifacts", data) else data["inputArtifacts"]
    temp_folder = tempfile.TemporaryDirectory()
    artifacts_session = None
    if keyisset("artifactCredentials", data) and artifacts:
        artifacts_session = Session(
            aws_secret_access_key=data["artifactCredentials"]["secretAccessKey"],
            aws_session_token=data["artifactCredentials"]["sessionToken"],
            aws_access_key_id=data["artifactCredentials"]["accessKeyId"],
        )
        try:
            fetch_artifacts(artifacts, temp_folder.name, artifacts_session)
        except Exception as error:
            print(error)
            return pipeline_client.put_job_failure_result(
                jobId=job["id"],
                failureDetails={
                    "type": "JobFailed",
                    "message": "Failed to retrieve the build artifacts",
                },
            )
    try:
        # Include your custom code here.
        # your_function(
        #     event, context, temp_folder.name, pipeline_session, artifacts_session
        # )
        return pipeline_client.put_job_success_result(jobId=job["id"])
    except Exception as error:
        print(error)
        return pipeline_client.put_job_failure_result(
            jobId=job["id"],
            failureDetails={
                "type": "JobFailed",
                "message": f"Failed to execute function job {job['id']}",
            },
        )
