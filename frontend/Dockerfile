# Use official Node base image
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files first (cache layer)
COPY package*.json .

# Install dependencies
RUN npm install

# Copy all frontend code
COPY . .

# Expose Vite dev port
EXPOSE 5173

# Start the dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]