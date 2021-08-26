==============================
CodePipeline Orchestra
==============================

This repository is a collection of useful tools that make usage of AWS CodePipeline/CodeBuild
and other AWS Developer tools.


AWS Accounts Setup for AWS CodePipeline
==================================================

In order to use AWS CodePipeline in a multi-account way, you will need to set IAM up properly to do so.
Properly and with a sense of least-privileges.

AWS Accounts Init
--------------------

In `aws_accounts_setup`_ you will find AWS CloudFormation templates that will allow you to set all these up.
Modify permissions or settings as you please.

To make it easy, an Ansible Playbook is available to allow you to set everything up in one command and save you
switching accounts in the AWS Console.

Lambda Functions
==================

codepipeline_wrapper
----------------------

Although not critically difficult to implement, the payload from CodePipeline when invoking the lambda function always
has the same structure, and the pipeline expects a reply to it to know whether the execution was successful or not.

The wrapper function is the lambda handler that will deal with ingesting the source artifacts if any into a temp
folder, and allow to carry on with any custom code.


.. _aws_accounts_setup: aws_accounts_setup/README.rst

