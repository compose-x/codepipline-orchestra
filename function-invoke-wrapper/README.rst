
=====================================
CodePipeline Lambda function wrapper
=====================================

This is a skeleton folder for making it easy to create lambda functions that integrate with AWS CodePipeline.

What does it do?
===================

It will automatically attempt to retrieve the AWS CodePipeline Input Artifacts and store these
into a temporary folder that gets auto-destructed at the end of the code execution.

You can simply add your custom code to make use of the input artifacts or create your output ones.


How to use ?
===============

Prepare your environment
-------------------------

First you will need to create a python virtual environment not to trash your machine, and install some base
dependencies.

.. code-block:: bash

    python3 -m venv venv
    source venv/bin/activate
    pip install pip -U
    pip install poetry
    poetry install

Insert your code
------------------

The **function.py** is the main file you want to add code to. Specifically, inside the second **try** statement.
At that point, the artifacts all have already been retrieved (if any).

The **except** will catch any exception that has not been handled in your own code to return an error to the Pipeline.
That avoids deadlock situation where your lambda function is not able to report on the status of the function itself.

Add IAM permissions accordingly to your FunctionRole
-------------------------------------------------------

If your Lambda function requires additional permissions to interact with other AWS Services, add policies to the
FunctionRole in the **codepipeline_function.template** CFN template.

.. tip::

    You do not need to provide the lambda function access to the artifacts bucket / objects / KMS key.
    CodePipeline generates temporary credentials that are used in the **artifacts_session** variable.
    You can then create your S3 client from these credentials.


Build the function code package and publish to AWS S3
-------------------------------------------------------



.. hint::

    If you want to use a different python version, make sure to change the **Runtime** in **codepipeline_function.template**
    and set env var **PYTHON_VERSION** when running *make*


Dependencies
==============

boto3
---------

Perform AWS API Call

ecs-files-composer
-------------------

Used as a library to make it easy to fetch our artifacts from S3.
Can be used to fetch other artifacts if you needed to.

compose-x-common
------------------

Common library across various compose-x projects that allows to make code-reuse easy.
