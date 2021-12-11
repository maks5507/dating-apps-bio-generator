FROM node:15.12-alpine
RUN apk --no-cache add g++ gcc libgcc libstdc++ linux-headers make python

WORKDIR /app
COPY . .
RUN yarn

EXPOSE 22111

WORKDIR /
CMD ["node", "app"]