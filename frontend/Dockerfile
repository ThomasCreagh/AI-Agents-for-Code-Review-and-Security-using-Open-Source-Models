FROM node:18-alpine

WORKDIR /frontend-code

COPY package*.json .

RUN npm install --silent

COPY . .

ENV PORT=3000

EXPOSE 3000

CMD ["npm", "run", "dev"]

