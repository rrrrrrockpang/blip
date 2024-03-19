# Use Node.js 14 as the base image
FROM node:14 as build

# Set the working directory
WORKDIR /react_app  

# Copy all files from the current directory to the working directory in the image
COPY . .

# Install all dependencies and build the project
RUN npm install
RUN npm run build

# Use Nginx alpine as the base image for the second stage
FROM nginx:alpine

# Copy the build output to the Nginx HTML directory
COPY --from=build /react_app/build /usr/share/nginx/html  

# Expose port 80
EXPOSE 3030

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
