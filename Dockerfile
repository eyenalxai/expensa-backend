FROM python:3.11.1

RUN pip install pdm

WORKDIR /expensa

COPY ./pyproject.toml /expensa/pyproject.toml
COPY ./pdm.lock /expensa/pdm.lock
RUN pdm install

COPY ./app /expensa/app
COPY ./main.py /expensa/main.py

ENV DATABASE_URL ${DATABASE_URL}
ENV FRONTEND_DOMAIN ${FRONTEND_DOMAIN}
ENV HASHING_SECRET ${HASHING_SECRET}
ENV PORT ${PORT}

ARG EXPOSE_PORT=${PORT}
EXPOSE ${EXPOSE_PORT}

CMD ["pdm", "run", "start"]