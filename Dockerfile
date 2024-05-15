FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y x11vnc xvfb lxde websockify xterm wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Download and extract noVNC
RUN wget https://github.com/novnc/noVNC/archive/refs/tags/v1.3.0.tar.gz && \
    tar -xvzf v1.3.0.tar.gz && \
    mv noVNC-1.3.0 /noVNC && \
    rm v1.3.0.tar.gz

# Copy custom vnc_auto.html
COPY vnc_auto.html /noVNC/vnc_auto.html

# Set environment variables
ENV DISPLAY=:99

# Start Xvfb, LXDE, x11vnc, and websockify
CMD /usr/bin/Xvfb :99 -screen 0 1024x768x16 & \
    sleep 2 && \
    startlxde & \
    sleep 2 && \
    x11vnc -display :99 -forever -nopw -shared & \
    websockify --web /noVNC 6080 localhost:5900
