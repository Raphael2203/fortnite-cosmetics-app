FROM node:20-slim

WORKDIR /app

COPY package*.json ./

RUN npm install
COPY . .

EXPOSE 4173

CMD ["npm", "run", "dev", "--", "--host"]