
#!/bin/bash
app="anp.api"
port=12345
docker build -t ${app} .
docker run -it --rm -p ${port}:80 \
  --env-file=env_file \
  --name=${app} \
  -v $PWD:/app ${app}
