=================================================
CodePipeline Setup - mono and multi-accounts
=================================================

This section provides with CFN templates and Ansible Roles that will allow you to deploy a baseline infrastructure
to make CodePipeline capable to deploy your applications and resources securely in AWS.

.. contents::


Before you begin
=====================

You must have your credentials ready either in environment variables or in your AWS .aws/ config files.

.. warning::

    The use of aws-vault is not fully supported to run all of the commands. When not supported, it will be flagged.

Accounts Structure
===================

If you only have one AWS account, it is a lot simpler to sort the IAM permissions as this is all for a single account.
However, most of the people going through this repository probably will have a dev and a production account.

In the following guides, we will consider that we have 3 accounts:

* A "CICD management account" which has our artifacts store (S3, ECR, CodeArtifact etc.) and the pipelines/build projects
* A "non-prod" account, which can have dev/staging and any sort of environment that is not prod.
* A production account, where your customer (or internal) workloads are running.

.. tip::

    If you do not have a dedicated account for the "CICD Management", you can use the nonprod account for that purpose.
    Some settings will need to be set differently, that's all.

Why a dedicated CICD account though ?
-----------------------------------------

Assume that you use the same account for CICD as for dev. Assume that your nonprod account stores your build artifacts,
your ECR images, your application source code.

Now imagine if a dev creates an application that has an IAM policy all too permissive, get pawned, and retrieves credentials
that grant access to all the things.

Your source code could get stolen, information of all kind. Or, almost worst, what if the hacker plants his own little services,
in a corner with similar names as your applications, finds ways to capture that pre-prod data and silently leaks information ....

You want a nonprod account you can in an instant get rid of, destroy all the things, and start fresh, without loosing or
compromising your artifacts.

.. hint::

    Most services, such as ECR, now offer cross-accounts replication for DR.

Settings templates
===================

Some of the templates in the following guide will be used to allow us to define some SSM Parameters and `AWS CloudFormation
Exports`_ that will allow us to put a deadlock in CFN (on top of potential `Termination Protection`_)


For the rest of the guide through, when refering to AWS accounts, we will use the following IDs

* 111111111111 - cicd management
* 222222222222 - non-prod
* 777777777777 - prod


Setup our artifacts store and IAM access
==========================================

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

IAM Roles
----------

In order to perform cross account roles pipelines executions, we need to set AWS IAM up to allow the CodePipeline
roles we will create later on to invoke lambda functions, start codebuild projects, and create CFN stacks.

.. image::  https://blog.compose-x.io/images/cicd-pipeline/cicd-iam-structure.jpg

Cross Account role
+++++++++++++++++++++

This is the role assumed by our CodePipeline role in the management account. It has access to only manipulate
CloudFormation stacks and manage AWS CodeBuild in our nonprod and prod accounts.

CloudFormation Role
++++++++++++++++++++++

This role is given to AWS CloudFormation when creating a new Stack. It has high privileges in order to create/delete etc.
the resources we want to deploy.

Although it has high privileges, this allows **not** to give our `Cross Account role`_ any privileges on creating the
resources itself.

BuildRoles
+++++++++++++++

This is a role we will be able to use for AWS Lambda Function or AWS CodeBuild projects in the nonprod/prod account
to perform some very limited actions. Mostly it is there to allow access to the S3 Buckets and the KMS Key in the
CICD Account.

CrossReadOnly role
+++++++++++++++++++++

This role is a very useful role that will allow us to do services and resources discovery to retrieve information
from one account to the other.

This is very useful and does not grant access to S3 or anything, just describe our account resources, and use the
Tagging API for further discovery.

Execute
=========

Using a very simple Ansible Playbook, we are going to create a series of AWS CloudFormation stacks with the templates
we described above, retrieve the output information from the stack, and use that as input into further executions.
Ansible makes it easy for us to switch account and create the stacks in the appropriate accounts with the values we
need to get ready to create our first Cross-Accounts CICD Pipelines.

Use the commands below to install and run ansible.

.. tip::

    Change the profile names with the appropriate AWS profile names configured in ~/.aws/config (or ~/.aws/credentials)

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate
    pip install pip -U
    pip install ansible==4.4.0
    ansible-galaxy collection install amazon.aws
    ansible-playbook playbook-cicd-01.yaml              \
        -e cicd_account_profile=cicd_profile            \
        -e nonprod_account_profile=nonprod_profile      \
        -e prod_account_profile=prod_profile

.. hint::

    You can set the profile to be the same for all 3 accounts, but again, recommend to use 3 separate accounts
    in your organization for production workloads.

Summary
=========

Using simple CloudFormation templates and ansible, we have now got a set of IAM roles in place in our accounts
we will deploy the applications to, S3 bucket with KMS encryption for our artifacts, and permissions sorted out
to use them.

