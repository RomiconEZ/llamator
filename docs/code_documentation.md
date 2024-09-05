# Code documentation

```{hint}

  To add your code use sphinx tool in project root directory:

    $ sphinx-apidoc -o docs/api/ src/llamator

  and add reference from any page which is reachable from the index page.
```

```python
    import llamator
```

```{toctree}
---
maxdepth: 4
---
api/modules
```