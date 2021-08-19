################################################################################
#
# CopePipeline wrapper function
#
################################################################################

ifndef VERBOSE
.SILENT:
endif

RM					= rm -f
ECHO				= echo -e
TAG					= etags
PIP					= pip
PYTHON				= /usr/bin/python3
SHELL				= /bin/bash
WHICH   			= /usr/bin/which
WATCH   			= /usr/bin/watch
TEST    			= /usr/bin/test
ZIP     			= /usr/bin/zip
AWS					= aws

VENV 				?= .venv
VENV_ACTIVATE =. $(VENV)/bin/activate
ALIAS_NAME ?= $(shell bash -c 'read -p "Alias name: " alias; echo $$alias')

ifndef STACK
STACK				:= cicd-tool--codepipeline-wrapper
endif

ifndef FUNCTION_NAME
FUNCTION_NAME		:= ecr-codepipeline-wrapper
endif

ifndef TEMPLATE_FILE
TEMPLATE_FILE		:= codepipeline_function.template
endif

ifndef PARAMETERS_OVERRIDE
PARAMETERS_OVERRIDE	: ""
endif

ifndef BUCKET_NAME
BUCKET_NAME			?= $(shell bash -c 'read -p "bucket name: " alias; echo $$alias')
endif

ifndef PYTHON_VERSION
PYTHON_VERSION  	:= python38
endif

export VIRTUAL_ENV 	:= $(abspath ${VENV})
export PATH 		:= ${VIRTUAL_ENV}/bin:${PATH}

all					: venv template package

${VENV}				:
					$(PYTHON) -m venv $@

clean-template		:
					$(RM) $(FUNCTION_NAME).yml

clean				: clean-template
					$(RM) function.zip
					$(RM) -rf layer

python39			: clean
					test -d layer && rm -rf layer || mkdir layer
					docker run -u $(shell bash -c 'id -u'):$(shell bash -c 'id -u') \
					--rm -it -v $(PWD):/opt/build --entrypoint /bin/bash \
					public.ecr.aws/compose-x/python:3.9 \
					-c "pip install /opt/build/dist/codepipeline_wrapper-*.whl -t /opt/build/layer"

python38			: clean
					test -d layer && rm -rf layer || mkdir layer
					docker run -u $(shell bash -c 'id -u'):$(shell bash -c 'id -u') \
					--rm -it -v $(PWD):/opt/build --entrypoint /bin/bash \
					public.ecr.aws/compose-x/python:3.8 \
					-c "pip install /opt/build/dist/codepipeline_wrapper-*.whl -t /opt/build/layer"

python37			: clean
					test -d layer && rm -rf layer || mkdir layer
					docker run -u $(shell bash -c 'id -u'):$(shell bash -c 'id -u') \
					--rm -it -v $(PWD):/opt/build --entrypoint /bin/bash \
					public.ecr.aws/compose-x/python:3.7 \
					-c "pip install /opt/build/dist/codepipeline_wrapper-*.whl -t /opt/build/layer"

dist				: clean ## builds source and wheel package
					poetry build

package				: dist $(PYTHON_VERSION)
					pyclean layer/

venv-install		: requirements.txt | ${VENV}
					$(PIP) install -U pip
					$(PIP) install --upgrade -r requirements.txt

venv        		:
					test -d ${VENV} || $(MAKE) venv-install
					$(VENV_ACTIVATE)
					$(WHICH) python

template    		: clean-template $(VENV_ACTIVATE)
					$(AWS) cloudformation package --s3-bucket $(BUCKET_NAME) \
					--template-file $(TEMPLATE_FILE) \
					--output-template-file $(FUNCTION_NAME).yaml

deps       			: $(VENV_ACTIVATE) clean
					mkdir layer
					$(PIP) install -r requirements.txt -t layer

deploy      		: $(VENV_ACTIVATE) template validate
					$(AWS) cloudformation deploy --stack-name $(STACK) \
					--template-file $(FUNCTION_NAME).yaml \
					--capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_IAM $(PARAMETERS_OVERRIDE)

delete      		: clean-template
					$(AWS) cloudformation delete-stack --stack-name $(STACK)

validate    		: $(VENV_ACTIVATE)
					$(AWS) cloudformation validate-template \
					--template-body file://$(FUNCTION_NAME).yaml

events      		: $(VENV_ACTIVATE)
					$(AWS) cloudformation describe-stack-events \
					--stack-name $(STACK) \
					--region $(AWS_REGION)

watch       		:
					$(WATCH) --interval 1 "bash -c 'make events | head -40'"

.PHONY      		: all venv venv-install clean clean-template package layer dist
