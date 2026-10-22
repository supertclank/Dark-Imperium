FROM gradle:8.14.3-jdk21 AS build
WORKDIR /workspace/backend
COPY backend/ .
COPY database/ /workspace/database/
RUN gradle --no-daemon installDist
FROM eclipse-temurin:21-jre-jammy
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/* && useradd --uid 10001 --create-home app
WORKDIR /app
COPY --from=build /workspace/backend/build/install/dark-imperium-api/ ./
USER app
EXPOSE 8080
CMD ["bin/dark-imperium-api"]
