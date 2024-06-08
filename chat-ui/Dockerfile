# Use an official Node runtime as a parent image
FROM node:22.1-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install any needed packages
RUN npm install

# Bundle app source inside Docker image
COPY . .

# Build the React app
RUN npm run build

# Install serve to serve the production build
RUN npm install

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define command to run the app using serve
CMD ["npm", "start"]
