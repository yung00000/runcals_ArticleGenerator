#!/bin/bash
# Script to verify environment variables in Docker container
echo "Checking environment variables in container..."
docker exec runcals_article_generator_api env | grep -E "(DATABASE_URL|API_KEY|SUPABASE)" | sed 's/=.*/=***/'

