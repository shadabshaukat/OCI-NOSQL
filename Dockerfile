FROM python:3
ADD func.py /
ADD borneo-5.2.1-py2.py3-none-any.whl /

RUN pip install fdk
RUN pip install oci
RUN pip install ./borneo-5.2.1-py2.py3-none-any.whl

CMD [ "fdk", "./func.py", "handler"]
