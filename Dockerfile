FROM nvidia/cuda:12.8.0-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential python3 python3-pip python3-dev python3-venv git curl && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

RUN pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

RUN pip install \
    bitsandbytes==0.45.5 \
    trl==0.9.3 \
    peft==0.10.0 \
    transformers==4.40.1 \
    accelerate \
    datasets \
    sentence-transformers \
    jupyterlab \
    mlflow \
    huggingface_hub \
    ipywidgets \
    requests

RUN useradd -m -u 1000 -s /bin/bash analyst

USER analyst
ENV PATH="$PATH:/home/analyst/.local/bin"
WORKDIR /workspace

CMD ["jupyter", "lab", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--NotebookApp.token=", \
     "--NotebookApp.allow_origin=*", \
     "--NotebookApp.allow_root=True"]
