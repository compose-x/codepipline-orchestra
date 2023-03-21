{% for _ in range(0, cookiecutter.app_name|length +2) %}={% endfor %}
{{ cookiecutter.app_name }}
{% for _ in range(0, cookiecutter.app_name|length +2) %}={% endfor %}


{{ cookiecutter.short_description }}
{% for _ in range(0, cookiecutter.short_description|length +2) %}-{% endfor %}

A new application to deploy
