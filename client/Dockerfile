FROM node:14.17.4-alpine
RUN apk add --no-cache bash
WORKDIR /client
#VOLUME ["/client"]
COPY package*.json ./
RUN npm install
EXPOSE 8080
CMD ["npm", "run", "theme:build"]
CMD ["npm", "run", "serve"]