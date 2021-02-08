## ohdo2
```bash
docker image build \
--build-arg http_proxy \
--build-arg https_proxy \
-t ohdo2:latest .
```

```bash
docker container run \
--rm \
-it \
-e http_proxy \
-e https_proxy \
ohdo2:latest /bin/bash
```