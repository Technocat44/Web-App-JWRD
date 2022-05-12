FROM python:3 

RUN mkdir /usr/src/server/
COPY . /usr/src/server/
WORKDIR /usr/src/server/
EXPOSE 5000

RUN pip install --user pyopenssl
#RUN pip3 install -r  requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
#RUN pip install --user python-ldap
#RUN python3 -m pip install python-dev-tools --user --upgrade
RUN python -m pip install --user --upgrade setuptools
#RUN python -m pip install --user python-ldap
RUN pip install --user --upgrade -r requirements.txt


ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
CMD /wait && python3 server.py --host=0.0.0.0