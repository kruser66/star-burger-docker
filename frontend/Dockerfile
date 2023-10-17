FROM node:16.16.0-alpine

ENV APP_HOME=/opt/app

RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

COPY package*.json ./

RUN npm ci --include=dev

COPY bundles-src ./bundles-src

RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

COPY . .
