FROM balenalib/raspberry-pi-alpine-python:3.7.4-3.9-build as build

WORKDIR /pulsereader

# Install python requirements (to /pulsereader/reqs for multi stage build)
COPY ./src/requirements.txt requirements.txt
RUN mkdir reqs && pip3 install -r requirements.txt --target=reqs

# Copy code and configurations over
COPY ./src src
# We don't copy a pulse reader ini file to the container, it needs to be mounted. See README.md for details

# Do a multi-stage build to reduce final image size (by dropping all the build stuff)
FROM balenalib/raspberry-pi-alpine-python:3.7.4-3.9-run
WORKDIR /pulsereader
COPY --from=build /pulsereader .
ENV PYTHONPATH "${PYTHONPATH}:/pulsereader/reqs"
CMD ["python3","-u","src/main.py"]