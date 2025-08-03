# === Build stage ===
FROM eclipse-temurin:21-jdk AS build

# Set working directory
WORKDIR /app

# Copy your project source files
COPY . .

# Run Maven to build the app
RUN ./mvnw clean package -DskipTests

# === Runtime stage ===
FROM eclipse-temurin:21-jdk-alpine

WORKDIR /app

# Copy the built JAR from the build stage
COPY --from=build /app/target/*.jar app.jar

# Expose the app port
EXPOSE 8080

# Run the application
ENTRYPOINT ["java", "-jar", "app.jar"]
