FROM node:22-slim

WORKDIR /app

# Copy only package.json to ignore local package-lock.json (which might have Windows-specific bindings)
COPY package.json ./

# Clean install dependencies
RUN npm install

# Explicitly install Linux bindings for Rolldown to ensure they are present in the container
RUN npm install -D @rolldown/binding-linux-x64-gnu

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
