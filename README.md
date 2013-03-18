# A more powerful include tag for Django

* Works with recursive includes
* Allows templates to be conditionally included, based on whether they exist
* Allows individual blocks to be included from a template
* Backwards-compatible with the Django built-in include tag


## Installation

```
pip install partial_include
```


## Usage

Load the tags:

```
{% load partial_include %}
```

Include a template:

```
{% include "mytemplate.html" %}
```

Include a block from the template:

```
{% include "mytemplate.html" with block="short_description" %}
```

Include a template, but suppress errors if it doesn't exist:

```
{% include "mytemplate.html" quiet %}
```

This works with blocks as well:

```
{% include "mytemplate.html" with block="short_description" quiet %}
```

Everything else works the same as the built-in Django include tag.

https://docs.djangoproject.com/en/dev/ref/templates/builtins/#include


# Running the tests

Execute runtests.py in the tests folder.
