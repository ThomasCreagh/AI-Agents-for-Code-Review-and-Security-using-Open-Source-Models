FROM ollama/ollama

ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

COPY ./get_models.sh /get_models.sh

# Fix Windows-style line endings (CRLF -> LF) and set execute permissions
# This may only be needed if the script was edited on Windows or has incorrect permissions
RUN sed -i 's/\r$//' /get_models.sh && \
    chmod +x /get_models.sh
