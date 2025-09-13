#!/bin/bash
docker run -it -p 80:80 --name news-dev -e PORT=80 -e DEBUG=True -v $(pwd)/src:/app/src news-sumary
