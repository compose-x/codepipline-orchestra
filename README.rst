==============================
CodePipeline Orchestra
==============================

This repository is a collection of useful tools that make usage of AWS CodePipeline/CodeBuild
and other AWS Developer tools.


Lambda Functions
==================

codepipeline_wrapper
----------------------

Although not critically difficult to implement, the payload from CodePipeline when invoking the lambda function always
has the same structure, and the pipeline expects a reply to it to know whether the execution was successful or not.

The wrapper function is the lambda handler that will deal with ingesting the source artifacts if any into a temp
folder, and allow to carry on with any custom code.


