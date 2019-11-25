# Example Walkthrough for eland

This example demonstrate the functionality of `eland` through a walkthrough of a simple analysis of the [Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/online+retail).

To run this example, make sure that you have an elasticsearch cluster running on port 9200 and please install any additional dependencies in addition to `eland`:

```
pip install -r requirements-example.txt
```

Once these requirements are satisfied, load the data using the provided script:

```
python load.py
```

This will create an index called `online-retail` with a mapping defined in `load.py`.

## See "it" in a Notebook

```
docker-compose build
docker-compose up
```

Go to http://127.0.0.1:8888/ and use the token `eland`.

Use `docker-compose down` to remove the docker images.
