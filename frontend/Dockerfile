FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /frontend-code


# Copy package.json and package-lock.json first (for efficient caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --legacy-peer-deps --silent

# Copy the entire application
COPY . .

# Build the Next.js application
RUN npm run build

# Expose the application port
ENV PORT=3000
EXPOSE 3000

# Start the production server
CMD ["npm", "start"]


