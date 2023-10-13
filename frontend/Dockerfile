FROM node:16.16.0-buster-slim

WORKDIR /opt/app/frontend

COPY package.json .
COPY package-lock.json .

# COPY . .

# RUN npm ci --dev

RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

# COPY ./assets/ ../django/assets/
# COPY ./bundles/ ../django/bundles/
