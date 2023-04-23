# Safestat
Safestat is an app that keeps tabs on certain crime keywords on news platforms, and provides statistics about crime occurrances at different locations.

## Setting up the NER service

1. Download the model files and place in ner_service/models/transformers
2. cd into ner_service
3. Run setup.sh
4. Run docker container
    docker run -i -p 9000:5005 ner-service