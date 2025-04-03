# FROM node:18-alpine
#
# # Set the working directory inside the container
# WORKDIR 
#
# # Copy package.json and package-lock.json to install dependencies first (to optimize Docker cache)
# COPY package*.json ./
#
# # Install dependencies (using --legacy-peer-deps to avoid issues with conflicting peer dependencies)
# RUN npm install --legacy-peer-deps --silent
#
# # Copy the rest of the application code
# COPY . .
#
# # Set the environment variable for the application port
# ENV PORT=3000
#
# # Expose port 3000 for the app
# EXPOSE 3000
#
# # Default command to start the application
# # CMD ["npm", "run", "dev"]
# CMD ["next", "start"]
# Use Node.js 18 Alpine for a smaller image
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


