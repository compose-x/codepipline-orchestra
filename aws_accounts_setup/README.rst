=====================================
CodePipeline Templates
=====================================

This section provides with CFN templates and Ansible Roles that will allow you to deploy a baseline infrastructure
to make CodePipeline capable to deploy your applications and resources securely in AWS.


0 - Before you begin
=====================

You must have your credentials ready either in environment variables or in your AWS .aws/ config files.

.. warning::

    The use of aws-vault is not fully supported to run all of the commands. When not supported, it will be flagged.

Accounts Structure
-------------------

If you only have one AWS account, it is a lot simpler to sort the IAM permissions as this is all for a single account.
However, most of the people going through this repository probably will have a dev and a production account.

In the following guides, we will consider that we have 3 accounts:

* A "CICD management account" which has our artifacts store (S3, ECR, CodeArtifact etc.) and the pipelines/build projects
* A "non-prod" account, which can have dev/staging and any sort of environment that is not prod.
* A production account, where your customer (or internal) workloads are running.

.. tip::

    If you do not have a dedicated account for the "CICD Management", you can use the nonprod account for that purpose.
    Some settings will need to be set differently, that's all.

Settings templates
----------------------

Some of the templates in the following guide will be used to allow us to define some SSM Parameters and `AWS CloudFormation
Exports`_ that will allow us to put a deadlock in CFN (on top of potential `Termination Protection`_)


For the rest of the guide through, accounts as follow will be used


* 111111111111 - cicd management
* 222222222222 - non-prod
# 777777777777 - prod


Setup our artifacts store
===========================

In order to make a multi-account structure work, you will need to do a few things to get IAM etc. to play nicely.

KMS Key
----------
First, we create a new KMS Key that will be used to encrypt our artifacts in S3 (and possibly other resources).

Template: cicd_kms_key.template


.. _AWS CloudFormation Exports: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-exports.html
.. _Termination Protection: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-protect-stacks.html


S3 Buckets for our artifacts
----------------------------

The S3 bucket is central to ensuring that our artifacts, reports, or other resources (i.e. build cache) are available
for execution.

In the following template, we create two separate buckets, one for our Artifacts, and another for CFN and related templates.

Template: cicd_s3_buckets.template

The template will only create the bucket policies that are important for the cross account policies if the account ID value
given for **ProdAccountId** and **NonProdAccountId** are the same as the account ID the stack belongs to.

If you wish, you can input the IAM Role ID of the roles we will create afterwards to restrict the bucket access to these
roles only to the bucket, for additional security.

Execute
--------

