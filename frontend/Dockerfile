FROM node:20

# Set the working directory
WORKDIR /frontend

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application files
COPY . .

# Expose the development server port
EXPOSE 5173

# Run the development server
CMD ["npm", "run", "dev", "--", "--host"]
