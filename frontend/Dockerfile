FROM node:16.16.0-alpine

WORKDIR /opt/app/frontend

COPY package*.json .

RUN npm install
# RUN npm ci --include=dev

COPY . .

RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

