# Flask Tricks

Super Blocks
It’s possible to render the contents of the parent block by calling super. This gives back the results of the parent block:

```html
{% block sidebar %}
<h3>Table Of Contents</h3>
<!-- More content here -->
{{ super() }}
<!-- Close -->
{% endblock %}
```

[More tricks](https://jinja.palletsprojects.com/en/2.10.x/templates/)
