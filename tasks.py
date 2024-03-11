# Third Party
from invoke import task


@task
def docs(c):
    """Automate documentation tasks."""
    c.run("md_toc --in-place github --header-levels 4 README.md")
