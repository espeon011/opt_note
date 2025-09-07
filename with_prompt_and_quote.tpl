{%- extends 'markdown/index.md.j2' -%}

{% block codecell %}
In [{{ cell.execution_count if cell.execution_count else " " }}]:
```python
{{ cell.source | ipython2python }}
```
{% if cell.outputs %}
{% for out in cell.outputs %}
{{ "> ```\n" }}
{%- if out.text is defined -%}
> {{ out.text | replace("\n", "\n> ") }}
{%- elif 'text/plain' in out.data -%}
> {{ out.data['text/plain'] | replace("\n", "\n> ") }}
{%- endif %}
> ```
{% endfor %}
{% endif %}
{% endblock codecell %}
