{%- extends 'markdown/index.md.j2' -%}

{% block codecell %}
In [{{ cell.execution_count if cell.execution_count else " " }}]:
{{ "```python" }}
{{ cell.source }}
{{ "```\n" }}

{%- if cell.outputs -%}
{%- set cell_out_texts = ["> "] -%}
{%- for output in cell.outputs if output.output_type == 'stream' and output.name == 'stdout' -%}
{%- if output.text is defined -%}
{%- set _ = cell_out_texts.append(output.text | join('')) -%}
{%- elif 'text/plain' in out.data -%}
{%- set _ = cell_out_texts.append(out.data['text/plain'] | join('')) -%}
{%- endif -%}
{%- endfor -%}
{{ "\n> ```" }}
{{ cell_out_texts | join('') | trim | replace("\n", "\n> ") }}
{{ "> ```\n" }}
{%- endif -%}

{% endblock codecell %}
