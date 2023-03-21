==========================================
cookiecutter for new application pipeline
==========================================

-------------------------------------------------------------------------------------
Cookiecutter to create a new folder for a new app with all CICD for the application
-------------------------------------------------------------------------------------

How to use
===========

.. code-block:: bash

    python3 -m pip install cookiecutter --user
    git clone git@github.com:compose-x/codepipeline-orchestra
    cookiecutter codepipeline-orchestra/app-pipeline-boilerplate

Notes
    1. If you need checkmarx setup, request your Infosec Lead for Checkmarx Team Id, UserName and Password.
    2. Checkmarx notification mail Id must be a generic mail box for the team ideally.

Once you have the folder created, we can do the required the entity (you still need, sadly, to create the GIT repo from the UI).

.. code-block:: bash

   cd <project_name>/
   git init .
   git remote add origin git@github.com:${ORG_NAME:-comopse-x}/$(basename $PWD)
   git add *
   git add .gitignore
   git commit -m "Initial commit"
   git branch -m main
   git push origin main
