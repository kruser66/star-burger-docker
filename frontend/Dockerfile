FROM node:16

ENV APP_HOME=/opt/app

RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/static

WORKDIR ${APP_HOME}

COPY package*.json ./
RUN npm install
RUN npm ci --include=dev

COPY bundles-src ./bundles-src

RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir static --public-url="./"

