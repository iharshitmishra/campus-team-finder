# Multi-stage Dockerfile for Java 17 Javalin Backend
FROM maven:3.9-eclipse-temurin-17-alpine AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Lightweight JRE runtime
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=build /app/target/hackathon-team-finder-1.0.0.jar app.jar

ENV PORT=7070
EXPOSE 7070

ENTRYPOINT ["java", "-jar", "app.jar"]
