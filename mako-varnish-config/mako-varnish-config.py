#!/usr/bin/env python

from mako.template import Template

default_template = Template(filename="default.vcl", module_directory="/tmp/",)

production = {
    "host": "localhost",
    "port": "80",
}
staging = {
    "host": "127.0.0.1",
    "port": "8080",
}

print("production", "\n", default_template.render(**production))
print("\n", "staging", "\n", default_template.render(**staging))
