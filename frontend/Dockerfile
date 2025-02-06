FROM node:18-alpine
#
# RUN mkdir -p /usr/src/app
# WORKDIR /usr/src/app
# ENV PATH /usr/src/app/node_modules/.bin:$PATH
# COPY package.json /usr/src/app/package.json
# RUN npm install --silent
# RUN npm install react-scripts@1.1.1 -g --silent
# COPY . /usr/src/app
# RUN npm run build


# WORKDIR /react-docker-example/
# add `/app/node_modules/.bin` to the $PATH
# ENV PATH /app/node_modules/.bin:$PATH
#
# COPY package.json /app/package.json
#
# WORKDIR /app
#
# RUN npm install
# RUN npm install -g react-scripts

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
COPY package.json /usr/src/app/package.json
RUN npm install --silent
RUN npm install react-scripts@1.1.1 -g --silent
COPY . /usr/src/app

CMD ["npm", "run", "build"]
CMD ["npm", "run", "start"]

