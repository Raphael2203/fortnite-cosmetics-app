FROM node:20
WORKDIR /app

# copy lock + package first for deterministic install during build
COPY package*.json ./

# install deps at build time (fast subsequent starts) - use ci for reproducibility
RUN npm ci

COPY . .

# expose vite dev server port
EXPOSE 5173

# run vite dev server and bind to all interfaces so host can access container
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]