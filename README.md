# DynamiCode

This file will show you how to set up a local version of the website on your computer and how to edit the website in
the Flask format.

## Set Up

Follow these instructions to set up a local version of the website.

### Python

First, make sure you have Python3 and pip installed.

To install the requirements, open a terminal in the project root directory and
run the following command (optionally while inside a virtual environment):

```pip install -r requirements.txt```


### Environment Variables

There are two ways to set up your environment variables.
1. (Recommended) Create a file in the project root directory (same directory as `requirements.txt`) called `env.json`.
Then edit the contents of that file to be:
   ```
   {
      "SECRET_KEY": "<some random string of characters>",
      "SQLALCHEMY_DATABASE_URL": "postgresql://skwqxwdjzdofnn:f4c0203d496efd50c5a8f395a1e2876c77896b675d23d200e170d09f0cf73d64@ec2-3-231-69-204.compute-1.amazonaws.com:5432/dacu2sq019mugb"
   }
   ```
2. Create real environment variables (look up how to do this based on your Operating System). Some IDEs (such as
PyCharm) will let you specify environment variables, which may be easier. Either way, add the following variables
to your environment:
   
   * `SECRET_KEY="<some random string of characters>"`
   * `SQLALCHEMY_DATABASE_URL="postgresql://skwqxwdjzdofnn:f4c0203d496efd50c5a8f395a1e2876c77896b675d23d200e170d09f0cf73d64@ec2-3-231-69-204.compute-1.amazonaws.com:5432/dacu2sq019mugb"`

## Run the Website

Once you've finished the setup, run the following command to start the website in development mode:

```python manage.py runserver```

When the website finishes loading, it will print out a website URL. Go to the URL to view the website.
In development mode (which is on by default), changes you make to the website take effect almost immediately. 
Refresh your page in the browser to view your new changes.

## How to Use Flask and Edit Files Safely

Using Flask changes a couple of things about the website. This section will inform you of how you can edit HTML files,
python files, etc. in a way that is compatible with Flask and won't cause errors.

### HTML Files

All HTML files **must** be located in the "templates" folder (though they can be in sub-folders as well).
In Flask, HTML files are able to do some fancy things using a language called Jinja2. Jinja2 supplements HTML, so
writing in pure HTML will work fine, but is not ideal.

One of the most important features of Jinja2 is that HTML files can inherit from other HTML files. Check out the
`templates/TEMPLATE.html` file. You will see that the first line inherits from the layout file
(see `templates/layout.html`). The layout file contains a common `<head>` tag, the nav bar, and "blocks" in which
files that inherit from this file can insert their own content.

In `TEMPLATE.html`, you fill also find two blocks; a "content" block, and a "scripts" block. Add the page's body to the
"content" block, and add any `<script>` tags to the "scripts" block. The `TEMPLATE.html` file is not meant to be
edited. It is just a reference for creating new HTML files.

#### Dynamic HTML

Jinja2 also allows us to personalize the content of HTML files without using javascript. To do so, we add Jinja2 syntax
to our HTML files. When we render an HTML file from the `routes.py` file (more information on this below), we can pass
variables to our HTML files. To access these variables directly, we can write `{{ var_name }}` in the HTML file. We can
add logic to our HTML files by writing `{% if some_condition %} ... {% else %} ... {% endif %}`. The spaces between the
`{% ... %}` logic blocks gets rendered as HTML depending on the result of the logic. Similarly, we can also use for
loops. For more information on this, see the [Jinja2 Documentation](https://jinja.palletsprojects.com/en/3.0.x/).

For an example, look at `templates/layout.html` and look at where the title is being set:

```html
{% if title %}    <!-- Checks if the variable 'title' was passed from python -->
    <title>{{ title }}</title>    <!-- Sets the title to whatever was passed from python -->
{% else %}    <!-- If the 'title' variable doesnt exist or evaluates to False -->
    <title>DynamiCode</title>    <!-- The default title for any page -->
{% endif %}
```

### Adding New Routes (a.k.a. pages)

To add a new page to the website, use the following syntax and add it to the `routes.py` file:

```python
@app.route("/PATH_TO_THE_NEW_PAGE")
def page_name():
    return flask.render_template("TEMPLATE.html", title="Page Title")  # add no_header=True to remove the header from the page 
```
