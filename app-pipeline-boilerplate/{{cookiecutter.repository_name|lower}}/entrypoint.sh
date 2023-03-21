#!/bin/bash

{% if cookiecutter.runtime == "java" %}
export JAVA_OPTS=${JAVA_OPTS:-$JAVA_DEFAULT_OPTS}
exec java $EXTRA_ARGS "$@"
{% elif cookiecutter.runtime == "python" %}
exec python "$@"
{% else %}
exec "$@"
{% endif %}
