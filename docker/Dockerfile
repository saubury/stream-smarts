FROM python:2.7

LABEL version="1.0"
LABEL description="Extending 2.7 image adding a few more pip packages"

# Install confluent-kafka and pushbullet packages
# Bypass enterprise ssl interception by ignoring validation - which is really bad
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --index-url=https://pypi.org/simple/ confluent-kafka
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --index-url=https://pypi.org/simple/ pushbullet.py

# I know you are not supposed to do this, it's not very docker-like
ENTRYPOINT ["tail", "-f", "/dev/null"]